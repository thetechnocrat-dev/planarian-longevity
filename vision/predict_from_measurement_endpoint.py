import os
import platform
import time
import requests
import boto3
import subprocess
from ultralytics import YOLO
import torch
import timeit
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuration
WORKER_SECRET = os.getenv('WORKER_SECRET', 'your_worker_secret')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.openzyme.bio')
RETRIEVE_ENDPOINT = f"{API_BASE_URL}/devices/get_unprocessed_measurement/"
UPDATE_ENDPOINT = f"{API_BASE_URL}/devices/update_inference_value/"
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
CHECK_INTERVAL = 3  # seconds

# Check if CUDA is available and use GPU if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the trained model
model_load_start_time = timeit.default_timer()
model = YOLO('./models/best_v1.pt').to(device)
model_load_end_time = timeit.default_timer()
print(f"Model loading time: {model_load_end_time - model_load_start_time:.2f} seconds")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def download_file_from_s3(presigned_url, local_path):
    response = requests.get(presigned_url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception("Failed to download file from S3")

def upload_file_to_s3(local_path, s3_key):
    try:
        s3_client.upload_file(
            local_path,
            AWS_STORAGE_BUCKET_NAME,
            s3_key,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception(f"S3 upload failed: {str(e)}")

def update_inference_value(measurement_id, inference_value, inference_status):
    response = requests.post(
        UPDATE_ENDPOINT,
        data={'id': measurement_id, 'inference_value': inference_value, 'inference_status': inference_status, 'worker_secret': WORKER_SECRET}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to update inference value: {response.content}")

while True:
    try:
        # Fetch the next measurement to process
        response = requests.get(
            RETRIEVE_ENDPOINT,
            params={'worker_secret': WORKER_SECRET}
        )

        if response.status_code == 200:
            measurement = response.json()
            measurement_id = measurement['id']
            print(f"Picked up measurement: {measurement_id}")
            s3_path = measurement['value']
            presigned_url = measurement['presigned_url']

            # Update inference state to 'processing'
            update_inference_value(measurement_id, None, 'processing')

            try:
                # Create local paths for input and output
                local_input_path = f"/tmp/{os.path.basename(s3_path)}"
                local_output_mp4_path = f"/tmp/{os.path.splitext(os.path.basename(s3_path))[0]}_tracked.mp4"

                print(f"Local input path: {local_input_path}")
                print(f"Local output MP4 path: {local_output_mp4_path}")

                # Download the video from S3
                download_start_time = timeit.default_timer()
                download_file_from_s3(presigned_url, local_input_path)
                download_end_time = timeit.default_timer()
                print(f"Download time: {download_end_time - download_start_time:.2f} seconds")

                # Perform inference on the video
                start_time = timeit.default_timer()
                inference_start_time = timeit.default_timer()
                results = model.track(source=local_input_path, save=True)
                inference_end_time = timeit.default_timer()
                print(f"Inference time: {inference_end_time - inference_start_time:.2f} seconds")

                # Retrieve the actual saved path from YOLO results
                saved_video_dir = results[0].save_dir
                saved_video_path = os.path.join(saved_video_dir, os.path.basename(local_input_path))
                print(f"YOLO output path: {saved_video_path}")

                # Retrieve the actual saved path from YOLO results
                saved_video_dir = results[0].save_dir
                saved_video_name = os.path.basename(local_input_path)

                # Change the extension to .avi if not Mac
                if platform.system() != 'Darwin':
                    saved_video_name = os.path.splitext(saved_video_name)[0] + '.avi'

                saved_video_path = os.path.join(saved_video_dir, saved_video_name)
                print(f"YOLO output path: {saved_video_path}")

                # Convert the saved video to MP4 using ffmpeg
                conversion_start_time = timeit.default_timer()
                command = f"ffmpeg -y -i {saved_video_path} -vcodec libx264 -movflags +faststart -color_range pc -chroma_sample_location center {local_output_mp4_path}"
                subprocess.run(command, shell=True, check=True)
                conversion_end_time = timeit.default_timer()
                print(f"Video conversion time: {conversion_end_time - conversion_start_time:.2f} seconds")

                # Upload the processed video back to S3
                s3_key = f"{os.path.splitext(s3_path)[0]}_tracked.mp4"
                upload_start_time = timeit.default_timer()
                upload_file_to_s3(local_output_mp4_path, s3_key)
                upload_end_time = timeit.default_timer()
                print(f"Upload time: {upload_end_time - upload_start_time:.2f} seconds")

                # Update the inference value and state in the Django app
                update_inference_value(measurement_id, s3_key, 'succeeded')

                total_end_time = timeit.default_timer()
                print(f"Total processing time: {total_end_time - start_time:.2f} seconds")
                print(f"Processed video saved at: {local_output_mp4_path}")

                # Clean up local files
                os.remove(local_input_path)
                os.remove(saved_video_path)
                os.remove(local_output_mp4_path)

            except Exception as e:
                print(f"Error processing measurement {measurement_id}: {e}")
                update_inference_value(measurement_id, None, 'failed')

        elif response.status_code == 404:
            print("No measurements found, sleeping...")
            time.sleep(CHECK_INTERVAL)
        else:
            raise Exception(f"Failed to fetch measurement: {response.content}")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)
