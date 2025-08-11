#!/usr/bin/env python3
"""
Simple script to run the cricket ball detection calibration tool.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ball_detection_calibrator import BallDetectionCalibrator

def main():
    """Run the ball detection calibration tool."""
    print("Starting Cricket Ball Detection Calibrator...")
    print("This tool will help you tune the detection parameters for your specific video.")
    print()
    print("Instructions:")
    print("1. Use the trackbars to adjust HSV values and detection parameters")
    print("2. Watch the real-time detection in the main window")
    print("3. Press 's' to save your tuned parameters")
    print("4. Press 'l' to load previously saved parameters")
    print("5. Press 'q' to quit")
    print()
    
    try:
        calibrator = BallDetectionCalibrator()
        
        # Try to load existing parameters if available
        calibrator.load_parameters()
        
        # Run the calibration tool
        calibrator.run_calibration()
        
    except KeyboardInterrupt:
        print("\nCalibration interrupted by user")
    except Exception as e:
        print(f"Error running calibration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 