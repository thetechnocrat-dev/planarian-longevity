from ultralytics import YOLO

# Load the pre-trained YOLOv8 model with COCO weights
model = YOLO('./data/yolov8n.pt')

# Train the model on your dataset
model.train(
    data='data.yaml',  # Make sure this points to your dataset configuration
    epochs=50,
    batch=16,
    imgsz=640  # Image size
)
