import os
import cv2
import json
import numpy as np
from ultralytics import YOLO
from lbw_predictor import LBWPredictor
import logging
from typing import List, Tuple, Dict, Any, Optional
import traceback

logger = logging.getLogger(__name__)

# Constants for calibration
PIXELS_TO_METERS = 0.01  # Assuming 1 pixel = 1cm
FPS = 30  # Standard video frame rate

# Add a global variable to store the previous frame for motion detection
prev_gray_frame = None

# Global variables for real-time tracking
real_time_trajectory = []
tracking_active = False
last_ball_pos = None
frame_count = 0

# Add a global variable to store the previous ball position for continuity
prev_ball_pos = None

# Reference ball histogram (initialize as None)
ref_ball_hist = None

# Motion tracking variables
ball_positions_history = []
max_history_frames = 5

yolo_model = YOLO('yolov8n.pt')  # Load once globally

def calibrate_pixels_to_meters(frame_width, frame_height):
    """Calibrate pixel to meter conversion based on known cricket pitch dimensions."""
    # Standard cricket pitch is 20.12 meters long
    # We'll use this to calibrate our pixel-to-meter conversion
    pitch_length_pixels = frame_height * 0.8  # Assuming pitch takes 80% of frame height
    return 20.12 / pitch_length_pixels

def classify_shot_zone(start_pos, end_pos):
    """
    Classify shot zone based on ball trajectory.
    
    Args:
        start_pos: Starting position (x, y)
        end_pos: Ending position (x, y)
    
    Returns:
        str: Zone name ('leg_side', 'straight', or 'off_side')
    """
    dx = end_pos[0] - start_pos[0]
    
    # Use the same thresholds as analyze_shot_zone
    if dx > 0.2 * (end_pos[0] + start_pos[0]):  # More than 20% of average x position
        return 'leg_side'
    elif dx < -0.2 * (end_pos[0] + start_pos[0]):
        return 'off_side'
    else:
        return 'straight'

