import cv2
import numpy as np
import os
import json
import argparse
from enhanced_ball_tracker import EnhancedBallTracker
from typing import List, Tuple, Optional, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBallTrackerTester:
    """
    Test script for the enhanced ball tracker with video processing and analysis.
    """
    
    def __init__(self):
        self.tracker = EnhancedBallTracker()
        self.results = {
            'total_frames': 0,
            'detected_frames': 0,
            'trajectory_points': [],
            'detection_confidence': [],
            'processing_times': []
        }
    
    def process_video(self, video_path: str, output_path: str = None) -> Dict:
        """
        Process a video file and track the white ball across all frames.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output video (optional)
            
        Returns:
            Dictionary with tracking results
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
            
            # Setup output video if specified
            out = None
            if output_path:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            # Reset tracker
            self.tracker.reset_tracking()
            
            frame_count = 0
            detected_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Track ball in current frame
                ball_pos = self.tracker.detect_white_ball(frame)
                
                # Update results
                self.results['total_frames'] += 1
                if ball_pos:
                    detected_count += 1
                    self.results['trajectory_points'].append({
                        'frame': frame_count,
                        'position': ball_pos,
                        'timestamp': frame_count / fps
                    })
                
                # Visualize tracking
                annotated_frame = self.tracker.visualize_tracking(frame, ball_pos)
                
                # Add frame counter
                cv2.putText(annotated_frame, f"Frame: {frame_count}/{total_frames}", 
                           (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Write output frame
                if out:
                    out.write(annotated_frame)
                
                frame_count += 1
                
                # Progress update
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames, detected: {detected_count}")
            
            # Cleanup
            cap.release()
            if out:
                out.release()
            
            # Update final results
            self.results['detected_frames'] = detected_count
            self.results['detection_rate'] = detected_count / frame_count if frame_count > 0 else 0
            
            logger.info(f"Processing complete. Detection rate: {self.results['detection_rate']:.2%}")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            return {}
    
    def process_frames_directory(self, frames_dir: str, output_dir: str = None) -> Dict:
        """
        Process a directory of frame images and track the ball.
        
        Args:
            frames_dir: Directory containing frame images
            output_dir: Directory for output images (optional)
            
        Returns:
            Dictionary with tracking results
        """
        try:
            # Get sorted list of frame files
            frame_files = [f for f in os.listdir(frames_dir) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            frame_files.sort()
            
            if not frame_files:
                raise ValueError(f"No image files found in directory: {frames_dir}")
            
            logger.info(f"Processing {len(frame_files)} frames from directory")
            
            # Create output directory if specified
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Reset tracker
            self.tracker.reset_tracking()
            
            detected_count = 0
            ball_positions = []
            
            for i, frame_file in enumerate(frame_files):
                frame_path = os.path.join(frames_dir, frame_file)
                frame = cv2.imread(frame_path)
                
                if frame is None:
                    logger.warning(f"Could not read frame: {frame_path}")
                    continue
                
                # Track ball in current frame
                ball_pos = self.tracker.detect_white_ball(frame)
                
                # Update results
                self.results['total_frames'] += 1
                if ball_pos:
                    detected_count += 1
                    ball_positions.append({
                        'frame': i,
                        'position': ball_pos,
                        'file': frame_file
                    })
                
                # Visualize tracking
                annotated_frame = self.tracker.visualize_tracking(frame, ball_pos)
                
                # Add frame counter
                cv2.putText(annotated_frame, f"Frame: {i+1}/{len(frame_files)}", 
                           (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Save output frame if output directory specified
                if output_dir:
                    output_path = os.path.join(output_dir, f"tracked_{frame_file}")
                    cv2.imwrite(output_path, annotated_frame)
                
                # Progress update
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i+1}/{len(frame_files)} frames, detected: {detected_count}")
            
            # Update final results
            self.results['detected_frames'] = detected_count
            self.results['detection_rate'] = detected_count / len(frame_files) if frame_files else 0
            self.results['ball_positions'] = ball_positions
            
            logger.info(f"Processing complete. Detection rate: {self.results['detection_rate']:.2%}")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Error processing frames directory: {str(e)}")
            return {}
    
    def analyze_trajectory(self) -> Dict:
        """
        Analyze the tracked ball trajectory for patterns and statistics.
        
        Returns:
            Dictionary with trajectory analysis
        """
        trajectory = self.tracker.get_trajectory()
        velocity_history = self.tracker.get_velocity_history()
        
        if len(trajectory) < 2:
            return {'error': 'Insufficient trajectory data'}
        
        # Calculate trajectory statistics
        positions = np.array(trajectory)
        velocities = np.array(velocity_history) if velocity_history else np.array([])
        
        analysis = {
            'total_points': len(trajectory),
            'trajectory_length': len(trajectory),
            'start_position': trajectory[0] if trajectory else None,
            'end_position': trajectory[-1] if trajectory else None,
            'average_velocity': np.mean(velocities, axis=0).tolist() if len(velocities) > 0 else None,
            'max_velocity': np.max(np.linalg.norm(velocities, axis=1)) if len(velocities) > 0 else None,
            'min_velocity': np.min(np.linalg.norm(velocities, axis=1)) if len(velocities) > 0 else None,
        }
        
        # Calculate trajectory direction
        if len(trajectory) >= 2:
            start_pos = np.array(trajectory[0])
            end_pos = np.array(trajectory[-1])
            direction = end_pos - start_pos
            analysis['direction'] = direction.tolist()
            analysis['direction_magnitude'] = np.linalg.norm(direction)
        
        return analysis
    
    def save_results(self, output_path: str):
        """Save tracking results to JSON file."""
        try:
            # Add trajectory analysis
            trajectory_analysis = self.analyze_trajectory()
            self.results['trajectory_analysis'] = trajectory_analysis
            
            # Save to file
            with open(output_path, 'w') as f:
                json.dump(self.results, f, indent=2)
            
            logger.info(f"Results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """Main function to run the enhanced ball tracker test."""
    parser = argparse.ArgumentParser(description='Test Enhanced Ball Tracker')
    parser.add_argument('--video', type=str, help='Input video file path')
    parser.add_argument('--frames-dir', type=str, help='Input frames directory path')
    parser.add_argument('--output-video', type=str, help='Output video file path')
    parser.add_argument('--output-dir', type=str, help='Output frames directory path')
    parser.add_argument('--results', type=str, default='tracking_results.json', 
                       help='Output results JSON file path')
    
    args = parser.parse_args()
    
    if not args.video and not args.frames_dir:
        print("Please provide either --video or --frames-dir argument")
        return
    
    tester = EnhancedBallTrackerTester()
    
    if args.video:
        results = tester.process_video(args.video, args.output_video)
    else:
        results = tester.process_frames_directory(args.frames_dir, args.output_dir)
    
    if results:
        tester.save_results(args.results)
        print(f"Tracking completed successfully!")
        print(f"Detection rate: {results.get('detection_rate', 0):.2%}")
        print(f"Total frames processed: {results.get('total_frames', 0)}")
        print(f"Frames with ball detected: {results.get('detected_frames', 0)}")
    else:
        print("Tracking failed!")

if __name__ == "__main__":
    main() 