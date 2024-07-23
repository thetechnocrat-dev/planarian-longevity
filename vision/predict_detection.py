from ultralytics import YOLO
import moviepy.editor as mp
import os

# Load the trained model
model = YOLO('./models/best_v1.pt')

input_filename = 'flatworms_example.mp4'

# Perform inference on a video and save the results in the specified directory
results = model.track(source=input_filename, save=True)

output_filepath = os.path.join(results[0].save_dir, f"{input_filename[0:-4]}.avi")

# Convert the saved video to MP4 using moviepy
converted_filepath = f"{output_filepath[0:-4]}.mp4"

clip = mp.VideoFileClip(output_filepath)
clip.write_videofile(converted_filepath, codec='libx264')

# Clean up the original YOLO output video if needed
# os.remove(input_video_path)
