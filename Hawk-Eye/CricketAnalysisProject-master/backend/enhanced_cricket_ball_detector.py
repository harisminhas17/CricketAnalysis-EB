import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional, Dict, Any
from collections import deque
import math
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class BallDetection:
    position: Tuple[int, int]
    radius: float
    confidence: float
    velocity: Tuple[float, float, float]  # (vx, vy, vz) in m/s
    timestamp: float
    distance_covered: float  # in meters
    is_valid_cricket_ball: bool

class EnhancedCricketBallDetector:
    """
    Enhanced cricket ball detector that specifically addresses:
    1. Spherical/circular object detection with proper circumference understanding
    2. Minimum velocity requirements (30kmph minimum)
    3. Minimum distance tracking (15m minimum, 13m for validation)
    4. False positive removal based on motion patterns
    5. Standard cricket ball dimensions consideration
    """
    
    def __init__(self):
        # Cricket ball physical constants
        self.STANDARD_BALL_RADIUS = 0.0364  # meters (ICC standard)
        self.STANDARD_BALL_CIRCUMFERENCE = 2 * np.pi * self.STANDARD_BALL_RADIUS  # ~0.229m
        self.MIN_BALL_VELOCITY = 8.33  # m/s (30 km/h minimum)
        self.VALIDATION_VELOCITY = 8.33  # m/s (30 km/h for validation)
        self.MIN_DISTANCE_COVERED = 15.0  # meters minimum
        self.VALIDATION_DISTANCE = 13.0  # meters for validation
        
        # Detection parameters
        self.min_circularity = 0.7  # Stricter circularity for spherical objects
        self.max_circularity = 1.3
        self.min_radius_pixels = 5
        self.max_radius_pixels = 30
        
        # Motion tracking
        self.ball_positions_history = deque(maxlen=30)
        self.ball_velocities_history = deque(maxlen=30)
        self.distance_traveled = 0.0
        self.last_valid_position = None
        self.tracking_start_time = None
        
        # Calibration
        self.pixels_to_meters = 0.01  # Default calibration
        self.fps = 30  # Standard video frame rate
        
        # HSV color ranges for cricket balls
        self.red_ball_ranges = [
            (np.array([0, 100, 100]), np.array([10, 255, 255])),  # Lower red
            (np.array([160, 100, 100]), np.array([180, 255, 255]))  # Upper red
        ]
        self.white_ball_range = (np.array([0, 0, 200]), np.array([180, 30, 255]))
        
        # Validation thresholds
        self.min_frames_for_validation = 10
        self.max_missing_frames = 5
        self.velocity_smoothing_factor = 0.8
        
        # Multi-object tracking
        self.tracked_objects = {}  # id -> {'positions': [..], 'velocities': [..], 'last_frame': int}
        self.next_object_id = 1
        self.max_tracking_distance = 40  # pixels for centroid association
        self.max_missing_frames = 5

    def calibrate_from_pitch_dimensions(self, frame_width: int, frame_height: int):
        """Calibrate pixel-to-meter conversion using cricket pitch dimensions."""
        # Standard cricket pitch is 20.12 meters long
        # Assume pitch takes 80% of frame height
        pitch_length_pixels = frame_height * 0.8
        self.pixels_to_meters = 20.12 / pitch_length_pixels
        logger.info(f"Calibrated pixels_to_meters: {self.pixels_to_meters}")
    
    def _detect_hough_circles(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 | mask2
        red_only = cv2.bitwise_and(frame, frame, mask=red_mask)
        gray = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                                   param1=100, param2=30, minRadius=5, maxRadius=50)
        candidates = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                candidates.append({
                    'position': (i[0], i[1]),
                    'radius': i[2],
                    'confidence': 1.0,  # Hough is confident for clear circles
                    'source': 'hough'
                })
        return candidates

    def detect_cricket_ball(self, frame: np.ndarray, frame_number: int) -> Optional[BallDetection]:
        """
        Enhanced cricket ball detection with spherical dimension validation.
        
        Args:
            frame: Current video frame
            frame_number: Current frame number for timestamp calculation
            
        Returns:
            BallDetection object if valid cricket ball is detected
        """
        try:
            # Step 1: Preprocess frame for better detection
            processed_frame = self._preprocess_frame(frame)
            
            # Step 2: Create ROI mask focusing on cricket field
            roi_mask = self._create_cricket_field_roi(frame.shape)
            
            # Step 3: Detect spherical objects using multiple methods
            spherical_candidates = self._detect_spherical_objects(processed_frame, roi_mask)
            hough_candidates = self._detect_hough_circles(frame)
            all_candidates = spherical_candidates + hough_candidates
            
            # Print all candidate info for debugging
            print(f"[Frame {frame_number}] Candidates:")
            for cand in all_candidates:
                pos = cand.get('position')
                radius = cand.get('radius')
                conf = cand.get('confidence')
                source = cand.get('source', 'spherical')
                print(f"  - Pos: {pos}, Radius: {radius}, Conf: {conf}, Source: {source}")
            
            if not all_candidates:
                self._update_tracks([], frame_number)
                return self._predict_position_from_motion(frame_number)
            
            # Step 4: Filter by cricket ball characteristics
            ball_candidates = self._filter_cricket_ball_candidates(all_candidates, frame)
            self._update_tracks(ball_candidates, frame_number)
            
            # Find the best valid track
            best_track = None
            best_score = -1
            for obj_id, obj in self.tracked_objects.items():
                if len(obj['positions']) < 3:
                    continue
                velocities = obj['velocities']
                if not velocities:
                    continue
                avg_vx = np.mean([v[0] for v in velocities])
                avg_vy = np.mean([v[1] for v in velocities])
                avg_speed = math.sqrt(avg_vx**2 + avg_vy**2) * 3.6
                if avg_speed < 40.0:  # Raised from 10.0 to 40.0 km/h
                    continue
                speed_var = np.var([math.sqrt(v[0]**2 + v[1]**2) for v in velocities])
                if speed_var < 1.0:
                    continue
                x, y = obj['positions'][-1]
                height, width = frame.shape[:2]
                pitch_width = int(width * 0.12)
                pitch_height = int(height * 0.8)
                pitch_x = (width - pitch_width) // 2
                pitch_y = (height - pitch_height) // 2
                if not (pitch_x <= x <= pitch_x + pitch_width and pitch_y <= y <= pitch_y + pitch_height):
                    continue
                score = len(obj['positions']) + avg_speed
                if score > best_score:
                    best_score = score
                    best_track = obj
            if best_track:
                pos = best_track['positions'][-1]
                vx, vy = best_track['velocities'][-1] if best_track['velocities'] else (0.0, 0.0)
                velocity = (vx, vy, 0.0)
                distance_covered = 0.0
                for i in range(1, len(best_track['positions'])):
                    prev = best_track['positions'][i-1]
                    curr = best_track['positions'][i]
                    distance_covered += math.hypot(curr[0]-prev[0], curr[1]-prev[1]) * self.pixels_to_meters
                return BallDetection(
                    position=pos,
                    radius=12.0,  # Approximate
                    confidence=1.0,
                    velocity=velocity,
                    timestamp=frame_number / self.fps,
                    distance_covered=distance_covered,
                    is_valid_cricket_ball=True
                )
            return self._predict_position_from_motion(frame_number), all_candidates
            
        except Exception as e:
            logger.error(f"Error in cricket ball detection: {str(e)}")
            return self._predict_position_from_motion(frame_number), []
    
    def _preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Enhanced preprocessing for better spherical object detection."""
        # Convert to LAB color space for better color processing
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        # Apply CLAHE to L channel for better contrast
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels back
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply bilateral filter to reduce noise while preserving edges
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # Apply Gaussian blur for better contour detection
        blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
        
        return blurred
    
    def _create_cricket_field_roi(self, frame_shape: Tuple[int, int, int]) -> np.ndarray:
        """Create ROI mask focusing on cricket field area."""
        height, width = frame_shape[:2]
        
        # Focus on center 70% of the frame (typical cricket field area)
        roi_percentage = 0.7
        roi_top = int(height * (1 - roi_percentage) / 2)
        roi_bottom = int(height * (1 + roi_percentage) / 2)
        roi_left = int(width * (1 - roi_percentage) / 2)
        roi_right = int(width * (1 + roi_percentage) / 2)
        
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[roi_top:roi_bottom, roi_left:roi_right] = 255
        
        return mask
    
    def _detect_spherical_objects(self, frame: np.ndarray, roi_mask: np.ndarray) -> List[Dict]:
        """Detect spherical objects using multiple detection methods."""
        spherical_candidates = []
        
        # Method 1: HSV color-based detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create masks for red and white cricket balls
        ball_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        # Red ball detection
        for lower, upper in self.red_ball_ranges:
            red_mask = cv2.inRange(hsv, lower, upper)
            ball_mask = cv2.bitwise_or(ball_mask, red_mask)
        
        # White ball detection
        white_mask = cv2.inRange(hsv, self.white_ball_range[0], self.white_ball_range[1])
        ball_mask = cv2.bitwise_or(ball_mask, white_mask)
        
        # Apply ROI mask
        ball_mask = cv2.bitwise_and(ball_mask, roi_mask)
        
        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_CLOSE, kernel)
        ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter by circularity and size
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 50:  # Skip very small contours
                continue
            
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            
            # Calculate circularity (perfect circle = 1.0)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if self.min_circularity <= circularity <= self.max_circularity:
                # Get minimum enclosing circle
                (x, y), radius = cv2.minEnclosingCircle(contour)
                
                if self.min_radius_pixels <= radius <= self.max_radius_pixels:
                    # Calculate confidence based on circularity and size
                    size_confidence = 1.0 / (1.0 + abs(radius - 12))  # Prefer radius around 12 pixels
                    circularity_confidence = circularity
                    total_confidence = (size_confidence + circularity_confidence) / 2
                    
                    spherical_candidates.append({
                        'position': (int(x), int(y)),
                        'radius': radius,
                        'circularity': circularity,
                        'area': area,
                        'confidence': total_confidence,
                        'contour': contour
                    })
        
        return spherical_candidates
    
    def _filter_cricket_ball_candidates(self, candidates: List[Dict], frame: np.ndarray) -> List[Dict]:
        """Filter candidates based on cricket ball characteristics and restrict to pitch area."""
        filtered_candidates = []
        height, width = frame.shape[:2]
        # Define pitch rectangle (same as in comprehensive_video_analysis.py)
        pitch_width = int(width * 0.12)
        pitch_height = int(height * 0.8)
        pitch_x = (width - pitch_width) // 2
        pitch_y = (height - pitch_height) // 2
        pitch_rect = (pitch_x, pitch_y, pitch_x + pitch_width, pitch_y + pitch_height)
        for candidate in candidates:
            # Only accept candidates within the pitch rectangle
            x, y = candidate['position']
            if not (pitch_rect[0] <= x <= pitch_rect[2] and pitch_rect[1] <= y <= pitch_rect[3]):
                continue
            # Check if position is consistent with previous motion
            if len(self.ball_positions_history) > 0:
                last_pos = self.ball_positions_history[-1]
                distance = math.sqrt(
                    (candidate['position'][0] - last_pos[0])**2 + 
                    (candidate['position'][1] - last_pos[1])**2
                )
                # If distance is too large, it might be a false positive
                if distance > 100:
                    continue
            # Additional filtering based on position in frame
            frame_center_x = frame.shape[1] // 2
            frame_center_y = frame.shape[0] // 2
            distance_from_center = math.sqrt(
                (candidate['position'][0] - frame_center_x)**2 + 
                (candidate['position'][1] - frame_center_y)**2
            )
            position_confidence = 1.0 / (1.0 + distance_from_center / 200)
            candidate['confidence'] *= position_confidence
            filtered_candidates.append(candidate)
        return filtered_candidates
    
    def _select_best_candidate(self, candidates: List[Dict], frame: np.ndarray) -> Optional[Dict]:
        """Select the best cricket ball candidate."""
        if not candidates:
            return None
        
        # Sort by confidence
        candidates.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Return the best candidate
        return candidates[0]
    
    def _calculate_velocity(self, position: Tuple[int, int], frame_number: int) -> Tuple[float, float, float]:
        """Calculate ball velocity in m/s."""
        if len(self.ball_positions_history) < 2:
            return (0.0, 0.0, 0.0)
        
        # Get last position
        last_pos = self.ball_positions_history[-1]
        
        # Calculate velocity in pixels per frame
        vx_pixels = (position[0] - last_pos[0]) / self.fps
        vy_pixels = (position[1] - last_pos[1]) / self.fps
        
        # Convert to m/s
        vx = vx_pixels * self.pixels_to_meters
        vy = vy_pixels * self.pixels_to_meters
        
        # Estimate z-velocity (simplified - can be enhanced with depth estimation)
        vz = 0.0
        
        return (vx, vy, vz)
    
    def _calculate_distance_covered(self, position: Tuple[int, int]) -> float:
        """Calculate total distance covered by the ball."""
        if len(self.ball_positions_history) < 2:
            return 0.0
        
        total_distance = 0.0
        
        for i in range(1, len(self.ball_positions_history)):
            prev_pos = self.ball_positions_history[i-1]
            curr_pos = self.ball_positions_history[i]
            
            # Calculate distance in pixels
            distance_pixels = math.sqrt(
                (curr_pos[0] - prev_pos[0])**2 + 
                (curr_pos[1] - prev_pos[1])**2
            )
            
            # Convert to meters
            distance_meters = distance_pixels * self.pixels_to_meters
            total_distance += distance_meters
        
        return total_distance
    
    def _validate_cricket_ball_characteristics(self, candidate: Dict, velocity: Tuple[float, float, float], 
                                             distance_covered: float, frame_number: int) -> bool:
        """Validate if the detected object meets cricket ball characteristics."""
        
        # Calculate velocity magnitude
        velocity_magnitude = math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)
        velocity_kmh = velocity_magnitude * 3.6  # Convert to km/h
        
        # Check minimum velocity requirement (30 km/h)
        if velocity_kmh < 30.0:  # Direct comparison in km/h
            return False
        
        # Check minimum distance requirement
        if distance_covered < self.MIN_DISTANCE_COVERED:
            return False
        
        # Check if we have enough tracking history for validation
        if len(self.ball_positions_history) < self.min_frames_for_validation:
            return True  # Allow detection but mark as unvalidated
        
        # Additional validation for high-confidence detection
        if velocity_kmh >= 30.0 and distance_covered >= self.VALIDATION_DISTANCE:
            return True
        
        # Check motion consistency
        if len(self.ball_velocities_history) >= 3:
            recent_velocities = list(self.ball_velocities_history)[-3:]
            velocity_consistency = self._check_velocity_consistency(recent_velocities)
            if not velocity_consistency:
                return False
        
        return True
    
    def _check_velocity_consistency(self, velocities: List[Tuple[float, float, float]]) -> bool:
        """Check if velocity changes are consistent with cricket ball physics."""
        if len(velocities) < 2:
            return True
        
        # Calculate velocity changes
        velocity_changes = []
        for i in range(1, len(velocities)):
            prev_vel = velocities[i-1]
            curr_vel = velocities[i]
            
            change = math.sqrt(
                (curr_vel[0] - prev_vel[0])**2 + 
                (curr_vel[1] - prev_vel[1])**2 + 
                (curr_vel[2] - prev_vel[2])**2
            )
            velocity_changes.append(change)
        
        # Check if velocity changes are reasonable (not too abrupt)
        avg_change = sum(velocity_changes) / len(velocity_changes)
        return avg_change < 10.0  # m/s - reasonable threshold for cricket ball
        
    def _update_tracking_history(self, position: Tuple[int, int], velocity: Tuple[float, float, float], 
                                frame_number: int):
        """Update tracking history with new ball position."""
        self.ball_positions_history.append(position)
        self.ball_velocities_history.append(velocity)
        
        # Update distance traveled
        if len(self.ball_positions_history) >= 2:
            prev_pos = self.ball_positions_history[-2]
            distance_pixels = math.sqrt(
                (position[0] - prev_pos[0])**2 + 
                (position[1] - prev_pos[1])**2
            )
            self.distance_traveled += distance_pixels * self.pixels_to_meters
        
        # Update tracking start time
        if self.tracking_start_time is None:
            self.tracking_start_time = frame_number / self.fps
    
    def _predict_position_from_motion(self, frame_number: int) -> Optional[BallDetection]:
        """Predict ball position based on previous motion when detection fails."""
        if len(self.ball_positions_history) < 2 or len(self.ball_velocities_history) < 1:
            return None
        
        # Get last position and velocity
        last_pos = self.ball_positions_history[-1]
        last_vel = self.ball_velocities_history[-1]
        
        # Predict new position based on velocity
        predicted_x = last_pos[0] + last_vel[0] / self.pixels_to_meters / self.fps
        predicted_y = last_pos[1] + last_vel[1] / self.pixels_to_meters / self.fps
        
        predicted_position = (int(predicted_x), int(predicted_y))
        
        return BallDetection(
            position=predicted_position,
            radius=10.0,  # Default radius
            confidence=0.5,  # Lower confidence for predicted position
            velocity=last_vel,
            timestamp=frame_number / self.fps,
            distance_covered=self.distance_traveled,
            is_valid_cricket_ball=False  # Mark as predicted, not detected
        )

    def _update_tracks(self, candidates, frame_number):
        # Associate candidates to existing tracks by nearest centroid
        assigned_ids = set()
        for candidate in candidates:
            x, y = candidate['position']
            best_id = None
            best_dist = float('inf')
            for obj_id, obj in self.tracked_objects.items():
                last_pos = obj['positions'][-1]
                dist = math.hypot(x - last_pos[0], y - last_pos[1])
                if dist < self.max_tracking_distance and dist < best_dist:
                    best_dist = dist
                    best_id = obj_id
            if best_id is not None:
                # Update existing track
                obj = self.tracked_objects[best_id]
                obj['positions'].append((x, y))
                if len(obj['positions']) > 1:
                    vx = (x - obj['positions'][-2][0]) / self.fps * self.pixels_to_meters
                    vy = (y - obj['positions'][-2][1]) / self.fps * self.pixels_to_meters
                    obj['velocities'].append((vx, vy))
                else:
                    obj['velocities'].append((0.0, 0.0))
                obj['last_frame'] = frame_number
                assigned_ids.add(best_id)
            else:
                # Create new track
                self.tracked_objects[self.next_object_id] = {
                    'positions': [(x, y)],
                    'velocities': [],
                    'last_frame': frame_number
                }
                assigned_ids.add(self.next_object_id)
                self.next_object_id += 1
        # Remove tracks not seen for too long
        to_remove = [obj_id for obj_id, obj in self.tracked_objects.items() if frame_number - obj['last_frame'] > self.max_missing_frames]
        for obj_id in to_remove:
            del self.tracked_objects[obj_id]
    
    def get_tracking_statistics(self) -> Dict[str, Any]:
        """Get current tracking statistics."""
        if not self.ball_positions_history:
            return {
                'total_distance': 0.0,
                'average_velocity': 0.0,
                'max_velocity': 0.0,
                'tracking_duration': 0.0,
                'detection_rate': 0.0
            }
        
        # Calculate statistics
        velocities = list(self.ball_velocities_history)
        velocity_magnitudes = [math.sqrt(v[0]**2 + v[1]**2 + v[2]**2) for v in velocities]
        
        avg_velocity = sum(velocity_magnitudes) / len(velocity_magnitudes) if velocity_magnitudes else 0.0
        max_velocity = max(velocity_magnitudes) if velocity_magnitudes else 0.0
        
        tracking_duration = 0.0
        if self.tracking_start_time is not None:
            tracking_duration = (len(self.ball_positions_history) / self.fps)
        
        return {
            'total_distance': self.distance_traveled,
            'average_velocity': avg_velocity * 3.6,  # Convert to km/h
            'max_velocity': max_velocity * 3.6,  # Convert to km/h
            'tracking_duration': tracking_duration,
            'detection_rate': len(self.ball_positions_history) / max(tracking_duration * self.fps, 1)
        }
    
    def reset_tracking(self):
        """Reset tracking state."""
        self.ball_positions_history.clear()
        self.ball_velocities_history.clear()
        self.distance_traveled = 0.0
        self.last_valid_position = None
        self.tracking_start_time = None 