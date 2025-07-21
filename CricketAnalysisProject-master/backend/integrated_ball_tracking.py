#!/usr/bin/env python3
"""
Integrated Ball Tracking System
Combines the enhanced ball tracker with existing infrastructure for comprehensive
white ball detection and tracking across multiple frames.
"""

import cv2
import numpy as np
import os
import json
import logging
from typing import List, Tuple, Optional, Dict, Any
from enhanced_ball_tracker import EnhancedBallTracker
from track_ball import detect_ball, track_ball_movement
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegratedBallTrackingSystem:
    """
    Integrated system that combines enhanced white ball tracking with existing
    ball detection infrastructure for robust multi-frame ball tracking.
    """
    
    def __init__(self):
        self.enhanced_tracker = EnhancedBallTracker()
        self.tracking_results = {
            'enhanced_detections': [],
            'traditional_detections': [],
            'combined_detections': [],
            'trajectory_analysis': {},
            'performance_metrics': {}
        }
    
    def detect_ball_enhanced(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Enhanced white ball detection using the specialized tracker.
        """
        return self.enhanced_tracker.detect_white_ball(frame)
    
    def detect_ball_traditional(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Traditional ball detection using existing infrastructure.
        """
        return detect_ball(frame)
    
    def combine_detections(self, enhanced_pos: Optional[Tuple[int, int]], 
                          traditional_pos: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Combine detections from both methods for improved accuracy.
        """
        if enhanced_pos and traditional_pos:
            # Both detected - use enhanced if they're close, otherwise enhanced
            distance = np.sqrt((enhanced_pos[0] - traditional_pos[0])**2 + 
                             (enhanced_pos[1] - traditional_pos[1])**2)
            if distance < 50:  # Close detections - use enhanced
                return enhanced_pos
            else:  # Far apart - prefer enhanced for white balls
                return enhanced_pos
        elif enhanced_pos:
            return enhanced_pos
        elif traditional_pos:
            return traditional_pos
        else:
            return None
    
    def process_video_frame_by_frame(self, video_path: str, output_path: str = None) -> Dict:
        """
        Process video frame by frame using both detection methods.
        
        Args:
            video_path: Path to input video
            output_path: Path for output video (optional)
            
        Returns:
            Dictionary with comprehensive tracking results
        """
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Processing video: {width}x{height}, {fps} FPS, {total_frames} frames")
            
            # Setup output video
            out = None
            if output_path:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Reset trackers
            self.enhanced_tracker.reset_tracking()
            
            frame_count = 0
            enhanced_detections = 0
            traditional_detections = 0
            combined_detections = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect ball using both methods
                enhanced_pos = self.detect_ball_enhanced(frame)
                traditional_pos = self.detect_ball_traditional(frame)
                combined_pos = self.combine_detections(enhanced_pos, traditional_pos)
                
                # Update detection counts
                if enhanced_pos:
                    enhanced_detections += 1
                    self.tracking_results['enhanced_detections'].append({
                        'frame': frame_count,
                        'position': enhanced_pos,
                        'timestamp': frame_count / fps
                    })
                
                if traditional_pos:
                    traditional_detections += 1
                    self.tracking_results['traditional_detections'].append({
                        'frame': frame_count,
                        'position': traditional_pos,
                        'timestamp': frame_count / fps
                    })
                
                if combined_pos:
                    combined_detections += 1
                    self.tracking_results['combined_detections'].append({
                        'frame': frame_count,
                        'position': combined_pos,
                        'timestamp': frame_count / fps
                    })
                
                # Create visualization
                annotated_frame = self._create_comprehensive_visualization(
                    frame, enhanced_pos, traditional_pos, combined_pos
                )
                
                # Add frame counter
                cv2.putText(annotated_frame, f"Frame: {frame_count}/{total_frames}", 
                           (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Write output frame
                if out:
                    out.write(annotated_frame)
                
                frame_count += 1
                
                # Progress update
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")
                    logger.info(f"Enhanced: {enhanced_detections}, Traditional: {traditional_detections}, Combined: {combined_detections}")
            
            # Cleanup
            cap.release()
            if out:
                out.release()
            
            # Calculate performance metrics
            self.tracking_results['performance_metrics'] = {
                'total_frames': frame_count,
                'enhanced_detection_rate': enhanced_detections / frame_count if frame_count > 0 else 0,
                'traditional_detection_rate': traditional_detections / frame_count if frame_count > 0 else 0,
                'combined_detection_rate': combined_detections / frame_count if frame_count > 0 else 0,
                'enhanced_detections': enhanced_detections,
                'traditional_detections': traditional_detections,
                'combined_detections': combined_detections
            }
            
            # Analyze trajectory
            self.tracking_results['trajectory_analysis'] = self._analyze_trajectories()
            
            logger.info("Video processing completed successfully!")
            return self.tracking_results
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            return {}
    
    def _create_comprehensive_visualization(self, frame: np.ndarray, 
                                          enhanced_pos: Optional[Tuple[int, int]],
                                          traditional_pos: Optional[Tuple[int, int]],
                                          combined_pos: Optional[Tuple[int, int]]) -> np.ndarray:
        """
        Create comprehensive visualization showing all detection methods.
        """
        annotated_frame = frame.copy()
        
        # Draw enhanced detection (yellow)
        if enhanced_pos:
            cv2.circle(annotated_frame, enhanced_pos, 15, (0, 255, 255), 3)
            cv2.putText(annotated_frame, "Enhanced", (enhanced_pos[0] + 20, enhanced_pos[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        
        # Draw traditional detection (green)
        if traditional_pos:
            cv2.circle(annotated_frame, traditional_pos, 12, (0, 255, 0), 2)
            cv2.putText(annotated_frame, "Traditional", (traditional_pos[0] + 20, traditional_pos[1] + 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw combined detection (red)
        if combined_pos:
            cv2.circle(annotated_frame, combined_pos, 18, (0, 0, 255), 4)
            cv2.circle(annotated_frame, combined_pos, 8, (255, 255, 255), -1)
        
        # Add detection status
        status_text = f"Enhanced: {'✓' if enhanced_pos else '✗'}, Traditional: {'✓' if traditional_pos else '✗'}, Combined: {'✓' if combined_pos else '✗'}"
        cv2.putText(annotated_frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add trajectory from enhanced tracker
        trajectory = self.enhanced_tracker.get_trajectory()
        if len(trajectory) >= 2:
            for i in range(1, len(trajectory)):
                cv2.line(annotated_frame, trajectory[i-1], trajectory[i], (255, 255, 255), 2)
        
        return annotated_frame
    
    def _analyze_trajectories(self) -> Dict:
        """
        Analyze trajectories from both detection methods.
        """
        enhanced_trajectory = self.enhanced_tracker.get_trajectory()
        enhanced_velocities = self.enhanced_tracker.get_velocity_history()
        
        analysis = {
            'enhanced_trajectory_length': len(enhanced_trajectory),
            'enhanced_velocity_points': len(enhanced_velocities),
            'enhanced_start_position': enhanced_trajectory[0] if enhanced_trajectory else None,
            'enhanced_end_position': enhanced_trajectory[-1] if enhanced_trajectory else None,
        }
        
        if enhanced_velocities:
            velocities = np.array(enhanced_velocities)
            analysis['enhanced_average_velocity'] = np.mean(velocities, axis=0).tolist()
            analysis['enhanced_max_velocity'] = float(np.max(np.linalg.norm(velocities, axis=1)))
            analysis['enhanced_min_velocity'] = float(np.min(np.linalg.norm(velocities, axis=1)))
        
        return analysis
    
    def save_results(self, output_path: str):
        """Save comprehensive tracking results to JSON file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.tracking_results, f, indent=2)
            logger.info(f"Results saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """Main function to run the integrated ball tracking system."""
    parser = argparse.ArgumentParser(description='Integrated Ball Tracking System')
    parser.add_argument('--video', type=str, required=True, help='Input video file path')
    parser.add_argument('--output', type=str, help='Output video file path')
    parser.add_argument('--results', type=str, default='integrated_tracking_results.json',
                       help='Output results JSON file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video):
        print(f"Video file not found: {args.video}")
        return
    
    # Initialize integrated system
    system = IntegratedBallTrackingSystem()
    
    # Process video
    print(f"Processing video: {args.video}")
    results = system.process_video_frame_by_frame(args.video, args.output)
    
    if results:
        # Save results
        system.save_results(args.results)
        
        # Print summary
        metrics = results.get('performance_metrics', {})
        print("\n=== Tracking Results Summary ===")
        print(f"Total frames processed: {metrics.get('total_frames', 0)}")
        print(f"Enhanced detection rate: {metrics.get('enhanced_detection_rate', 0):.2%}")
        print(f"Traditional detection rate: {metrics.get('traditional_detection_rate', 0):.2%}")
        print(f"Combined detection rate: {metrics.get('combined_detection_rate', 0):.2%}")
        print(f"Enhanced detections: {metrics.get('enhanced_detections', 0)}")
        print(f"Traditional detections: {metrics.get('traditional_detections', 0)}")
        print(f"Combined detections: {metrics.get('combined_detections', 0)}")
        
        # Trajectory analysis
        trajectory_analysis = results.get('trajectory_analysis', {})
        if trajectory_analysis.get('enhanced_trajectory_length', 0) > 0:
            print(f"\nEnhanced trajectory length: {trajectory_analysis['enhanced_trajectory_length']}")
            print(f"Start position: {trajectory_analysis.get('enhanced_start_position')}")
            print(f"End position: {trajectory_analysis.get('enhanced_end_position')}")
        
        print("\nProcessing completed successfully!")
    else:
        print("Processing failed!")

if __name__ == "__main__":
    main() 