def estimate_velocity(pos1, pos2, pixels_to_meters, fps=FPS):
    """
    Enhanced velocity estimation with cricket ball requirements validation.
    Cricket ball should have minimum 30kmph velocity (8.33 m/s).
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    
    # Convert to meters per second
    vx = dx * pixels_to_meters * fps
    vy = dy * pixels_to_meters * fps
    
    # Calculate velocity magnitude
    velocity_magnitude = np.sqrt(vx**2 + vy**2)
    
    # Check minimum cricket ball velocity (30 km/h = 8.33 m/s)
    MIN_CRICKET_BALL_VELOCITY = 8.33  # m/s
    
    if velocity_magnitude < MIN_CRICKET_BALL_VELOCITY:
        # This might not be a cricket ball - too slow
        logger.debug(f"Low velocity detected: {velocity_magnitude:.2f} m/s, below cricket ball minimum")
    
    # Estimate z-velocity based on ball size change
    # This is a simplified approach - can be enhanced with better depth estimation
    z_velocity = 0  # Placeholder for z-velocity
    
    return (vx, vy, z_velocity)

def detect_pad_impact(ball_pos, pad_pos, threshold=0.1):
    """Enhanced pad impact detection with better thresholding."""
    distance = np.sqrt(sum((b - p) ** 2 for b, p in zip(ball_pos, pad_pos)))
    return distance < threshold

def validate_cricket_ball_motion(ball_positions: List[Tuple[int, int]], fps: float = 30) -> Dict[str, Any]:
    """
    Validate if detected object meets cricket ball motion requirements:
    - Minimum velocity: 30 km/h (8.33 m/s)
    - Minimum distance: 15 meters
    - Motion consistency across frames
    - Spherical object characteristics
    """
    if len(ball_positions) < 3:
        return {
            'is_valid_cricket_ball': False,
            'reason': 'Insufficient tracking data',
            'velocity_kmh': 0,
            'distance_meters': 0,
            'motion_consistency': False
        }
    
    # Calculate velocities between consecutive positions
    velocities = []
    distances = []
    
    for i in range(1, len(ball_positions)):
        pos1 = ball_positions[i-1]
        pos2 = ball_positions[i]
        
        # Calculate distance in pixels
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        distance_pixels = np.sqrt(dx*dx + dy*dy)
        distances.append(distance_pixels)
        
        # Calculate velocity in m/s (assuming pixels_to_meters = 0.01)
        pixels_to_meters = 0.01  # This should be calibrated properly
        velocity_mps = distance_pixels * pixels_to_meters * fps
        velocities.append(velocity_mps)
    
    # Calculate statistics
    avg_velocity = np.mean(velocities) if velocities else 0
    max_velocity = max(velocities) if velocities else 0
    total_distance = sum(distances) * 0.01  # Convert to meters
    
    # Check cricket ball requirements
    MIN_VELOCITY_KMH = 30.0
    MIN_DISTANCE_METERS = 15.0
    VALIDATION_VELOCITY_KMH = 30.0
    VALIDATION_DISTANCE_METERS = 13.0
    
    velocity_kmh = avg_velocity * 3.6  # Convert to km/h
    max_velocity_kmh = max_velocity * 3.6
    
    # Check motion consistency (velocity should not vary too much)
    velocity_std = np.std(velocities) if len(velocities) > 1 else 0
    motion_consistency = velocity_std < avg_velocity * 0.5  # Velocity should not vary by more than 50%
    
    # Determine if this is a valid cricket ball
    meets_min_velocity = velocity_kmh >= MIN_VELOCITY_KMH
    meets_min_distance = total_distance >= MIN_DISTANCE_METERS
    meets_validation_velocity = max_velocity_kmh >= VALIDATION_VELOCITY_KMH
    meets_validation_distance = total_distance >= VALIDATION_DISTANCE_METERS
    
    is_valid = (meets_min_velocity and meets_min_distance and 
                motion_consistency and len(ball_positions) >= 10)
    
    return {
        'is_valid_cricket_ball': is_valid,
        'velocity_kmh': velocity_kmh,
        'max_velocity_kmh': max_velocity_kmh,
        'distance_meters': total_distance,
        'motion_consistency': motion_consistency,
        'meets_min_velocity': meets_min_velocity,
        'meets_min_distance': meets_min_distance,
        'meets_validation_velocity': meets_validation_velocity,
        'meets_validation_distance': meets_validation_distance,
        'tracking_frames': len(ball_positions),
        'velocity_std': velocity_std
    }

def preprocess_frame(frame):
    """Enhanced preprocessing with histogram equalization and noise reduction."""
    # Convert to LAB color space for better color processing
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    
    # Merge channels back
    lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Apply bilateral filter to reduce noise while preserving edges
    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
    
    return denoised

def create_ball_color_masks(hsv_frame):
    """Create precise HSV color masks for red and white cricket balls."""
    # Red ball masks (cricket balls are typically dark red)
    # Lower red range (0-10)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    
    # Upper red range (160-180)
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    
    # Combine red masks
    mask_red = mask_red1 + mask_red2
    
    # White ball mask (for white cricket balls)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask_white = cv2.inRange(hsv_frame, lower_white, upper_white)
    
    # Combine all ball colors
    ball_mask = mask_red + mask_white
    
    return ball_mask, mask_red, mask_white

def filter_by_circularity(contours, min_circularity=0.7, max_circularity=1.3):
    """
    Enhanced filter for spherical/circular objects with stricter criteria for cricket balls.
    Cricket balls are spherical objects that should have high circularity.
    """
    circular_contours = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 50:  # Increased minimum area for better spherical detection
            continue
            
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
            
        # Calculate circularity: 4π * area / perimeter²
        # Perfect circle = 1.0, cricket ball should be close to this
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        if min_circularity <= circularity <= max_circularity:
            # Additional check: ensure the shape is actually circular
            (x, y), radius = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * radius * radius
            area_ratio = area / circle_area if circle_area > 0 else 0
            
            # Cricket ball should fill most of its enclosing circle
            if area_ratio > 0.6:  # At least 60% of enclosing circle
                circular_contours.append(contour)
    
    return circular_contours

def filter_by_size(contours, min_radius=3, max_radius=20):
    """Filter contours by size to match cricket ball dimensions."""
    size_filtered = []
    
    for contour in contours:
        # Get minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        
        if min_radius <= radius <= max_radius:
            size_filtered.append((contour, (int(x), int(y)), radius))
    
    return size_filtered

def filter_by_motion(candidates, prev_positions, max_motion_distance=50):
    """Filter candidates based on motion consistency."""
    if not prev_positions or len(prev_positions) < 2:
        return candidates
    
    motion_filtered = []
    
    for candidate in candidates:
        contour, (x, y), radius = candidate
        
        # Check if this position is consistent with recent motion
        is_consistent = True
        
        for prev_pos in prev_positions[-2:]:  # Check last 2 positions
            if prev_pos is not None:
                distance = np.sqrt((x - prev_pos[0])**2 + (y - prev_pos[1])**2)
                if distance > max_motion_distance:
                    is_consistent = False
                    break
        
        if is_consistent:
            motion_filtered.append(candidate)
    
    return motion_filtered

def create_roi_mask(frame_shape, roi_percentage=0.6):
    """Create ROI mask to focus on the cricket field area."""
    height, width = frame_shape[:2]
    
    # Define ROI as center portion of the frame
    roi_top = int(height * (1 - roi_percentage) / 2)
    roi_bottom = int(height * (1 + roi_percentage) / 2)
    roi_left = int(width * (1 - roi_percentage) / 2)
    roi_right = int(width * (1 + roi_percentage) / 2)
    
    # Create mask
    mask = np.zeros((height, width), dtype=np.uint8)
    mask[roi_top:roi_bottom, roi_left:roi_right] = 255
    
    return mask, (roi_left, roi_top, roi_right, roi_bottom)

def detect_ball(frame: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Enhanced cricket ball detection with multiple filtering stages:
    1. Preprocessing with histogram equalization
    2. Precise HSV color filtering for red/white balls
    3. Circularity filtering using contour math
    4. Size filtering based on radius
    5. ROI filtering to avoid detection outside field area
    6. Motion filtering for consistency
    7. Exclude detections overlapping with people (player/coach)
    """
    global prev_gray_frame, prev_ball_pos, ball_positions_history
    try:
        # Step 1: Enhanced preprocessing
        processed_frame = preprocess_frame(frame)

        # Step 2: Create ROI mask (pitch area)
        roi_mask, (roi_left, roi_top, roi_right, roi_bottom) = create_roi_mask(frame.shape)

        # Step 3: HSV color filtering
        hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
        ball_mask, red_mask, white_mask = create_ball_color_masks(hsv)

        # Apply ROI mask to color mask
        ball_mask = cv2.bitwise_and(ball_mask, roi_mask)

        # Step 4: Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_CLOSE, kernel)
        ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)

        # Step 5: Find contours
        contours, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return prev_ball_pos

        # Step 6: Circularity filtering
        circular_contours = filter_by_circularity(contours)
        if not circular_contours:
            return prev_ball_pos

        # Step 7: Size filtering
        size_filtered = filter_by_size(circular_contours)
        if not size_filtered:
            return prev_ball_pos

        # Step 8: Motion filtering
        motion_filtered = filter_by_motion(size_filtered, ball_positions_history)
        if not motion_filtered:
            motion_filtered = size_filtered

        # Step 9: Detect people (player/coach) using YOLO
        person_boxes = []
        yolo_results = yolo_model(frame, conf=0.3)
        for result in yolo_results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0].cpu().numpy())
                    # Class 0 is 'person' in COCO/YOLO
                    if cls == 0:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        person_boxes.append((int(x1), int(y1), int(x2), int(y2)))

        # Step 10: Filter out ball candidates overlapping with any person box or outside pitch ROI
        filtered_candidates = []
        for contour, (x, y), radius in motion_filtered:
            # Check if center is inside pitch ROI
            if not (roi_left <= x <= roi_right and roi_top <= y <= roi_bottom):
                continue
            # Check if center is inside any person box
            overlap = False
            for (px1, py1, px2, py2) in person_boxes:
                if px1 <= x <= px2 and py1 <= y <= py2:
                    overlap = True
                    break
            if not overlap:
                filtered_candidates.append((contour, (x, y), radius))

        if not filtered_candidates:
            return prev_ball_pos

        # Step 11: Select best candidate (same as before)
        best_candidate = None
        best_score = -float('inf')
        for contour, (x, y), radius in filtered_candidates:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
            distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            size_score = 1.0 / (1.0 + abs(radius - 8))
            circularity_score = circularity
            position_score = 1.0 / (1.0 + distance_from_center / 100)
            total_score = size_score + circularity_score + position_score
            if total_score > best_score:
                best_score = total_score
                best_candidate = (x, y)

        # Step 12: Validate cricket ball motion and update history
        if best_candidate:
            # Add to history for validation
            ball_positions_history.append(best_candidate)
            if len(ball_positions_history) > max_history_frames:
                ball_positions_history.pop(0)
            
            # Validate if this meets cricket ball requirements
            validation_result = validate_cricket_ball_motion(list(ball_positions_history), FPS)
            
            if validation_result['is_valid_cricket_ball']:
                logger.info(f"Valid cricket ball detected: Vel={validation_result['velocity_kmh']:.1f} km/h, "
                          f"Dist={validation_result['distance_meters']:.1f} m")
            else:
                logger.debug(f"Object detected but doesn't meet cricket ball criteria: "
                           f"Vel={validation_result['velocity_kmh']:.1f} km/h, "
                           f"Dist={validation_result['distance_meters']:.1f} m")
            
            prev_ball_pos = best_candidate
            return best_candidate
        return prev_ball_pos
    except Exception as e:
        logger.error(f"Error in enhanced ball detection: {str(e)}")
        return prev_ball_pos

