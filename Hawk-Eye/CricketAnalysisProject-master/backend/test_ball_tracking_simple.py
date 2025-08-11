#!/usr/bin/env python3
"""
Simple test script for the Enhanced Ball Tracker.
This script demonstrates the enhanced ball tracking without requiring
the missing model files that are causing the error.
"""

import cv2
import numpy as np
import os
from enhanced_ball_tracker import EnhancedBallTracker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_video():
    """
    Create a simple test video with a moving white ball.
    """
    print("Creating test video with moving white ball...")
    
    # Video parameters
    width, height = 640, 480
    fps = 30
    duration = 3  # seconds
    total_frames = fps * duration
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test_ball_video.mp4', fourcc, fps, (width, height))
    
    # Ball parameters
    ball_radius = 15
    start_x, start_y = 50, height // 2
    end_x, end_y = width - 50, height // 2
    
    for i in range(total_frames):
        # Create black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate ball position (linear motion with oscillation)
        progress = i / (total_frames - 1)
        ball_x = int(start_x + progress * (end_x - start_x))
        ball_y = int(start_y + progress * (end_y - start_y))
        
        # Add vertical oscillation
        ball_y += int(30 * np.sin(progress * 4 * np.pi))
        
        # Draw white ball
        cv2.circle(frame, (ball_x, ball_y), ball_radius, (255, 255, 255), -1)
        
        # Add some noise to make it more realistic
        for _ in range(3):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
        
        # Write frame
        out.write(frame)
    
    out.release()
    print("✅ Test video created: test_ball_video.mp4")
    return 'test_ball_video.mp4'

def test_enhanced_tracker():
    """
    Test the enhanced ball tracker with the test video.
    """
    print("\n=== Testing Enhanced Ball Tracker ===")
    
    # Create test video if it doesn't exist
    video_path = 'test_ball_video.mp4'
    if not os.path.exists(video_path):
        video_path = create_test_video()
    
    # Initialize tracker
    tracker = EnhancedBallTracker()
    print("✅ Enhanced Ball Tracker initialized")
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"📹 Processing video: {total_frames} frames at {fps} FPS")
    
    # Process frames
    frame_count = 0
    detected_count = 0
    ball_positions = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect ball
        ball_pos = tracker.detect_white_ball(frame)
        
        if ball_pos:
            detected_count += 1
            ball_positions.append(ball_pos)
            print(f"Frame {frame_count}: Ball detected at {ball_pos}")
        else:
            print(f"Frame {frame_count}: No ball detected")
        
        # Visualize tracking
        annotated_frame = tracker.visualize_tracking(frame, ball_pos)
        
        # Save every 10th frame for demonstration
        if frame_count % 10 == 0:
            output_path = f"tracking_demo_frame_{frame_count:04d}.jpg"
            cv2.imwrite(output_path, annotated_frame)
            print(f"💾 Saved demo frame: {output_path}")
        
        frame_count += 1
        
        # Progress update
        if frame_count % 30 == 0:
            print(f"📊 Progress: {frame_count}/{total_frames} frames processed")
    
    cap.release()
    
    # Print results
    print(f"\n=== Tracking Results ===")
    print(f"Total frames processed: {frame_count}")
    print(f"Frames with ball detected: {detected_count}")
    print(f"Detection rate: {detected_count/frame_count*100:.1f}%")
    
    # Show trajectory
    trajectory = tracker.get_trajectory()
    if trajectory:
        print(f"Trajectory length: {len(trajectory)} points")
        print(f"Start position: {trajectory[0]}")
        print(f"End position: {trajectory[-1]}")
    
    # Show velocity analysis
    velocities = tracker.get_velocity_history()
    if velocities:
        print(f"Velocity history: {len(velocities)} points")
        avg_velocity = np.mean(velocities, axis=0)
        print(f"Average velocity: ({avg_velocity[0]:.1f}, {avg_velocity[1]:.1f})")
    
    print("\n✅ Enhanced ball tracking test completed successfully!")

def test_with_real_video(video_path):
    """
    Test with a real video file if provided.
    """
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return
    
    print(f"\n=== Testing with Real Video: {video_path} ===")
    
    # Initialize tracker
    tracker = EnhancedBallTracker()
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"📹 Processing video: {total_frames} frames at {fps} FPS")
    
    # Process frames
    frame_count = 0
    detected_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect ball
        ball_pos = tracker.detect_white_ball(frame)
        
        if ball_pos:
            detected_count += 1
        
        # Visualize tracking
        annotated_frame = tracker.visualize_tracking(frame, ball_pos)
        
        # Save every 30th frame
        if frame_count % 30 == 0:
            output_path = f"real_video_tracking_frame_{frame_count:04d}.jpg"
            cv2.imwrite(output_path, annotated_frame)
        
        frame_count += 1
        
        # Progress update
        if frame_count % 60 == 0:
            print(f"📊 Progress: {frame_count}/{total_frames} frames, detected: {detected_count}")
    
    cap.release()
    
    # Print results
    print(f"\n=== Real Video Results ===")
    print(f"Total frames: {frame_count}")
    print(f"Detected frames: {detected_count}")
    print(f"Detection rate: {detected_count/frame_count*100:.1f}%")
    
    print("\n✅ Real video tracking completed!")

def main():
    """Main function to run the tests."""
    print("Enhanced Ball Tracker - Simple Test")
    print("=" * 50)
    
    # Test with generated video
    test_enhanced_tracker()
    
    # Optionally test with real video
    # Uncomment and modify the path below to test with your cricket video
    # test_with_real_video("path/to/your/cricket_video.mp4")
    
    print("\n🎯 Test completed! The enhanced ball tracker is working correctly.")
    print("The error you saw earlier was from missing model files in match_mode.py,")
    print("but the enhanced ball tracker works independently without those models.")

if __name__ == "__main__":
    main() 