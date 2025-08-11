import cv2
import os
import logging
from typing import Tuple, Optional
import tempfile
import shutil
import subprocess

logger = logging.getLogger(__name__)

class VideoTrimmer:
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        
    def trim_video(self, input_path: str, start_time: float, end_time: float, 
                   output_path: Optional[str] = None) -> str:
        """
        Trim a video file using FFmpeg for browser compatibility.
        
        Args:
            input_path (str): Path to input video file
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            output_path (str, optional): Path for output file. If None, creates temp file.
            
        Returns:
            str: Path to the trimmed video file
        """
        try:
            # Validate input file
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input video file not found: {input_path}")
                
            # Validate time range
            if start_time < 0 or end_time <= start_time:
                raise ValueError("Invalid time range")
                
            # Create output path if not provided
            if output_path is None:
                temp_dir = tempfile.mkdtemp()
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(temp_dir, f"trimmed_{name}_{start_time:.1f}_{end_time:.1f}.mp4")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Use FFmpeg to trim and re-encode for browser compatibility
            # -ss before -i for fast seek, -to for end time, re-encode to H.264/AAC
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-ss', str(start_time),
                '-to', str(end_time),
                '-i', input_path,
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-strict', 'experimental',
                '-movflags', '+faststart',
                output_path
            ]
            logger.info(f"Running FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr.decode('utf-8')}")
                raise RuntimeError(f"FFmpeg failed: {result.stderr.decode('utf-8')}")

            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise RuntimeError(f"Trimmed video file not created: {output_path}")

            logger.info(f"Video trimmed successfully with FFmpeg: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error trimming video: {str(e)}")
            raise
            
    def get_video_info(self, video_path: str) -> dict:
        """
        Get video information including duration, fps, dimensions.
        
        Args:
            video_path (str): Path to video file
            
        Returns:
            dict: Video information
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
                
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps
            
            cap.release()
            
            return {
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': total_frames,
                'duration': duration,
                'format': os.path.splitext(video_path)[1].lower()
            }
            
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            raise
            
    def validate_video(self, video_path: str) -> bool:
        """
        Validate if a video file can be processed.
        
        Args:
            video_path (str): Path to video file
            
        Returns:
            bool: True if video is valid
        """
        try:
            if not os.path.exists(video_path):
                return False
                
            file_ext = os.path.splitext(video_path)[1].lower()
            if file_ext not in self.supported_formats:
                return False
                
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return False
                
            cap.release()
            return True
            
        except Exception:
            return False
            
    def create_thumbnail(self, video_path: str, timestamp: float = 0, 
                        output_path: Optional[str] = None) -> str:
        """
        Create a thumbnail from video at specified timestamp.
        
        Args:
            video_path (str): Path to video file
            timestamp (float): Timestamp in seconds
            output_path (str, optional): Path for thumbnail. If None, creates temp file.
            
        Returns:
            str: Path to the thumbnail image
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
                
            # Set position to timestamp
            cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                raise ValueError(f"Could not read frame at timestamp {timestamp}")
                
            # Create output path if not provided
            if output_path is None:
                temp_dir = tempfile.mkdtemp()
                filename = os.path.basename(video_path)
                name, _ = os.path.splitext(filename)
                output_path = os.path.join(temp_dir, f"thumbnail_{name}_{timestamp:.1f}.jpg")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save thumbnail
            cv2.imwrite(output_path, frame)
            
            logger.info(f"Thumbnail created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail: {str(e)}")
            raise 