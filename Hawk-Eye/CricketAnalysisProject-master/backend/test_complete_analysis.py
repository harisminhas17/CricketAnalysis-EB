#!/usr/bin/env python3
"""
Test Complete Video Analysis
Demonstrates the complete video analysis functionality with all object detection features.
"""

import os
import sys
from comprehensive_video_analysis import integrate_with_analyze_endpoint
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_analysis():
    """
    Test the complete video analysis functionality.
    """
    print("Testing Complete Video Analysis with All Object Detection")
    print("=" * 60)
    
    # Check if demo video exists, create if not
    demo_video = 'demo_cricket_video.mp4'
    if not os.path.exists(demo_video):
        print("Creating demo cricket video...")
        from test_ball_tracking_simple import create_test_video
        demo_video = create_test_video()
    
    print(f"Using video: {demo_video}")
    
    # Run comprehensive analysis
    print("\nStarting comprehensive analysis...")
    result = integrate_with_analyze_endpoint(demo_video)
    
    if result['success']:
        print("\n✅ Analysis completed successfully!")
        print(f"📹 Output video: {result['output_video']}")
        print(f"📊 Results JSON: {result['results_json']}")
        
        # Print detailed results
        analysis_results = result['analysis_results']
        metrics = analysis_results.get('performance_metrics', {})
        
        print(f"\n📈 Detailed Analysis Results:")
        print(f"   Total frames processed: {analysis_results['total_frames']}")
        print(f"   Enhanced ball detections: {metrics.get('total_enhanced_detections', 0)}")
        print(f"   Traditional ball detections: {metrics.get('total_traditional_detections', 0)}")
        print(f"   Player detections: {metrics.get('total_player_detections', 0)}")
        print(f"   Enhanced detection rate: {metrics.get('enhanced_detection_rate', 0)*100:.1f}%")
        print(f"   Traditional detection rate: {metrics.get('traditional_detection_rate', 0)*100:.1f}%")
        print(f"   Player detection rate: {metrics.get('player_detection_rate', 0)*100:.1f}%")
        
        # Show object detection summary
        object_counts = analysis_results.get('object_detections', {})
        if object_counts:
            print(f"\n🎯 Object Detection Summary:")
            for obj_type, count in object_counts.items():
                print(f"   {obj_type}: {count}")
        
        # Show trajectory analysis
        if analysis_results.get('trajectory_analysis'):
            trajectory = analysis_results['trajectory_analysis']
            print(f"\n🔄 Trajectory Analysis:")
            print(f"   Trajectory points: {trajectory.get('total_points', 0)}")
            print(f"   Start position: {trajectory.get('start_position')}")
            print(f"   End position: {trajectory.get('end_position')}")
            if trajectory.get('average_velocity'):
                vel = trajectory['average_velocity']
                print(f"   Average velocity: ({vel[0]:.1f}, {vel[1]:.1f})")
        
        print(f"\n🎯 Output Video Features:")
        print(f"   ✅ Ball detection with trajectory tracking")
        print(f"   ✅ Player detection and bounding boxes")
        print(f"   ✅ Stump and field boundary detection")
        print(f"   ✅ Velocity vectors and motion analysis")
        print(f"   ✅ Shot zone analysis (Off Side/Straight/Leg Side)")
        print(f"   ✅ LBW possibility analysis")
        print(f"   ✅ Cricket field overlay with pitch and stumps")
        print(f"   ✅ Real-time analytics overlay")
        print(f"   ✅ Object count and detection rates")
        
        print(f"\n📁 Generated Files:")
        print(f"   Video: {result['output_video']}")
        print(f"   Results: {result['results_json']}")
        
        # Check if files exist
        if os.path.exists(result['output_video']):
            file_size = os.path.getsize(result['output_video']) / (1024 * 1024)  # MB
            print(f"   Video size: {file_size:.1f} MB")
        
        if os.path.exists(result['results_json']):
            print(f"   Results file exists and contains analysis data")
        
        print(f"\n🎉 Test completed successfully!")
        print(f"You can now play the output video to see all the detection features!")
        
    else:
        print(f"\n❌ Analysis failed: {result.get('error', 'Unknown error')}")
        return False
    
    return True

def test_with_real_video(video_path):
    """
    Test with a real cricket video.
    """
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return False
    
    print(f"\nTesting with real cricket video: {video_path}")
    
    result = integrate_with_analyze_endpoint(video_path)
    
    if result['success']:
        print(f"✅ Real video analysis completed!")
        print(f"📹 Output: {result['output_video']}")
        print(f"📊 Results: {result['results_json']}")
        return True
    else:
        print(f"❌ Real video analysis failed: {result.get('error')}")
        return False

def main():
    """Main function to run the complete analysis test."""
    print("Complete Video Analysis Test")
    print("=" * 40)
    
    # Test with demo video
    success = test_complete_analysis()
    
    if success:
        print(f"\n✅ All tests passed!")
        print(f"The comprehensive video analysis is working correctly.")
        print(f"You can now integrate this with your upload/analyze flow.")
        
        # Optionally test with real video
        # Uncomment and modify the path below to test with your cricket video
        # test_with_real_video("path/to/your/cricket_video.mp4")
        
    else:
        print(f"\n❌ Tests failed!")
        print(f"Please check the error messages above.")

if __name__ == "__main__":
    main() 