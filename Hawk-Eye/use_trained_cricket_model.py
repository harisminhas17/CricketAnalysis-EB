import cv2
import torch
from pathlib import Path
from ultralytics import YOLO
import argparse
import os

def use_trained_model(video_path, confidence=0.5, model_type='best'):
    """
    Use trained cricket model to detect balls and bats in video
    """
    print("=== Using Trained Cricket Model ===")
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        return False
    
    print(f"✓ Video found: {video_path}")
    
    # Path to trained models
    trained_model_dir = Path('CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/results')
    
    if model_type == 'best':
        model_path = trained_model_dir / 'best.pt'
    elif model_type == 'last':
        model_path = trained_model_dir / 'last.pt'
    else:
        print(f"❌ Error: Invalid model type. Use 'best' or 'last'")
        return False
    
    # Check if trained model exists
    if not model_path.exists():
        print(f"❌ Error: Trained model not found at {model_path}")
        print("Please make sure you have trained the model first")
        return False
    
    print(f"✓ Found trained model: {model_path}")
    print(f"   Model type: {model_type}")
    
    # Load the trained model
    try:
        model = YOLO(str(model_path))
        print("✓ Trained model loaded successfully")
        print(f"   Model classes: {model.names}")
    except Exception as e:
        print(f"❌ Error loading trained model: {e}")
        return False
    
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
    
    # Run detection with trained model
    print(f"\n🔍 Running trained model detection...")
    print("This may take a few minutes depending on video length...")
    
    try:
        # Run inference
        results = model(
            video_path,
            conf=confidence,
            save=True,
            project='trained_cricket_results',
            name=f'{model_type}_model',
            verbose=True
        )
        
        print(f"\n✅ Detection completed with trained model!")
        
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
        output_path = f"trained_cricket_results/{model_type}_model/"
        print(f"\n📁 Results saved in: {output_path}")
        print(f"  - Processed video with detection boxes")
        print(f"  - Detection data and statistics")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Use trained cricket model for detection')
    parser.add_argument('video_path', help='Path to cricket video file')
    parser.add_argument('--confidence', '-c', type=float, default=0.5, 
                       help='Confidence threshold (0.1-0.9, default: 0.5)')
    parser.add_argument('--model', '-m', choices=['best', 'last'], default='best',
                       help='Which trained model to use (best or last, default: best)')
    
    args = parser.parse_args()
    
    # Validate confidence
    if args.confidence < 0.1 or args.confidence > 0.9:
        print("❌ Error: Confidence must be between 0.1 and 0.9")
        return
    
    # Run detection with trained model
    success = use_trained_model(args.video_path, args.confidence, args.model)
    
    if success:
        print(f"\n🎉 Trained model detection completed successfully!")
        print(f"Check the 'trained_cricket_results' folder for processed video and results.")
        print(f"\n💡 You used the '{args.model}' model with confidence {args.confidence}")
    else:
        print(f"\n❌ Detection failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
