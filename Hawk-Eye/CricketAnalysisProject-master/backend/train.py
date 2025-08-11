import os
import torch
from ultralytics import YOLO

def main():
    # Model and config
    model_path = 'yolov8n.pt'  # Make sure this file exists in your backend/ directory
    yaml_path = os.path.join('cricket_ball_data', 'data.yaml')  # ✅ updated folder name

    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"Model file {model_path} not found. Downloading...")
        # This will automatically download the model if it doesn't exist
        model = YOLO('yolov8n.pt')
    else:
        # Load YOLO model
        model = YOLO(model_path)

    # Start training
    model.train(
        data=yaml_path,
        epochs=50,
        imgsz=640,
        batch=8,
        project='runs',
        name='cricket_ball_train',
        workers=1,
        verbose=True
    )

if __name__ == '__main__':
    main()
