import cv2
import os
import logging
from ultralytics import YOLO
from track_ball import real_time_ball_tracking, reset_real_time_tracking, get_real_time_trajectory
import json
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def extract_frames(video_path, output_dir, every_n_frames=1):
    """
    Extract frames from a video file.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory to save extracted frames
        every_n_frames (int): Extract every nth frame
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Could not open video file")
        
        frame_count = 0
        saved_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % every_n_frames == 0:
                # Save frame
                frame_path = os.path.join(output_dir, f'frame_{saved_count:04d}.jpg')
                cv2.imwrite(frame_path, frame)
                saved_count += 1
                
            frame_count += 1
            
        cap.release()
        logger.info(f"Extracted {saved_count} frames from video")
        
    except Exception as e:
        logger.error(f"Error extracting frames: {str(e)}")
        raise

def detect_objects_in_frames(frames_dir, output_dir):
    """
    Detect objects in frames using YOLO model.
    
    Args:
        frames_dir (str): Directory containing input frames
        output_dir (str): Directory to save annotated frames
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load YOLO model
        model = YOLO('yolov8n.pt')
        
        # Process each frame
        for filename in os.listdir(frames_dir):
            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            # Read frame
            frame_path = os.path.join(frames_dir, filename)
            frame = cv2.imread(frame_path)
            
            # Run detection
            results = model(frame, conf=0.15)
            
            # Draw detections
            annotated_frame = results[0].plot()
            
            # Save annotated frame
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, annotated_frame)
            
        logger.info(f"Processed frames in {frames_dir}")
        
    except Exception as e:
        logger.error(f"Error detecting objects: {str(e)}")
        raise

def analyze_video_real_time(video_path: str, output_dir: str) -> Dict[str, Any]:
    """
    Real-time video analysis with immediate ball tracking and trajectory visualization.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory to save analysis results
        
    Returns:
        Dict containing analysis results and trajectory data
    """
    try:
        # Reset tracking state
        reset_real_time_tracking()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Could not open video file")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Processing video: {fps} FPS, {total_frames} frames, {width}x{height}")
        
        # Prepare output video writer
        output_video_path = os.path.join(output_dir, 'real_time_tracking.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        
        frame_count = 0
        tracking_started = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame with real-time tracking
            ball_pos, annotated_frame = real_time_ball_tracking(frame)
            
            # Check if tracking has started
            if ball_pos is not None and not tracking_started:
                tracking_started = True
                logger.info(f"Ball tracking started at frame {frame_count}")
            
            # Write frame to output video
            out.write(annotated_frame)
            
            # Progress update every 100 frames
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                logger.info(f"Processing: {progress:.1f}% complete")
            
            frame_count += 1
        
        # Cleanup
        cap.release()
        out.release()
        
        # Get final trajectory data
        trajectory_data = get_real_time_trajectory()
        
        # Save trajectory data
        trajectory_path = os.path.join(output_dir, 'trajectory_data.json')
        with open(trajectory_path, 'w') as f:
            json.dump({
                'trajectory': trajectory_data,
                'total_frames': frame_count,
                'tracking_frames': len(trajectory_data),
                'video_info': {
                    'fps': fps,
                    'width': width,
                    'height': height,
                    'duration': frame_count / fps
                }
            }, f, indent=2)
        
        # Calculate analysis metrics
        analysis_results = {
            'video_path': video_path,
            'output_video': output_video_path,
            'trajectory_data': trajectory_path,
            'total_frames_processed': frame_count,
            'frames_with_ball': len(trajectory_data),
            'tracking_efficiency': len(trajectory_data) / frame_count if frame_count > 0 else 0,
            'ball_positions': [pos['position'] for pos in trajectory_data],
            'timestamps': [pos['timestamp'] for pos in trajectory_data]
        }
        
        logger.info(f"Real-time analysis completed. Trajectory points: {len(trajectory_data)}")
        return analysis_results
        
    except Exception as e:
        logger.error(f"Error in real-time video analysis: {str(e)}")
        raise
