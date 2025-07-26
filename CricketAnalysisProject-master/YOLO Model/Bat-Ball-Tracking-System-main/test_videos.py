import cv2
import torch
from pathlib import Path
from ultralytics import YOLO

def test_on_videos():
    print("=== YOLO 11 Video Testing ===")
    
    # Check if the trained model exists
    model_path = Path('runs/train/yolo11_ball_detect/weights/best.pt')
    if not model_path.exists():
        print(f"Error: Trained model not found at {model_path}")
        return
    
    print(f"✓ Found trained model: {model_path}")
    
    # Load the trained model
    try:
        model = YOLO(str(model_path))
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Check test videos directory
    videos_dir = Path('dataset/test')
    if not videos_dir.exists():
        print("Test videos directory not found!")
        return
    
    video_files = list(videos_dir.glob('*.mp4'))
    print(f"✓ Found {len(video_files)} test videos")
    
    # Test on each video
    for i, video_path in enumerate(video_files):
        print(f"\n--- Testing Video {i+1}: {video_path.name} ---")
        
        try:
            # Run inference on video with confidence threshold 0.5
            results = model(
                str(video_path), 
                conf=0.5, 
                save=True, 
                project='video_test_results', 
                name=f'video_{i+1}',
                verbose=True
            )
            
            print(f"✓ Video {i+1} processed successfully")
            print(f"  Results saved in: video_test_results/video_{i+1}/")
            
        except Exception as e:
            print(f"Error processing video {i+1}: {e}")
    
    print(f"\n=== Testing Complete ===")
    print("All video results saved in: video_test_results/")
    print("You can find the processed videos with ball and bat detection boxes drawn on them.")

if __name__ == "__main__":
    test_on_videos() 