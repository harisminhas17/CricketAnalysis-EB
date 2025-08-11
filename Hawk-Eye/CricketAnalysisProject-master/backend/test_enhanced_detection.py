#!/usr/bin/env python3
"""
Test script for enhanced cricket ball detection system.
This script helps verify that the enhanced detection is working properly.
"""

import os
import sys
import cv2
import numpy as np
from track_ball import detect_ball, preprocess_frame, create_ball_color_masks
import argparse

def test_enhanced_detection(video_path, output_dir=None):
    """
    Test the enhanced ball detection on a video file.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory to save test results (optional)
    """
    
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found")
        return
    
    print(f"Testing enhanced ball detection on: {video_path}")
    
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory: {output_dir}")
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    total_frames = int(cap.get(cv2.COLOR_BGR2HSV))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video info: {total_frames} frames, {fps} FPS, {width}x{height}")
    
    # Test parameters
    test_frames = min(100, total_frames)  # Test first 100 frames or all frames if less
    detections = 0
    frame_count = 0
    
    print(f"\nTesting {test_frames} frames...")
    print("-" * 50)
    
    while frame_count < test_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Test enhanced ball detection
        ball_pos = detect_ball(frame)
        
        if ball_pos:
            detections += 1
            print(f"Frame {frame_count}: Ball detected at {ball_pos}")
            
            # Save frame with detection if output directory specified
            if output_dir:
                # Draw ball position on frame
                annotated_frame = frame.copy()
                cv2.circle(annotated_frame, ball_pos, 15, (0, 0, 255), 3)
                cv2.putText(annotated_frame, f'Ball: {ball_pos}', (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(annotated_frame, f'Frame: {frame_count}', (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Save annotated frame
                output_path = os.path.join(output_dir, f'detection_frame_{frame_count:04d}.jpg')
                cv2.imwrite(output_path, annotated_frame)
        else:
            print(f"Frame {frame_count}: No ball detected")
        
        frame_count += 1
        
        # Progress indicator
        if frame_count % 10 == 0:
            print(f"Progress: {frame_count}/{test_frames} frames processed")
    
    cap.release()
    
    # Print results
    print("-" * 50)
    print(f"Test completed!")
    print(f"Frames tested: {frame_count}")
    print(f"Detections: {detections}")
    print(f"Detection rate: {(detections/frame_count)*100:.1f}%")
    
    if output_dir:
        print(f"Annotated frames saved to: {output_dir}")
    
    return detections, frame_count

def test_color_masks(image_path):
    """
    Test the color mask creation on a single image.
    
    Args:
        image_path (str): Path to the test image
    """
    
    if not os.path.exists(image_path):
        print(f"Error: Image file {image_path} not found")
        return
    
    print(f"Testing color masks on: {image_path}")
    
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    # Test preprocessing
    processed = preprocess_frame(image)
    print("✓ Preprocessing completed")
    
    # Test color mask creation
    hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
    ball_mask, red_mask, white_mask = create_ball_color_masks(hsv)
    print("✓ Color masks created")
    
    # Save test results
    output_dir = "test_color_masks"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save masks
    cv2.imwrite(os.path.join(output_dir, "original.jpg"), image)
    cv2.imwrite(os.path.join(output_dir, "processed.jpg"), processed)
    cv2.imwrite(os.path.join(output_dir, "ball_mask.jpg"), ball_mask)
    cv2.imwrite(os.path.join(output_dir, "red_mask.jpg"), red_mask)
    cv2.imwrite(os.path.join(output_dir, "white_mask.jpg"), white_mask)
    
    print(f"Test results saved to: {output_dir}")
    print("✓ Color mask test completed")

def main():
    """Main function to run tests."""
    
    parser = argparse.ArgumentParser(description='Test enhanced cricket ball detection')
    parser.add_argument('--video', type=str, help='Path to video file for testing')
    parser.add_argument('--image', type=str, help='Path to image file for color mask testing')
    parser.add_argument('--output', type=str, help='Output directory for test results')
    
    args = parser.parse_args()
    
    if not args.video and not args.image:
        print("Please provide either --video or --image argument")
        print("Example usage:")
        print("  python test_enhanced_detection.py --video cricket_video.mp4 --output test_results")
        print("  python test_enhanced_detection.py --image test_frame.jpg")
        return
    
    if args.video:
        test_enhanced_detection(args.video, args.output)
    
    if args.image:
        test_color_masks(args.image)

if __name__ == "__main__":
    main() 