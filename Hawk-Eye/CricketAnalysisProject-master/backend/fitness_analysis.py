import numpy as np
import cv2
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class MovementMetrics:
    distance: float
    speed: float
    acceleration: float
    direction_changes: int
    timestamp: datetime

@dataclass
class FitnessMetrics:
    distance_covered: float  # in meters
    average_speed: float    # in km/h
    max_speed: float       # in km/h
    acceleration: float    # in m/s²
    movement_patterns: Dict[str, int]  # count of different movement types
    energy_expenditure: float  # in kcal

class FitnessAnalyzer:
    def __init__(self):
        self.movement_history: List[MovementMetrics] = []
        self.fatigue_threshold = 0.7  # Threshold for fatigue detection
        self.workload_threshold = 0.8  # Threshold for high workload
        
    def analyze_movement(self, frame: np.ndarray, player_positions: List[Tuple[int, int]]) -> Dict[str, Any]:
        """Analyze player movement in a frame."""
        if len(player_positions) < 2:
            return {
                'distance': 0,
                'speed': 0,
                'acceleration': 0,
                'direction_changes': 0,
                'fatigue_level': 0,
                'workload_level': 0
            }
            
        # Calculate movement metrics
        distances = []
        speeds = []
        accelerations = []
        direction_changes = 0
        
        for i in range(1, len(player_positions)):
            # Calculate distance
            dx = player_positions[i][0] - player_positions[i-1][0]
            dy = player_positions[i][1] - player_positions[i-1][1]
            distance = np.sqrt(dx*dx + dy*dy)
            distances.append(distance)
            
            # Calculate speed (pixels per frame)
            speed = distance
            speeds.append(speed)
            
            # Calculate acceleration
            if i > 1:
                acceleration = speed - speeds[i-2]
                accelerations.append(acceleration)
            
            # Detect direction changes
            if i > 1:
                prev_dx = player_positions[i-1][0] - player_positions[i-2][0]
                prev_dy = player_positions[i-1][1] - player_positions[i-2][1]
                current_dx = dx
                current_dy = dy
                
                # Calculate angle between vectors
                dot_product = prev_dx * current_dx + prev_dy * current_dy
                prev_mag = np.sqrt(prev_dx*prev_dx + prev_dy*prev_dy)
                current_mag = np.sqrt(current_dx*current_dx + current_dy*current_dy)
                
                if prev_mag > 0 and current_mag > 0:
                    cos_angle = dot_product / (prev_mag * current_mag)
                    if cos_angle < 0.7:  # Angle greater than ~45 degrees
                        direction_changes += 1
        
        # Calculate average metrics
        avg_distance = np.mean(distances) if distances else 0
        avg_speed = np.mean(speeds) if speeds else 0
        avg_acceleration = np.mean(accelerations) if accelerations else 0
        
        # Calculate fatigue and workload levels
        fatigue_level = self._calculate_fatigue_level(avg_speed, direction_changes)
        workload_level = self._calculate_workload_level(avg_distance, avg_speed)
        
        # Store metrics
        metrics = MovementMetrics(
            distance=avg_distance,
            speed=avg_speed,
            acceleration=avg_acceleration,
            direction_changes=direction_changes,
            timestamp=datetime.now()
        )
        self.movement_history.append(metrics)
        
        return {
            'distance': float(avg_distance),
            'speed': float(avg_speed),
            'acceleration': float(avg_acceleration),
            'direction_changes': direction_changes,
            'fatigue_level': float(fatigue_level),
            'workload_level': float(workload_level)
        }
    
    def _calculate_fatigue_level(self, speed: float, direction_changes: int) -> float:
        """Calculate fatigue level based on movement patterns."""
        # Normalize speed (assuming max speed of 50 pixels per frame)
        normalized_speed = min(speed / 50, 1.0)
        
        # Calculate fatigue score (0-1)
        fatigue_score = (normalized_speed * 0.4 + 
                        (direction_changes / 10) * 0.6)  # Normalize direction changes
        
        return min(fatigue_score, 1.0)
    
    def _calculate_workload_level(self, distance: float, speed: float) -> float:
        """Calculate workload level based on distance and speed."""
        # Normalize distance (assuming max distance of 1000 pixels)
        normalized_distance = min(distance / 1000, 1.0)
        
        # Normalize speed (assuming max speed of 50 pixels per frame)
        normalized_speed = min(speed / 50, 1.0)
        
        # Calculate workload score (0-1)
        workload_score = (normalized_distance * 0.6 + 
                         normalized_speed * 0.4)
        
        return min(workload_score, 1.0)
    
    def get_trends(self) -> Dict[str, Any]:
        """Get movement trends over time."""
        if not self.movement_history:
            return {
                'fatigue_trend': [],
                'workload_trend': [],
                'speed_trend': [],
                'distance_trend': []
            }
        
        # Extract trends
        fatigue_trend = [m.fatigue_level for m in self.movement_history]
        workload_trend = [m.workload_level for m in self.movement_history]
        speed_trend = [m.speed for m in self.movement_history]
        distance_trend = [m.distance for m in self.movement_history]
        
        return {
            'fatigue_trend': fatigue_trend,
            'workload_trend': workload_trend,
            'speed_trend': speed_trend,
            'distance_trend': distance_trend
        }

