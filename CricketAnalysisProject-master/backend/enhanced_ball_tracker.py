import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional, Dict, Any
from collections import deque
import math

logger = logging.getLogger(__name__)

class EnhancedBallTracker:
    """
    Enhanced ball tracker specifically designed for white circular cricket balls
    that are constantly changing position across multiple frames.
    """
    
    def __init__(self, max_history_frames=10, prediction_frames=3):
        self.max_history_frames = max_history_frames
        self.prediction_frames = prediction_frames
        self.ball_positions_history = deque(maxlen=max_history_frames)
        self.ball_velocities_history = deque(maxlen=max_history_frames)
        self.last_detected_position = None
        self.tracking_active = False
        self.missing_frames_count = 0
        self.max_missing_frames = 5
        
        # Enhanced parameters for white ball detection
        self.white_ball_lower = np.array([0, 0, 200])  # High value for white
        self.white_ball_upper = np.array([180, 30, 255])
        
        # Motion prediction parameters
        self.velocity_smoothing_factor = 0.7
        self.position_smoothing_factor = 0.8
        
        # Detection parameters
        self.min_ball_radius = 3
        self.max_ball_radius = 25
        self.min_circularity = 0.6
        self.max_circularity = 1.4
        
    def detect_white_ball(self, frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """
        Enhanced detection specifically for white circular balls.
        Uses multiple detection strategies and motion prediction.
        """
        try:
            # Step 1: Preprocess frame for better white detection
            processed_frame = self._preprocess_for_white_detection(frame)
            
            # Step 2: Create multiple detection masks
            hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
            
            # Primary white ball mask
            white_mask = cv2.inRange(hsv, self.white_ball_lower, self.white_ball_upper)
            
            # Additional white detection with different parameters
            white_mask2 = cv2.inRange(hsv, np.array([0, 0, 180]), np.array([180, 50, 255]))
            
            # Combine masks
            combined_mask = cv2.bitwise_or(white_mask, white_mask2)
            
            # Step 3: Apply ROI to focus on cricket field
            roi_mask = self._create_cricket_field_roi(frame.shape)
            combined_mask = cv2.bitwise_and(combined_mask, roi_mask)
            
            # Step 4: Morphological operations
            kernel = np.ones((3, 3), np.uint8)
            combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
            combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
            
            # Step 5: Find contours
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return self._predict_position_from_motion()
            
            # Step 6: Filter by circularity and size
            ball_candidates = self._filter_circular_objects(contours)
            
            if not ball_candidates:
                return self._predict_position_from_motion()
            
            # Step 7: Motion consistency filtering
            motion_filtered = self._filter_by_motion_consistency(ball_candidates)
            
            if not motion_filtered:
                motion_filtered = ball_candidates  # Use all candidates if no motion consistency
            
            # Step 8: Select best candidate
            best_candidate = self._select_best_candidate(motion_filtered, frame)
            
            if best_candidate:
                self._update_tracking_state(best_candidate)
                return best_candidate
            
            return self._predict_position_from_motion()
            
        except Exception as e:
            logger.error(f"Error in white ball detection: {str(e)}")
            return self._predict_position_from_motion()
    
    def _preprocess_for_white_detection(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame to enhance white object detection."""
        # Enhance contrast for better white detection
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply bilateral filter to reduce noise while preserving edges
        processed = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        return processed
    
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
    
    def _filter_circular_objects(self, contours: List) -> List[Tuple]:
        """Filter contours to find circular objects matching ball criteria."""
        circular_candidates = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 20:  # Skip very small contours
                continue
            
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            
            # Calculate circularity
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if self.min_circularity <= circularity <= self.max_circularity:
                # Get minimum enclosing circle
                (x, y), radius = cv2.minEnclosingCircle(contour)
                
                if self.min_ball_radius <= radius <= self.max_ball_radius:
                    circular_candidates.append((contour, (int(x), int(y)), radius, circularity))
        
        return circular_candidates
    
    def _filter_by_motion_consistency(self, candidates: List[Tuple]) -> List[Tuple]:
        """Filter candidates based on motion consistency with previous detections."""
        if len(self.ball_positions_history) < 2:
            return candidates
        
        motion_filtered = []
        max_motion_distance = 100  # Increased for fast-moving balls
        
        for candidate in candidates:
            contour, (x, y), radius, circularity = candidate
            
            # Check if this position is consistent with recent motion
            is_consistent = True
            
            for prev_pos in list(self.ball_positions_history)[-3:]:  # Check last 3 positions
                if prev_pos is not None:
                    distance = math.sqrt((x - prev_pos[0])**2 + (y - prev_pos[1])**2)
                    if distance > max_motion_distance:
                        is_consistent = False
                        break
            
            if is_consistent:
                motion_filtered.append(candidate)
        
        return motion_filtered
    
    def _select_best_candidate(self, candidates: List[Tuple], frame: np.ndarray) -> Optional[Tuple[int, int]]:
        """Select the best ball candidate based on multiple criteria."""
        if not candidates:
            return None
        
        best_candidate = None
        best_score = -float('inf')
        
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2
        
        for contour, (x, y), radius, circularity in candidates:
            # Calculate multiple scoring factors
            
            # 1. Circularity score (higher is better)
            circularity_score = circularity
            
            # 2. Size score (prefer radius around 8-12 pixels)
            ideal_radius = 10
            size_score = 1.0 / (1.0 + abs(radius - ideal_radius))
            
            # 3. Position score (prefer center of frame)
            distance_from_center = math.sqrt((x - frame_center_x)**2 + (y - frame_center_y)**2)
            position_score = 1.0 / (1.0 + distance_from_center / 200)
            
            # 4. Motion prediction score (if we have previous positions)
            motion_score = 0
            if len(self.ball_positions_history) > 0:
                predicted_pos = self._predict_next_position()
                if predicted_pos:
                    predicted_distance = math.sqrt((x - predicted_pos[0])**2 + (y - predicted_pos[1])**2)
                    motion_score = 1.0 / (1.0 + predicted_distance / 50)
            
            # 5. Area score (prefer larger circular objects)
            area = cv2.contourArea(contour)
            area_score = min(area / 1000, 1.0)  # Normalize to 0-1
            
            # Combine all scores
            total_score = (circularity_score * 0.3 + 
                         size_score * 0.2 + 
                         position_score * 0.2 + 
                         motion_score * 0.2 + 
                         area_score * 0.1)
            
            if total_score > best_score:
                best_score = total_score
                best_candidate = (x, y)
        
        return best_candidate
    
    def _predict_next_position(self) -> Optional[Tuple[int, int]]:
        """Predict next ball position based on velocity history."""
        if len(self.ball_positions_history) < 2 or len(self.ball_velocities_history) < 1:
            return None
        
        # Get last position and average velocity
        last_pos = self.ball_positions_history[-1]
        avg_velocity = np.mean(list(self.ball_velocities_history)[-3:], axis=0) if len(self.ball_velocities_history) >= 3 else self.ball_velocities_history[-1]
        
        # Predict next position
        predicted_x = int(last_pos[0] + avg_velocity[0])
        predicted_y = int(last_pos[1] + avg_velocity[1])
        
        return (predicted_x, predicted_y)
    
    def _predict_position_from_motion(self) -> Optional[Tuple[int, int]]:
        """Predict ball position when detection fails using motion history."""
        if not self.tracking_active or self.missing_frames_count > self.max_missing_frames:
            return None
        
        predicted_pos = self._predict_next_position()
        if predicted_pos:
            self.missing_frames_count += 1
            return predicted_pos
        
        return self.last_detected_position
    
    def _update_tracking_state(self, new_position: Tuple[int, int]):
        """Update tracking state with new ball position."""
        if self.last_detected_position is not None:
            # Calculate velocity
            velocity = (new_position[0] - self.last_detected_position[0],
                       new_position[1] - self.last_detected_position[1])
            
            # Smooth velocity
            if len(self.ball_velocities_history) > 0:
                last_velocity = self.ball_velocities_history[-1]
                smoothed_velocity = (
                    last_velocity[0] * self.velocity_smoothing_factor + velocity[0] * (1 - self.velocity_smoothing_factor),
                    last_velocity[1] * self.velocity_smoothing_factor + velocity[1] * (1 - self.velocity_smoothing_factor)
                )
                self.ball_velocities_history.append(smoothed_velocity)
            else:
                self.ball_velocities_history.append(velocity)
        
        # Update position history
        self.ball_positions_history.append(new_position)
        self.last_detected_position = new_position
        self.tracking_active = True
        self.missing_frames_count = 0
    
    def track_ball_across_frames(self, frames: List[np.ndarray]) -> List[Optional[Tuple[int, int]]]:
        """
        Track ball across multiple frames with enhanced detection and prediction.
        
        Args:
            frames: List of video frames
            
        Returns:
            List of ball positions for each frame (None if not detected)
        """
        ball_positions = []
        
        for i, frame in enumerate(frames):
            ball_pos = self.detect_white_ball(frame)
            ball_positions.append(ball_pos)
            
            # Log detection status
            if ball_pos:
                logger.debug(f"Frame {i}: Ball detected at {ball_pos}")
            else:
                logger.debug(f"Frame {i}: No ball detected")
        
        return ball_positions
    
    def get_trajectory(self) -> List[Tuple[int, int]]:
        """Get the current ball trajectory."""
        return list(self.ball_positions_history)
    
    def get_velocity_history(self) -> List[Tuple[float, float]]:
        """Get the velocity history."""
        return list(self.ball_velocities_history)
    
    def reset_tracking(self):
        """Reset tracking state."""
        self.ball_positions_history.clear()
        self.ball_velocities_history.clear()
        self.last_detected_position = None
        self.tracking_active = False
        self.missing_frames_count = 0
    
    def visualize_tracking(self, frame: np.ndarray, ball_pos: Optional[Tuple[int, int]]) -> np.ndarray:
        """Visualize ball tracking on frame."""
        annotated_frame = frame.copy()
        
        if ball_pos:
            # Draw current ball position
            cv2.circle(annotated_frame, ball_pos, 12, (0, 255, 255), 3)  # Yellow circle
            cv2.circle(annotated_frame, ball_pos, 8, (255, 255, 255), -1)  # White center
            
            # Draw trajectory
            if len(self.ball_positions_history) >= 2:
                points = list(self.ball_positions_history)
                for i in range(1, len(points)):
                    cv2.line(annotated_frame, points[i-1], points[i], (255, 255, 255), 2)
        
        # Add tracking status
        status = "TRACKING" if self.tracking_active else "SEARCHING"
        cv2.putText(annotated_frame, f"Ball: {status}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add trajectory length
        if self.tracking_active:
            cv2.putText(annotated_frame, f"Trajectory: {len(self.ball_positions_history)}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_frame 