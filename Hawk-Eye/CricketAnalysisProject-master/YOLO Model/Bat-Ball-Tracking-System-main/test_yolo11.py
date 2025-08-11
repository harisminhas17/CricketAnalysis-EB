import cv2
import torch
import numpy as np
from pathlib import Path
import argparse

def test_yolo11_model():
    print("=== YOLO 11 Model Testing ===")
    
    # Check if the trained model exists
    model_path = Path('runs/train/yolo11_ball_detect/weights/best.pt')
    if not model_path.exists():
        print(f"Error: Trained model not found at {model_path}")
        print("Please make sure training has completed successfully.")
        return
    
    print(f"✓ Found trained model: {model_path}")
    
    # Install ultralytics if not available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO available")
    except ImportError:
        print("Installing ultralytics...")
        import os
        os.system("pip install ultralytics")
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO installed")
    
    # Load the trained model
    try:
        model = YOLO(str(model_path))
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Test options
    print("\n=== Testing Options ===")
    print("1. Test on training images")
    print("2. Test on test videos")
    print("3. Test on a specific image")
    print("4. Test on webcam")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_on_training_images(model)
    elif choice == "2":
        test_on_test_videos(model)
    elif choice == "3":
        test_on_specific_image(model)
    elif choice == "4":
        test_on_webcam(model)
    else:
        print("Invalid choice. Please run the script again.")

def test_on_training_images(model):
    """Test on a few training images"""
    print("\n=== Testing on Training Images ===")
    
    images_dir = Path('dataset/train/images')
    if not images_dir.exists():
        print("Training images directory not found!")
        return
    
    # Get first 5 images
    image_files = list(images_dir.glob('*.png'))[:5]
    
    for i, img_path in enumerate(image_files):
        print(f"\nTesting image {i+1}: {img_path.name}")
        
        # Run inference
        results = model(str(img_path), conf=0.5)  # Confidence threshold 0.5
        
        # Display results
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                print(f"  Detected {len(boxes)} objects:")
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = ['ball', 'bat'][cls]
                    print(f"    - {class_name}: {conf:.3f}")
            else:
                print("  No objects detected")
        
        # Save annotated image
        output_path = f"test_result_{i+1}.jpg"
        for result in results:
            annotated_img = result.plot()
            cv2.imwrite(output_path, annotated_img)
            print(f"  Saved annotated image: {output_path}")

def test_on_test_videos(model):
    """Test on test videos"""
    print("\n=== Testing on Test Videos ===")
    
    videos_dir = Path('dataset/test')
    if not videos_dir.exists():
        print("Test videos directory not found!")
        return
    
    video_files = list(videos_dir.glob('*.mp4'))
    
    for i, video_path in enumerate(video_files):
        print(f"\nTesting video {i+1}: {video_path.name}")
        
        # Run inference on video
        results = model(str(video_path), conf=0.5, save=True, project='test_results', name=f'video_{i+1}')
        
        print(f"  Results saved in: test_results/video_{i+1}/")

def test_on_specific_image(model):
    """Test on a specific image file"""
    print("\n=== Testing on Specific Image ===")
    
    image_path = input("Enter the path to your image: ").strip()
    
    if not Path(image_path).exists():
        print("Image file not found!")
        return
    
    print(f"Testing image: {image_path}")
    
    # Run inference
    results = model(image_path, conf=0.5)
    
    # Display results
    for result in results:
        boxes = result.boxes
        if boxes is not None:
            print(f"Detected {len(boxes)} objects:")
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = ['ball', 'bat'][cls]
                print(f"  - {class_name}: {conf:.3f}")
        else:
            print("No objects detected")
    
    # Save annotated image
    output_path = "test_result_specific.jpg"
    for result in results:
        annotated_img = result.plot()
        cv2.imwrite(output_path, annotated_img)
        print(f"Saved annotated image: {output_path}")

def test_on_webcam(model):
    """Test on webcam feed"""
    print("\n=== Testing on Webcam ===")
    print("Press 'q' to quit")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run inference
        results = model(frame, conf=0.5)
        
        # Draw results on frame
        annotated_frame = results[0].plot()
        
        # Display frame
        cv2.imshow('YOLO 11 Cricket Detection', annotated_frame)
        
        # Break on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_yolo11_model() 