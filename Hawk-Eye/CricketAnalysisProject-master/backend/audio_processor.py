import numpy as np
import librosa
import soundfile as sf
from typing import Tuple, List, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AudioFrame:
    timestamp: float
    samples: np.ndarray
    sample_rate: int
    frame_number: int

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 44100  # Standard sample rate
        self.frame_length = 2048  # Frame length for STFT
        self.hop_length = 512    # Hop length for STFT
        self.edge_threshold = 0.7  # Threshold for edge detection
        
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file and return samples and sample rate."""
        try:
            samples, sample_rate = librosa.load(audio_path, sr=self.sample_rate)
            return samples, sample_rate
        except Exception as e:
            logger.error(f"Error loading audio file: {str(e)}")
            raise
            
    def extract_features(self, samples: np.ndarray) -> dict:
        """Extract audio features for edge detection."""
        try:
            # Compute STFT
            stft = librosa.stft(samples, n_fft=self.frame_length, hop_length=self.hop_length)
            
            # Compute spectral features
            spectral_centroid = librosa.feature.spectral_centroid(S=np.abs(stft))[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(S=np.abs(stft))[0]
            spectral_flux = np.diff(np.abs(stft), axis=1)
            
            # Compute temporal features
            onset_env = librosa.onset.onset_strength(y=samples, sr=self.sample_rate)
            tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sample_rate)
            
            return {
                'spectral_centroid': spectral_centroid,
                'spectral_rolloff': spectral_rolloff,
                'spectral_flux': spectral_flux,
                'onset_env': onset_env,
                'tempo': tempo
            }
        except Exception as e:
            logger.error(f"Error extracting audio features: {str(e)}")
            raise
            
    def detect_edges(self, features: dict) -> List[Tuple[float, float]]:
        """Detect edges in audio using multiple features."""
        try:
            edges = []
            
            # Detect edges using spectral flux
            flux_edges = self._detect_flux_edges(features['spectral_flux'])
            
            # Detect edges using onset strength
            onset_edges = self._detect_onset_edges(features['onset_env'])
            
            # Combine and filter edges
            combined_edges = self._combine_edges(flux_edges, onset_edges)
            
            return combined_edges
        except Exception as e:
            logger.error(f"Error detecting edges: {str(e)}")
            raise
            
    def _detect_flux_edges(self, spectral_flux: np.ndarray) -> List[Tuple[float, float]]:
        """Detect edges using spectral flux."""
        edges = []
        threshold = np.mean(spectral_flux) + self.edge_threshold * np.std(spectral_flux)
        
        for i in range(1, len(spectral_flux)):
            if spectral_flux[i] > threshold:
                time = librosa.frames_to_time(i, sr=self.sample_rate, hop_length=self.hop_length)
                confidence = min(1.0, spectral_flux[i] / (2 * threshold))
                edges.append((time, confidence))
                
        return edges
        
    def _detect_onset_edges(self, onset_env: np.ndarray) -> List[Tuple[float, float]]:
        """Detect edges using onset strength."""
        edges = []
        threshold = np.mean(onset_env) + self.edge_threshold * np.std(onset_env)
        
        for i in range(1, len(onset_env)):
            if onset_env[i] > threshold:
                time = librosa.frames_to_time(i, sr=self.sample_rate, hop_length=self.hop_length)
                confidence = min(1.0, onset_env[i] / (2 * threshold))
                edges.append((time, confidence))
                
        return edges
        
    def _combine_edges(self, flux_edges: List[Tuple[float, float]], 
                      onset_edges: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Combine and filter edges from different detection methods."""
        all_edges = flux_edges + onset_edges
        all_edges.sort(key=lambda x: x[0])  # Sort by time
        
        # Merge nearby edges
        merged_edges = []
        current_edge = None
        
        for edge in all_edges:
            if current_edge is None:
                current_edge = edge
            elif edge[0] - current_edge[0] < 0.1:  # Merge edges within 100ms
                # Take the edge with higher confidence
                current_edge = max([current_edge, edge], key=lambda x: x[1])
            else:
                merged_edges.append(current_edge)
                current_edge = edge
                
        if current_edge is not None:
            merged_edges.append(current_edge)
            
        return merged_edges
        
    def synchronize_with_video(self, audio_edges: List[Tuple[float, float]], 
                             video_fps: float) -> List[Tuple[int, float]]:
        """Convert audio edge timestamps to video frame numbers."""
        synchronized_edges = []
        
        for time, confidence in audio_edges:
            frame_number = int(time * video_fps)
            synchronized_edges.append((frame_number, confidence))
            
        return synchronized_edges 