from ultralytics import YOLO
import os
import torch
import timeit

# Check if CUDA is available and use GPU if possible
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Measure total time
start_time = timeit.default_timer()

# Load the trained model
model_load_start_time = timeit.default_timer()
model = YOLO('./models/best_v1.pt').to(device)
model_load_end_time = timeit.default_timer()
print(f"Model loading time: {model_load_end_time - model_load_start_time:.2f} seconds")

input_filename = 'flatworms_example.mp4'

# Perform inference on a video and save the results in the specified directory
inference_start_time = timeit.default_timer()
results = model.track(source=input_filename, save=True)
inference_end_time = timeit.default_timer()
print(f"Inference time: {inference_end_time - inference_start_time:.2f} seconds")

output_filepath = os.path.join(results[0].save_dir, f"{input_filename[0:-4]}.avi")

# Convert the saved video to MP4 using moviepy
conversion_start_time = timeit.default_timer()
converted_filepath = f"{output_filepath[0:-4]}.mp4"

# Efficiently convert using ffmpeg directly
os.system(f"ffmpeg -i {output_filepath} -vcodec libx264 {converted_filepath}")
conversion_end_time = timeit.default_timer()
print(f"Video conversion time: {conversion_end_time - conversion_start_time:.2f} seconds")

# Clean up the original YOLO output video if needed
# os.remove(output_filepath)

total_end_time = timeit.default_timer()
print(f"Total processing time: {total_end_time - start_time:.2f} seconds")

print(f"Processed video saved at: {converted_filepath}")
