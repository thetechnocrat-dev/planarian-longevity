import ffmpeg
import os
import tempfile
from celery import shared_task
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from ultralytics import YOLO
from pathlib import Path
from .models import Measurement

def convert_avi_to_mp4(avi_filepath, output_filepath):
    (
        ffmpeg
        .input(avi_filepath)
        .output(output_filepath, vcodec='libx264')
        .run(overwrite_output=True)
    )

@shared_task
def process_video(measurement_id):
    measurement = Measurement.objects.get(id=measurement_id)
    s3_video_path = measurement.value
    
    # Download the video from S3 to a temp directory
    with tempfile.NamedTemporaryFile(suffix='.avi', delete=False) as tmp_file:
        tmp_file.write(default_storage.open(s3_video_path, 'rb').read())
        video_filepath = tmp_file.name

    processed_video_path = perform_video_analysis(video_filepath)

    # Upload the processed video to S3
    with open(processed_video_path, 'rb') as f:
        s3_key = f"{measurement.device.uuid}/inference/{os.path.basename(processed_video_path)}"
        default_storage.save(s3_key, ContentFile(f.read()))

    measurement.inference_value = s3_key
    measurement.save()

    # Clean up local files
    os.remove(video_filepath)
    os.remove(processed_video_path)

def perform_video_analysis(video_filepath):
    BASE_DIR = settings.BASE_DIR
    model_path = BASE_DIR / 'vision' / 'models' / 'best_v1.pt'
    model = YOLO(model_path)

    # Perform inference on a video and save the results
    results = model.track(source=video_filepath, save=True)

    avi_output_filepath = os.path.join(results[0].save_dir, f"{os.path.splitext(os.path.basename(video_filepath))[0]}.avi")
    mp4_output_filepath = os.path.join(results[0].save_dir, f"{os.path.splitext(os.path.basename(video_filepath))[0]}.mp4")
    convert_avi_to_mp4(avi_output_filepath, mp4_output_filepath)

    # Remove the original YOLO output avi video
    os.remove(avi_output_filepath)
 
    return mp4_output_filepath
