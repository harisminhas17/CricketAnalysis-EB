import cv2
import numpy as np
from typing import Tuple, List, Optional
import logging
from dataclasses import dataclass
from audio_processor import AudioProcessor, AudioFrame

logger = logging.getLogger(__name__)

@dataclass
class SynchronizedFrame:
    frame_number: int
    video_frame: np.ndarray
    audio_frame: Optional[AudioFrame]
    timestamp: float

class AudioVideoSynchronizer:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.video_fps = 30.0  # Default video FPS
        self.audio_sample_rate = 44100  # Default audio sample rate
        self.sync_window = 0.1  # Synchronization window in seconds
        
    def synchronize(self, video_path: str, audio_path: str) -> List[SynchronizedFrame]:
        """Synchronize audio and video streams."""
        try:
            # Open video capture
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Failed to open video file: {video_path}")
                
            # Get video properties
            self.video_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Load audio
            audio_samples, self.audio_sample_rate = self.audio_processor.load_audio(audio_path)
            
            # Calculate samples per frame
            samples_per_frame = int(self.audio_sample_rate / self.video_fps)
            
            # Process frames
            synchronized_frames = []
            frame_number = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Calculate timestamp
                timestamp = frame_number / self.video_fps
                
                # Extract corresponding audio frame
                start_sample = int(timestamp * self.audio_sample_rate)
                end_sample = start_sample + samples_per_frame
                
                if end_sample <= len(audio_samples):
                    audio_frame = AudioFrame(
                        timestamp=timestamp,
                        samples=audio_samples[start_sample:end_sample],
                        sample_rate=self.audio_sample_rate,
                        frame_number=frame_number
                    )
                else:
                    audio_frame = None
                    
                # Create synchronized frame
                sync_frame = SynchronizedFrame(
                    frame_number=frame_number,
                    video_frame=frame,
                    audio_frame=audio_frame,
                    timestamp=timestamp
                )
                
                synchronized_frames.append(sync_frame)
                frame_number += 1
                
            cap.release()
            return synchronized_frames
            
        except Exception as e:
            logger.error(f"Error synchronizing audio and video: {str(e)}")
            raise
            
    def detect_edges(self, synchronized_frames: List[SynchronizedFrame]) -> List[Tuple[int, float, str]]:
        """Detect edges using synchronized audio and video data."""
        try:
            edges = []
            
            for frame in synchronized_frames:
                if frame.audio_frame is None:
                    continue
                    
                # Extract audio features
                features = self.audio_processor.extract_features(frame.audio_frame.samples)
                
                # Detect edges in audio
                audio_edges = self.audio_processor.detect_edges(features)
                
                # Process video frame for visual edges
                visual_edges = self._detect_visual_edges(frame.video_frame)
                
                # Combine audio and visual edges
                combined_edges = self._combine_edges(
                    frame.frame_number,
                    audio_edges,
                    visual_edges
                )
                
                edges.extend(combined_edges)
                
            return edges
            
        except Exception as e:
            logger.error(f"Error detecting edges: {str(e)}")
            raise
            
    def _detect_visual_edges(self, frame: np.ndarray) -> List[Tuple[float, float]]:
        """Detect edges in video frame using Canny edge detection."""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Detect edges
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calculate edge strength for each contour
            visual_edges = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small contours
                    # Calculate edge strength based on contour properties
                    perimeter = cv2.arcLength(contour, True)
                    strength = min(1.0, area / (perimeter * perimeter))
                    visual_edges.append((strength, strength))
                    
            return visual_edges
            
        except Exception as e:
            logger.error(f"Error detecting visual edges: {str(e)}")
            return []
            
    def _combine_edges(self, frame_number: int, 
                      audio_edges: List[Tuple[float, float]], 
                      visual_edges: List[Tuple[float, float]]) -> List[Tuple[int, float, str]]:
        """Combine audio and visual edges with confidence scores."""
        combined = []
        
        # Process audio edges
        for _, confidence in audio_edges:
            if confidence > 0.5:  # Threshold for audio edges
                combined.append((frame_number, confidence, 'audio'))
                
        # Process visual edges
        for _, confidence in visual_edges:
            if confidence > 0.5:  # Threshold for visual edges
                combined.append((frame_number, confidence, 'visual'))
                
        # Sort by confidence
        combined.sort(key=lambda x: x[1], reverse=True)
        
        return combined 