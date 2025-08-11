import cv2
import torch
from pathlib import Path
from ultralytics import YOLO
import argparse
import os

def test_cricket_video(video_path, confidence=0.5):
    """
    Test YOLO model on a cricket video
    """
    print("=== Cricket Video YOLO Test ===")
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        return
    
    print(f"✓ Video found: {video_path}")
    
    # Check for trained model
    model_path = Path('yolo11n.pt')  # Using the model in root directory
    if not model_path.exists():
        print(f"❌ Error: YOLO model not found at {model_path}")
        print("Please make sure yolo11n.pt is in the current directory")
        return
    
    print(f"✓ Found YOLO model: {model_path}")
    
    # Load the model
    try:
        model = YOLO(str(model_path))
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Get video info
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    cap.release()
    
    print(f"📹 Video Info:")
    print(f"  - Total frames: {total_frames}")
    print(f"  - FPS: {fps:.2f}")
    print(f"  - Duration: {duration:.2f} seconds")
    print(f"  - Confidence threshold: {confidence}")
    
    # Run detection
    print(f"\n🔍 Running YOLO detection...")
    print("This may take a few minutes depending on video length...")
    
    try:
        # Run inference
        results = model(
            video_path,
            conf=confidence,
            save=True,
            project='cricket_detection_results',
            name='test_video',
            verbose=True
        )
        
        print(f"\n✅ Detection completed!")
        
        # Analyze results
        print(f"\n📊 Detection Summary:")
        
        # Count detections per frame
        ball_count = 0
        bat_count = 0
        total_frames_processed = 0
        
        for result in results:
            total_frames_processed += 1
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    if cls == 0:  # Ball
                        ball_count += 1
                    elif cls == 1:  # Bat
                        bat_count += 1
        
        print(f"  - Frames processed: {total_frames_processed}")
        print(f"  - Total ball detections: {ball_count}")
        print(f"  - Total bat detections: {bat_count}")
        print(f"  - Average balls per frame: {ball_count/total_frames_processed:.2f}")
        print(f"  - Average bats per frame: {bat_count/total_frames_processed:.2f}")
        
        # Save results
        output_path = "cricket_detection_results/test_video/"
        print(f"\n📁 Results saved in: {output_path}")
        print(f"  - Processed video with detection boxes")
        print(f"  - Detection data and statistics")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test YOLO model on cricket video')
    parser.add_argument('video_path', help='Path to cricket video file')
    parser.add_argument('--confidence', '-c', type=float, default=0.5, 
                       help='Confidence threshold (0.1-0.9, default: 0.5)')
    
    args = parser.parse_args()
    
    # Validate confidence
    if args.confidence < 0.1 or args.confidence > 0.9:
        print("❌ Error: Confidence must be between 0.1 and 0.9")
        return
    
    # Run test
    success = test_cricket_video(args.video_path, args.confidence)
    
    if success:
        print(f"\n🎉 Test completed successfully!")
        print(f"Check the 'cricket_detection_results' folder for processed video and results.")
    else:
        print(f"\n❌ Test failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
