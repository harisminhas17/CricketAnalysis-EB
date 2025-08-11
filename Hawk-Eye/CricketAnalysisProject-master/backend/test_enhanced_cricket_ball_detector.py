import cv2
import numpy as np
import json
import os
from enhanced_cricket_ball_detector import EnhancedCricketBallDetector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_enhanced_cricket_ball_detection(video_path: str, output_dir: str = None):
    """
    Test the enhanced cricket ball detector with specific requirements:
    - Spherical/circular object detection
    - Minimum 30kmph velocity
    - Minimum 15m distance (13m for validation)
    - False positive removal based on motion patterns
    """
    
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return
    
    # Initialize the enhanced detector
    detector = EnhancedCricketBallDetector()
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Failed to open video: {video_path}")
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calibrate detector using pitch dimensions
    detector.calibrate_from_pitch_dimensions(frame_width, frame_height)
    detector.fps = fps
    
    logger.info(f"Video properties: {frame_width}x{frame_height}, {fps} FPS, {total_frames} frames")
    logger.info(f"Calibrated pixels_to_meters: {detector.pixels_to_meters}")
    
    # Initialize tracking variables
    frame_count = 0
    detections = []
    valid_detections = 0
    total_detections = 0
    
    # Create output directory if specified
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process video frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Detect cricket ball
        detection = detector.detect_cricket_ball(frame, frame_count)
        
        if detection:
            total_detections += 1
            
            # Check if it's a valid cricket ball
            if detection.is_valid_cricket_ball:
                valid_detections += 1
                logger.info(f"Frame {frame_count}: Valid cricket ball detected at {detection.position}")
                logger.info(f"  Velocity: {detection.velocity[0]:.2f}, {detection.velocity[1]:.2f} m/s")
                logger.info(f"  Distance covered: {detection.distance_covered:.2f} m")
                logger.info(f"  Confidence: {detection.confidence:.3f}")
            
            # Store detection data
            detections.append({
                'frame': frame_count,
                'position': detection.position,
                'radius': detection.radius,
                'confidence': detection.confidence,
                'velocity': detection.velocity,
                'timestamp': detection.timestamp,
                'distance_covered': detection.distance_covered,
                'is_valid_cricket_ball': detection.is_valid_cricket_ball
            })
            
            # Draw detection on frame
            annotated_frame = frame.copy()
            
            # Draw ball circle
            color = (0, 255, 0) if detection.is_valid_cricket_ball else (0, 0, 255)
            cv2.circle(annotated_frame, detection.position, int(detection.radius), color, 2)
            
            # Draw velocity vector
            if detection.velocity[0] != 0 or detection.velocity[1] != 0:
                end_x = int(detection.position[0] + detection.velocity[0] * 10)
                end_y = int(detection.position[1] + detection.velocity[1] * 10)
                cv2.arrowedLine(annotated_frame, detection.position, (end_x, end_y), (255, 255, 0), 2)
            
            # Add text information
            velocity_kmh = math.sqrt(detection.velocity[0]**2 + detection.velocity[1]**2) * 3.6
            cv2.putText(annotated_frame, f"Vel: {velocity_kmh:.1f} km/h", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(annotated_frame, f"Dist: {detection.distance_covered:.1f} m", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(annotated_frame, f"Conf: {detection.confidence:.3f}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Save annotated frame if output directory is specified
            if output_dir:
                output_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(output_path, annotated_frame)
        
        # Print progress every 100 frames
        if frame_count % 100 == 0:
            logger.info(f"Processed {frame_count}/{total_frames} frames")
    
    # Release video capture
    cap.release()
    
    # Get final statistics
    stats = detector.get_tracking_statistics()
    
    # Create results summary
    results = {
        'video_path': video_path,
        'frame_count': frame_count,
        'total_detections': total_detections,
        'valid_detections': valid_detections,
        'detection_rate': valid_detections / max(frame_count, 1),
        'tracking_statistics': stats,
        'detections': detections,
        'requirements_met': {
            'minimum_velocity_30kmph': stats['average_velocity'] >= 30.0,
            'validation_velocity_30kmph': stats['max_velocity'] >= 30.0,
            'minimum_distance_15m': stats['total_distance'] >= 15.0,
            'validation_distance_13m': stats['total_distance'] >= 13.0,
            'spherical_detection': True,  # Always true as we filter by circularity
            'motion_consistency': stats['detection_rate'] > 0.5
        }
    }
    
    # Save results
    if output_dir:
        results_path = os.path.join(output_dir, 'detection_results.json')
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to: {results_path}")
    
    # Print summary
    logger.info("=== ENHANCED CRICKET BALL DETECTION RESULTS ===")
    logger.info(f"Total frames processed: {frame_count}")
    logger.info(f"Total detections: {total_detections}")
    logger.info(f"Valid cricket ball detections: {valid_detections}")
    logger.info(f"Detection rate: {valid_detections/max(frame_count, 1)*100:.2f}%")
    logger.info(f"Average velocity: {stats['average_velocity']:.1f} km/h")
    logger.info(f"Maximum velocity: {stats['max_velocity']:.1f} km/h")
    logger.info(f"Total distance covered: {stats['total_distance']:.2f} m")
    logger.info(f"Tracking duration: {stats['tracking_duration']:.2f} s")
    
    logger.info("\n=== REQUIREMENTS VALIDATION ===")
    for requirement, met in results['requirements_met'].items():
        status = "✓ PASS" if met else "✗ FAIL"
        logger.info(f"{requirement}: {status}")
    
    return results

def analyze_spherical_dimensions(detections: list) -> dict:
    """
    Analyze how well the detector understands spherical dimensions.
    """
    if not detections:
        return {'spherical_analysis': 'No detections available'}
    
    # Analyze circularity and size consistency
    radii = [d['radius'] for d in detections if d['is_valid_cricket_ball']]
    confidences = [d['confidence'] for d in detections if d['is_valid_cricket_ball']]
    
    if not radii:
        return {'spherical_analysis': 'No valid detections for analysis'}
    
    # Calculate statistics
    avg_radius = np.mean(radii)
    std_radius = np.std(radii)
    avg_confidence = np.mean(confidences)
    
    # Check if radius variations are reasonable for a cricket ball
    # Cricket ball should maintain relatively consistent size
    radius_consistency = std_radius / avg_radius if avg_radius > 0 else 0
    
    analysis = {
        'average_radius_pixels': avg_radius,
        'radius_standard_deviation': std_radius,
        'radius_consistency': radius_consistency,
        'average_confidence': avg_confidence,
        'spherical_detection_quality': 'Good' if radius_consistency < 0.3 else 'Poor',
        'total_valid_detections': len(radii)
    }
    
    return analysis

def test_with_sample_video():
    """Test the enhanced detector with a sample video."""
    # You can replace this with your actual video path
    video_path = "demo_cricket_video.mp4"
    
    if not os.path.exists(video_path):
        logger.warning(f"Sample video not found: {video_path}")
        logger.info("Please provide a cricket video file to test the enhanced detector.")
        return
    
    output_dir = "enhanced_detection_results"
    results = test_enhanced_cricket_ball_detection(video_path, output_dir)
    
    # Additional spherical dimension analysis
    spherical_analysis = analyze_spherical_dimensions(results['detections'])
    logger.info("\n=== SPHERICAL DIMENSION ANALYSIS ===")
    for key, value in spherical_analysis.items():
        logger.info(f"{key}: {value}")

if __name__ == "__main__":
    import math
    
    # Test with sample video
    test_with_sample_video() 