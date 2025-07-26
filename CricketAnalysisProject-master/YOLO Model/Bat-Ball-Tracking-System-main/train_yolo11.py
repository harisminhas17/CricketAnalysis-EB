import os
import torch
import yaml
from pathlib import Path

def train_yolo11():
    print("=== YOLO 11 Training Script ===")
    
    # Check if YOLO 11 model exists
    yolo11_model_path = Path('../yolo11n.pt')
    if not yolo11_model_path.exists():
        print(f"Error: YOLO 11 model {yolo11_model_path} not found!")
        return
    
    print(f"✓ Found YOLO 11 model: {yolo11_model_path}")
    
    # Check data.yaml
    if not Path('data.yaml').exists():
        print("Error: data.yaml not found!")
        return
    
    print("✓ Found data.yaml")
    
    # Check dataset
    if not Path('dataset/train/images').exists():
        print("Error: Training images not found!")
        return
    
    print("✓ Found training images")
    
    # Check labels
    labels_dir = Path('dataset/train/labels')
    if not labels_dir.exists():
        print("Error: Labels directory not found! Run convert_csv_to_yolo.py first.")
        return
    
    label_count = len(list(labels_dir.glob('*.txt')))
    print(f"✓ Found {label_count} label files")
    
    # Install ultralytics if not available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO available")
    except ImportError:
        print("Installing ultralytics...")
        os.system("pip install ultralytics")
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO installed")
    
    # Load and train the model
    print("\n=== Starting YOLO 11 Training ===")
    
    try:
        # Load the YOLO 11 model
        model = YOLO(str(yolo11_model_path))
        print(f"✓ Loaded YOLO 11 model: {yolo11_model_path}")
        
        # Start training
        results = model.train(
            data='data.yaml',
            epochs=50,
            imgsz=640,
            batch=16,
            name='yolo11_ball_detect',
            project='runs/train',
            verbose=True,
            save=True,
            save_period=10
        )
        
        print("✓ Training completed successfully!")
        print(f"Results saved in: runs/train/yolo11_ball_detect/")
        
    except Exception as e:
        print(f"Error during training: {e}")
        print("Please check your model file and dataset.")

if __name__ == "__main__":
    train_yolo11() 