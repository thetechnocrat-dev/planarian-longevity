import os
import time
import requests
import boto3
from ultralytics import YOLO
import torch
import timeit
from datetime import datetime, timedelta
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
CHECK_INTERVAL = 3 # seconds
RECORDING_DATE = (datetime.now() - timedelta(days=7)).isoformat()

# Check if CUDA is available and use GPU if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the trained model
model_load_start_time = timeit.default_timer()
model = YOLO('./models/best_v1.pt').to(device)
model_load_end_time = timeit.default_timer()
print(f"Model loading time: {model_load_end_time - model_load_start_time:.2f} seconds")

# S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def download_file_from_s3(presigned_url, local_path):
    download_start_time = timeit.default_timer()
    response = requests.get(presigned_url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        download_end_time = timeit.default_timer()
        print(f"Download time: {download_end_time - download_start_time:.2f} seconds")
    else:
        raise Exception("Failed to download file from S3")

def upload_file_to_s3(local_path, s3_key):
    upload_start_time = timeit.default_timer()
    try:
        s3_client.upload_file(local_path, AWS_STORAGE_BUCKET_NAME, s3_key)
        upload_end_time = timeit.default_timer()
        print(f"Upload time: {upload_end_time - upload_start_time:.2f} seconds")
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception(f"S3 upload failed: {str(e)}")

def update_inference_value(measurement_id, inference_value):
    response = requests.post(
        UPDATE_ENDPOINT,
        data={'id': measurement_id, 'inference_value': inference_value, 'worker_secret': WORKER_SECRET}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to update inference value: {response.content}")

while True:
    try:
        # Fetch the next measurement to process
        response = requests.get(
            RETRIEVE_ENDPOINT,
            params={'worker_secret': WORKER_SECRET, 'recorded_after': RECORDING_DATE}
        )

        if response.status_code == 200:
            measurement = response.json()
            measurement_id = measurement['id']
            s3_path = measurement['value']
            presigned_url = measurement['presigned_url']
            
            # Download the video from S3
            local_input_path = '/tmp/input_video.mp4'
            download_file_from_s3(presigned_url, local_input_path)

            # Perform inference on the video
            start_time = timeit.default_timer()
            inference_start_time = timeit.default_timer()
            results = model.track(source=local_input_path, save=True)
            inference_end_time = timeit.default_timer()
            print(f"Inference time: {inference_end_time - inference_start_time:.2f} seconds")

            output_filepath = os.path.join(results[0].save_dir, f"{os.path.splitext(local_input_path)[0]}.avi")

            # Convert the saved video to MP4 using ffmpeg
            conversion_start_time = timeit.default_timer()
            converted_filepath = f"{os.path.splitext(output_filepath)[0]}.mp4"
            os.system(f"ffmpeg -i {output_filepath} -vcodec libx264 {converted_filepath}")
            conversion_end_time = timeit.default_timer()
            print(f"Video conversion time: {conversion_end_time - conversion_start_time:.2f} seconds")

            # Upload the processed video back to S3 with '_tracked' suffix
            s3_key_tracked = f"{os.path.splitext(s3_path)[0]}_tracked.mp4"
            upload_file_to_s3(converted_filepath, s3_key_tracked)

            # Update the inference value in the Django app
            update_inference_value(measurement_id, s3_key_tracked)

            # Clean up local files
            os.remove(local_input_path)
            os.remove(output_filepath)
            os.remove(converted_filepath)

            total_end_time = timeit.default_timer()
            print(f"Total processing time: {total_end_time - start_time:.2f} seconds")
            print(f"Processed video saved at: {converted_filepath}")

        elif response.status_code == 404:
            print("No measurements found, sleeping...")
            time.sleep(CHECK_INTERVAL)
        else:
            raise Exception(f"Failed to fetch measurement: {response.content}")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)