def analyze_player_movement(frames: List[np.ndarray], fps: float) -> FitnessMetrics:
    """
    Analyze player movement patterns and calculate fitness metrics.
    
    Args:
        frames (List[np.ndarray]): List of video frames
        fps (float): Frames per second of the video
        
    Returns:
        FitnessMetrics: Object containing various fitness metrics
    """
    try:
        # Initialize variables
        total_distance = 0.0
        speeds = []
        accelerations = []
        movement_patterns = {
            'walking': 0,
            'running': 0,
            'sprinting': 0,
            'standing': 0
        }
        
        # Process frames
        prev_position = None
        prev_speed = 0
        
        for i in range(1, len(frames)):
            # Get player position in current frame
            current_position = detect_player_position(frames[i])
            
            if prev_position is not None and current_position is not None:
                # Calculate distance moved
                distance = calculate_distance(prev_position, current_position)
                total_distance += distance
                
                # Calculate speed
                speed = distance * fps  # m/s
                speeds.append(speed)
                
                # Calculate acceleration
                if len(speeds) > 1:
                    acceleration = (speed - prev_speed) * fps  # m/s²
                    accelerations.append(acceleration)
                
                # Classify movement pattern
                movement_type = classify_movement(speed)
                movement_patterns[movement_type] += 1
                
                prev_speed = speed
            
            prev_position = current_position
        
        # Calculate metrics
        avg_speed = np.mean(speeds) if speeds else 0
        max_speed = max(speeds) if speeds else 0
        avg_acceleration = np.mean(accelerations) if accelerations else 0
        
        # Calculate energy expenditure (simplified model)
        energy = calculate_energy_expenditure(
            total_distance,
            avg_speed,
            movement_patterns
        )
        
        return FitnessMetrics(
            distance_covered=total_distance,
            average_speed=avg_speed * 3.6,  # convert to km/h
            max_speed=max_speed * 3.6,     # convert to km/h
            acceleration=avg_acceleration,
            movement_patterns=movement_patterns,
            energy_expenditure=energy
        )
        
    except Exception as e:
        logger.error(f"Error in fitness analysis: {str(e)}")
        raise

def detect_player_position(frame):
    """Detect player position in a frame."""
    try:
        # Ensure frame is a numpy array
        if not isinstance(frame, np.ndarray):
            frame = np.array(frame)
        
        # Convert frame to RGB if it's not already
        if len(frame.shape) == 2:  # If grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:  # If RGBA
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Find the largest contour (assuming it's the player)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Calculate center point
        center_x = x + w // 2
        center_y = y + h // 2
        
        return (center_x, center_y)
        
    except Exception as e:
        logger.error(f"Error detecting player position: {str(e)}")
        return None

def calculate_distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        pos1 (Tuple[float, float]): First position
        pos2 (Tuple[float, float]): Second position
        
    Returns:
        float: Distance in meters
    """
    try:
        # Convert pixel coordinates to meters (assuming 1 pixel = 0.01 meters)
        PIXEL_TO_METER = 0.01
        return np.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2) * PIXEL_TO_METER
    except Exception as e:
        logger.error(f"Error calculating distance: {str(e)}")
        return 0.0

def classify_movement(speed: float) -> str:
    """
    Classify movement type based on speed.
    
    Args:
        speed (float): Speed in m/s
        
    Returns:
        str: Movement type
    """
    if speed < 0.5:
        return 'standing'
    elif speed < 2.0:
        return 'walking'
    elif speed < 4.0:
        return 'running'
    else:
        return 'sprinting'

def calculate_energy_expenditure(
    distance: float,
    avg_speed: float,
    movement_patterns: Dict[str, int]
) -> float:
    """
    Calculate energy expenditure using a simplified model.
    
    Args:
        distance (float): Total distance covered in meters
        avg_speed (float): Average speed in m/s
        movement_patterns (Dict[str, int]): Count of different movement types
        
    Returns:
        float: Energy expenditure in kcal
    """
    try:
        # Energy expenditure coefficients (kcal per minute)
        COEFFICIENTS = {
            'standing': 1.0,
            'walking': 3.0,
            'running': 7.0,
            'sprinting': 12.0
        }
        
        # Calculate total time spent in each movement type
        total_frames = sum(movement_patterns.values())
        if total_frames == 0:
            return 0.0
            
        # Calculate energy expenditure
        energy = 0.0
        for movement_type, count in movement_patterns.items():
            time_fraction = count / total_frames
            energy += COEFFICIENTS[movement_type] * time_fraction
            
        # Convert to total energy expenditure
        total_time = distance / avg_speed if avg_speed > 0 else 0
        total_energy = energy * (total_time / 60)  # Convert to minutes
        
        return total_energy
        
    except Exception as e:
        logger.error(f"Error calculating energy expenditure: {str(e)}")
        return 0.0 