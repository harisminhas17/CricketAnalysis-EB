#!/usr/bin/env python3
"""
Simple example demonstrating how to use the Enhanced Ball Tracker
for detecting white circular balls across multiple frames.
"""

import cv2
import numpy as np
from enhanced_ball_tracker import EnhancedBallTracker

def main():
    """
    Simple example showing how to use the enhanced ball tracker.
    """
    print("Enhanced Ball Tracker - Example Usage")
    print("=" * 40)
    
    # Initialize the enhanced ball tracker
    tracker = EnhancedBallTracker()
    print("✓ Enhanced Ball Tracker initialized")
    
    # Create a simple test frame with a white ball
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Draw a white ball in the center
    center_x, center_y = 320, 240
    cv2.circle(frame, (center_x, center_y), 20, (255, 255, 255), -1)
    
    print("✓ Created test frame with white ball")
    
    # Detect the ball in the frame
    ball_position = tracker.detect_white_ball(frame)
    
    if ball_position:
        print(f"✓ Ball detected at position: {ball_position}")
        
        # Visualize the detection
        annotated_frame = tracker.visualize_tracking(frame, ball_position)
        
        # Save the result
        cv2.imwrite('ball_detection_example.jpg', annotated_frame)
        print("✓ Saved annotated frame to 'ball_detection_example.jpg'")
        
        # Show trajectory information
        trajectory = tracker.get_trajectory()
        print(f"✓ Trajectory length: {len(trajectory)} points")
        
    else:
        print("✗ No ball detected in the frame")
    
    print("\nExample completed successfully!")
    print("\nTo use with your own video:")
    print("1. Import EnhancedBallTracker")
    print("2. Initialize tracker = EnhancedBallTracker()")
    print("3. For each frame: ball_pos = tracker.detect_white_ball(frame)")
    print("4. Get trajectory: trajectory = tracker.get_trajectory()")

if __name__ == "__main__":
    main() 