def track_ball_movement(frames_dir: str, output_path: str) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, Any]]:
    """
    Track ball movement with improved robustness and debug output.
    - Loosen detection constraints
    - Use last known position for up to 5 frames if detection fails
    - Save debug images with detected ball position
    - Build continuous trajectory, only break if missing >5 frames
    """
    try:
        frame_files = [f for f in os.listdir(frames_dir) if f.endswith(('.jpg', '.png'))]
        frame_files.sort()
        if not frame_files:
            logger.warning("No frame files found in directory")
            return [], [], {}

        potential_positions = []
        debug_dir = os.path.join(frames_dir, 'debug_tracking')
        os.makedirs(debug_dir, exist_ok=True)
        last_pos = None
        missing_count = 0
        max_missing = 2  # Only use last known position for up to 2 frames
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)
            if frame is None:
                continue
            ball_pos = detect_ball(frame)
            debug_frame = frame.copy()
            last_unique = potential_positions[-1]['position'] if potential_positions else None
            if ball_pos:
                cv2.circle(debug_frame, tuple(map(int, ball_pos)), 15, (0, 0, 255), 3)
                if last_unique is None or tuple(ball_pos) != tuple(last_unique):
                    potential_positions.append({'frame': i, 'position': ball_pos})
                last_pos = ball_pos
                missing_count = 0
            else:
                if last_pos and missing_count < max_missing:
                    cv2.circle(debug_frame, tuple(map(int, last_pos)), 15, (255, 0, 0), 2)
                    if last_unique is None or tuple(last_pos) != tuple(last_unique):
                        potential_positions.append({'frame': i, 'position': last_pos})
                    missing_count += 1
                else:
                    last_pos = None
                    missing_count = 0
            debug_img_path = os.path.join(debug_dir, f'debug_{i:04d}.jpg')
            cv2.imwrite(debug_img_path, debug_frame)

        # Build continuous trajectory, only break if missing > max_missing
        ball_positions = []
        if len(potential_positions) > 1:
            segment = []
            for idx, pos in enumerate(potential_positions):
                if idx == 0 or np.linalg.norm(np.array(pos['position']) - np.array(potential_positions[idx-1]['position'])) < 200:
                    segment.append(pos)
                else:
                    if len(segment) > len(ball_positions):
                        ball_positions = segment
                    segment = [pos]
            if len(segment) > len(ball_positions):
                ball_positions = segment

        logger.info(f"Ball tracking completed. Found {len(ball_positions)} main delivery positions.")
        tracking_results = {
            "ball_positions": ball_positions,
            "total_frames_processed": len(frame_files),
            "frames_with_ball": len(potential_positions)
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(tracking_results, f, indent=4)
        shot_zones = []
        if ball_positions:
            for i in range(len(ball_positions) - 1):
                start_pos = ball_positions[i]['position']
                end_pos = ball_positions[i + 1]['position']
                zone = classify_shot_zone(start_pos, end_pos)
                shot_zones.append(zone)
        lbw_analysis = analyze_lbw_possibility([pos['position'] for pos in ball_positions]) if ball_positions else {}
        return ball_positions, shot_zones, lbw_analysis
    except Exception as e:
        logger.error(f"Error in ball tracking: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return [], [], {}

def is_non_game_frame(frame: np.ndarray) -> bool:
    # Check if frame is mostly black
    if np.mean(frame) < 20:
        return True
    # Check for Bandicut logo (large blue region in center)
    h, w = frame.shape[:2]
    center_patch = frame[h//2-50:h//2+50, w//2-50:w//2+50]
    mean_b = np.mean(center_patch[:,:,0])
    mean_g = np.mean(center_patch[:,:,1])
    mean_r = np.mean(center_patch[:,:,2])
    if mean_b > 100 and mean_b > mean_g + 30 and mean_b > mean_r + 30:
        return True
    return False

def get_reference_ball_hist(frame: np.ndarray) -> np.ndarray:
    """Extract a reference ball color histogram from the center of the pitch."""
    height, width = frame.shape[:2]
    # Assume ball is near the center of the pitch (tune as needed)
    cx, cy = width // 2, int(0.55 * height)
    r = 8  # radius for patch
    patch = frame[cy - r:cy + r, cx - r:cx + r]
    hsv_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_patch], [0, 1], None, [16, 16], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist

def compare_hist(candidate_patch: np.ndarray, ref_hist: np.ndarray) -> float:
    hsv_patch = cv2.cvtColor(candidate_patch, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv_patch], [0, 1], None, [16, 16], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return cv2.compareHist(hist, ref_hist, cv2.HISTCMP_CORREL)

def analyze_shot_zone(ball_pos: Tuple[int, int], frame_shape: Tuple[int, int, int]) -> str:
    """
    Analyze which zone the ball is in.
    
    Args:
        ball_pos (Tuple[int, int]): Ball position
        frame_shape (Tuple[int, int, int]): Frame dimensions
    
    Returns:
        str: Zone name
    """
    try:
        x, y = ball_pos
        height, width = frame_shape[:2]
        
        # Define zones with more balanced proportions
        zones = {
            'off_side': (width * 0.6, 0, width, height),
            'leg_side': (0, 0, width * 0.4, height),
            'straight': (width * 0.4, 0, width * 0.6, height)
        }
        
        # Check which zone the ball is in
        for zone_name, (x1, y1, x2, y2) in zones.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return zone_name
        
        # If ball is outside defined zones, return unknown
        return 'unknown'
        
    except Exception as e:
        logger.error(f"Error in analyze_shot_zone: {str(e)}")
        return 'unknown'

def check_lbw(ball_pos: Tuple[int, int], frame_shape: Tuple[int, int, int]) -> float:
    """
    Check if there's a possibility of LBW.
    
    Args:
        ball_pos (Tuple[int, int]): Ball position
        frame_shape (Tuple[int, int, int]): Frame dimensions
    
    Returns:
        float: Probability of LBW (0.0 to 1.0)
    """
    try:
        x, y = ball_pos
        height, width = frame_shape[:2]
        
        # Define stumps area (approximate)
        stumps_x = width * 0.5
        stumps_y = height * 0.7
        
        # Calculate distance to stumps
        distance = np.sqrt((x - stumps_x)**2 + (y - stumps_y)**2)
        
        # Convert distance to probability (closer = higher probability)
        max_distance = np.sqrt(width**2 + height**2)
        probability = 1.0 - (distance / max_distance)
        
        return probability
        
    except Exception as e:
        logger.error(f"Error in check_lbw: {str(e)}")
        return 0.0

def analyze_lbw_possibility(ball_positions: List[Tuple[float, float]]) -> Dict[str, Any]:
    """
    Analyze the possibility of an LBW based on ball trajectory.
    
    Args:
        ball_positions: List of ball positions as (x, y) tuples
        
    Returns:
        Dictionary containing LBW analysis results
    """
    try:
        if len(ball_positions) < 2:
            return {
                "lbw_possible": False,
                "impact_point": None,
                "trajectory": None,
                "confidence": 0.0
            }
        
        # Get the last two ball positions
        pos1 = ball_positions[-2]
        pos2 = ball_positions[-1]
        
        # Calculate trajectory
        dx = pos2[0] - pos1[0]  # x coordinate is at index 0
        dy = pos2[1] - pos1[1]  # y coordinate is at index 1
        
        # Check if ball is moving towards the stumps
        # This is a simplified check - in practice, you would use more sophisticated
        # trajectory analysis and consider the player's position
        if abs(dx) < 0.1 and dy > 0:  # Ball moving straight and forward
            return {
                "lbw_possible": True,
                "impact_point": {"x": pos2[0], "y": pos2[1]},
                "trajectory": {
                    "start": {"x": pos1[0], "y": pos1[1]},
                    "end": {"x": pos2[0], "y": pos2[1]},
                    "direction": {"dx": dx, "dy": dy}
                },
                "confidence": 0.7
            }
        
        return {
            "lbw_possible": False,
            "impact_point": None,
            "trajectory": {
                "start": {"x": pos1[0], "y": pos1[1]},
                "end": {"x": pos2[0], "y": pos2[1]},
                "direction": {"dx": dx, "dy": dy}
            },
            "confidence": 0.3
        }
        
    except Exception as e:
        logger.error(f"Error in LBW analysis: {str(e)}")
        return {
            "lbw_possible": False,
            "impact_point": None,
            "trajectory": None,
            "confidence": 0.0
        }

def real_time_ball_tracking(frame: np.ndarray) -> Tuple[Optional[Tuple[int, int]], np.ndarray]:
    """
    Real-time ball tracking that provides immediate feedback with smooth trajectory.
    
    Args:
        frame: Current video frame
        
    Returns:
        Tuple of (ball_position, annotated_frame)
    """
    global real_time_trajectory, tracking_active, last_ball_pos, frame_count
    
    try:
        # Detect ball in current frame
        ball_pos = detect_ball(frame)
        annotated_frame = frame.copy()
        
        # Check if ball is detected and tracking should start
        if ball_pos is not None:
            # Start tracking if not already active
            if not tracking_active:
                tracking_active = True
                real_time_trajectory = []
                logger.info("Ball tracking started - bowler detected!")
            
            # Add current position to trajectory
            real_time_trajectory.append({
                'frame': frame_count,
                'position': ball_pos,
                'timestamp': frame_count / 30.0  # Assuming 30 FPS
            })
            
            last_ball_pos = ball_pos
            
            # Draw ball with bright circle
            cv2.circle(annotated_frame, ball_pos, 12, (0, 255, 255), 3)
            cv2.circle(annotated_frame, ball_pos, 8, (255, 255, 255), -1)
            
        elif tracking_active and last_ball_pos is not None:
            # Ball temporarily lost - use last known position for smooth tracking
            ball_pos = last_ball_pos
            cv2.circle(annotated_frame, ball_pos, 10, (0, 0, 255), 2)  # Red for predicted
            
            # Check if we should stop tracking (ball lost for too long)
            if len(real_time_trajectory) > 0:
                last_detection = real_time_trajectory[-1]['frame']
                if frame_count - last_detection > 10:  # Stop after 10 frames without detection
                    tracking_active = False
                    real_time_trajectory = []
                    last_ball_pos = None
                    logger.info("Ball tracking stopped - ball lost")
        
        # Draw trajectory line if we have enough points
        if len(real_time_trajectory) >= 2:
            # Draw smooth trajectory line
            points = [pos['position'] for pos in real_time_trajectory]
            
            # Draw thick white line for trajectory
            for i in range(1, len(points)):
                cv2.line(annotated_frame, points[i-1], points[i], (255, 255, 255), 3)
            
            # Draw thin colored line overlay for better visibility
            for i in range(1, len(points)):
                color = (0, 255, 0) if i < len(points) - 5 else (0, 255, 255)  # Green to yellow
                cv2.line(annotated_frame, points[i-1], points[i], color, 1)
        
        # Add tracking status text
        status_text = f"Tracking: {'ACTIVE' if tracking_active else 'INACTIVE'}"
        cv2.putText(annotated_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add trajectory length info
        if tracking_active:
            trajectory_info = f"Trajectory: {len(real_time_trajectory)} points"
            cv2.putText(annotated_frame, trajectory_info, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        frame_count += 1
        return ball_pos, annotated_frame
        
    except Exception as e:
        logger.error(f"Error in real-time tracking: {str(e)}")
        return None, frame

def get_real_time_trajectory() -> List[Dict]:
    """Get the current real-time trajectory data."""
    return real_time_trajectory.copy()

def reset_real_time_tracking():
    """Reset real-time tracking state."""
    global real_time_trajectory, tracking_active, last_ball_pos, frame_count
    real_time_trajectory = []
    tracking_active = False
    last_ball_pos = None
    frame_count = 0
