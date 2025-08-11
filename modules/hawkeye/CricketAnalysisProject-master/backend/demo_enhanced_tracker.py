#!/usr/bin/env python3
"""
Demonstration script for the Enhanced Ball Tracker.
This script shows how to use the enhanced ball tracker to detect and track
white circular balls across multiple frames.
"""

import cv2
import numpy as np
import os
from enhanced_ball_tracker import EnhancedBallTracker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_frames():
    """
    Create test frames with a moving white ball for demonstration.
    Returns a list of frames with a white ball moving across the image.
    """
    frames = []
    width, height = 640, 480
    
    # Create a white ball that moves across the frame
    ball_radius = 15
    start_x, start_y = 50, height // 2
    end_x, end_y = width - 50, height // 2
    
    num_frames = 30
    for i in range(num_frames):
        # Create black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate ball position (linear motion)
        progress = i / (num_frames - 1)
        ball_x = int(start_x + progress * (end_x - start_x))
        ball_y = int(start_y + progress * (end_y - start_y))
        
        # Add some vertical oscillation
        ball_y += int(20 * np.sin(progress * 2 * np.pi))
        
        # Draw white ball
        cv2.circle(frame, (ball_x, ball_y), ball_radius, (255, 255, 255), -1)
        
        # Add some noise and background elements to make it more realistic
        # Add some random white spots (noise)
        for _ in range(5):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            cv2.circle(frame, (x, y), 3, (255, 255, 255), -1)
        
        frames.append(frame)
    
    return frames

def demonstrate_tracking():
    """
    Demonstrate the enhanced ball tracker with test frames.
    """
    print("=== Enhanced Ball Tracker Demonstration ===")
    
    # Create test frames
    print("Creating test frames with moving white ball...")
    frames = create_test_frames()
    print(f"Created {len(frames)} test frames")
    
    # Initialize tracker
    tracker = EnhancedBallTracker()
    print("Initialized Enhanced Ball Tracker")
    
    # Process frames
    print("\nProcessing frames and tracking ball...")
    ball_positions = []
    
    for i, frame in enumerate(frames):
        # Detect ball in current frame
        ball_pos = tracker.detect_white_ball(frame)
        
        if ball_pos:
            ball_positions.append(ball_pos)
            print(f"Frame {i+1}: Ball detected at {ball_pos}")
        else:
            print(f"Frame {i+1}: No ball detected")
        
        # Visualize tracking
        annotated_frame = tracker.visualize_tracking(frame, ball_pos)
        
        # Display frame (optional - comment out if no display available)
        # cv2.imshow('Ball Tracking', annotated_frame)
        # cv2.waitKey(100)  # 100ms delay
    
    # Print results
    print(f"\n=== Tracking Results ===")
    print(f"Total frames processed: {len(frames)}")
    print(f"Frames with ball detected: {len(ball_positions)}")
    print(f"Detection rate: {len(ball_positions)/len(frames)*100:.1f}%")
    
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
    
    print("\n=== Demonstration Complete ===")

def demonstrate_with_real_video(video_path):
    """
    Demonstrate tracking with a real video file.
    
    Args:
        video_path: Path to video file
    """
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    print(f"=== Processing Real Video: {video_path} ===")
    
    # Initialize tracker
    tracker = EnhancedBallTracker()
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Could not open video file: {video_path}")
        return
    
    frame_count = 0
    detected_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Track ball
        ball_pos = tracker.detect_white_ball(frame)
        
        if ball_pos:
            detected_count += 1
        
        # Visualize
        annotated_frame = tracker.visualize_tracking(frame, ball_pos)
        
        # Display (optional)
        # cv2.imshow('Real Video Tracking', annotated_frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        
        frame_count += 1
        
        # Progress update
        if frame_count % 30 == 0:
            print(f"Processed {frame_count} frames, detected: {detected_count}")
    
    cap.release()
    # cv2.destroyAllWindows()
    
    print(f"\n=== Real Video Results ===")
    print(f"Total frames: {frame_count}")
    print(f"Detected frames: {detected_count}")
    print(f"Detection rate: {detected_count/frame_count*100:.1f}%")

def main():
    """Main function to run demonstrations."""
    print("Enhanced Ball Tracker - Demonstration Script")
    print("=" * 50)
    
    # Run demonstration with test frames
    demonstrate_tracking()
    
    # Optionally run with real video if provided
    # Uncomment and modify the path below to test with a real video
    # demonstrate_with_real_video("path/to/your/video.mp4")

if __name__ == "__main__":
    main() 