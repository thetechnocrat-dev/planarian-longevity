from ultralytics import YOLO

# Load the trained model
model = YOLO('./runs/detect/train/weights/best.pt')

# Perform inference on an image
results = model('./flatworms_example.png', save=True)
