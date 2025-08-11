import cv2
import numpy as np
import json
import os
from typing import Tuple, Optional

class BallDetectionCalibrator:
    """
    Real-time calibration tool for cricket ball detection parameters.
    Allows tuning of HSV values, circularity thresholds, size ranges, and motion parameters.
    """
    
    def __init__(self):
        self.hsv_ranges = {
            'red_lower1': [0, 100, 100],
            'red_upper1': [10, 255, 255],
            'red_lower2': [160, 100, 100],
            'red_upper2': [180, 255, 255],
            'white_lower': [0, 0, 200],
            'white_upper': [180, 30, 255]
        }
        
        self.detection_params = {
            'min_circularity': 0.6,
            'max_circularity': 1.4,
            'min_radius': 3,
            'max_radius': 20,
            'max_motion_distance': 50,
            'roi_percentage': 0.6
        }
        
        self.window_name = 'Cricket Ball Detection Calibrator'
        self.trackbar_window = 'Parameters'
        
        # Create windows
        cv2.namedWindow(self.window_name)
        cv2.namedWindow(self.trackbar_window)
        
        self._create_trackbars()
        
    def _create_trackbars(self):
        """Create trackbars for all adjustable parameters."""
        
        # HSV Red Range 1
        cv2.createTrackbar('Red1 H Lower', self.trackbar_window, self.hsv_ranges['red_lower1'][0], 180, lambda x: self._update_hsv('red_lower1', 0, x))
        cv2.createTrackbar('Red1 S Lower', self.trackbar_window, self.hsv_ranges['red_lower1'][1], 255, lambda x: self._update_hsv('red_lower1', 1, x))
        cv2.createTrackbar('Red1 V Lower', self.trackbar_window, self.hsv_ranges['red_lower1'][2], 255, lambda x: self._update_hsv('red_lower1', 2, x))
        cv2.createTrackbar('Red1 H Upper', self.trackbar_window, self.hsv_ranges['red_upper1'][0], 180, lambda x: self._update_hsv('red_upper1', 0, x))
        cv2.createTrackbar('Red1 S Upper', self.trackbar_window, self.hsv_ranges['red_upper1'][1], 255, lambda x: self._update_hsv('red_upper1', 1, x))
        cv2.createTrackbar('Red1 V Upper', self.trackbar_window, self.hsv_ranges['red_upper1'][2], 255, lambda x: self._update_hsv('red_upper1', 2, x))
        
        # HSV Red Range 2
        cv2.createTrackbar('Red2 H Lower', self.trackbar_window, self.hsv_ranges['red_lower2'][0], 180, lambda x: self._update_hsv('red_lower2', 0, x))
        cv2.createTrackbar('Red2 S Lower', self.trackbar_window, self.hsv_ranges['red_lower2'][1], 255, lambda x: self._update_hsv('red_lower2', 1, x))
        cv2.createTrackbar('Red2 V Lower', self.trackbar_window, self.hsv_ranges['red_lower2'][2], 255, lambda x: self._update_hsv('red_lower2', 2, x))
        cv2.createTrackbar('Red2 H Upper', self.trackbar_window, self.hsv_ranges['red_upper2'][0], 180, lambda x: self._update_hsv('red_upper2', 0, x))
        cv2.createTrackbar('Red2 S Upper', self.trackbar_window, self.hsv_ranges['red_upper2'][1], 255, lambda x: self._update_hsv('red_upper2', 1, x))
        cv2.createTrackbar('Red2 V Upper', self.trackbar_window, self.hsv_ranges['red_upper2'][2], 255, lambda x: self._update_hsv('red_upper2', 2, x))
        
        # HSV White Range
        cv2.createTrackbar('White H Lower', self.trackbar_window, self.hsv_ranges['white_lower'][0], 180, lambda x: self._update_hsv('white_lower', 0, x))
        cv2.createTrackbar('White S Lower', self.trackbar_window, self.hsv_ranges['white_lower'][1], 255, lambda x: self._update_hsv('white_lower', 1, x))
        cv2.createTrackbar('White V Lower', self.trackbar_window, self.hsv_ranges['white_lower'][2], 255, lambda x: self._update_hsv('white_lower', 2, x))
        cv2.createTrackbar('White H Upper', self.trackbar_window, self.hsv_ranges['white_upper'][0], 180, lambda x: self._update_hsv('white_upper', 0, x))
        cv2.createTrackbar('White S Upper', self.trackbar_window, self.hsv_ranges['white_upper'][1], 255, lambda x: self._update_hsv('white_upper', 1, x))
        cv2.createTrackbar('White V Upper', self.trackbar_window, self.hsv_ranges['white_upper'][2], 255, lambda x: self._update_hsv('white_upper', 2, x))
        
        # Detection Parameters
        cv2.createTrackbar('Min Circularity', self.trackbar_window, int(self.detection_params['min_circularity'] * 100), 200, lambda x: self._update_param('min_circularity', x / 100))
        cv2.createTrackbar('Max Circularity', self.trackbar_window, int(self.detection_params['max_circularity'] * 100), 200, lambda x: self._update_param('max_circularity', x / 100))
        cv2.createTrackbar('Min Radius', self.trackbar_window, self.detection_params['min_radius'], 50, lambda x: self._update_param('min_radius', x))
        cv2.createTrackbar('Max Radius', self.trackbar_window, self.detection_params['max_radius'], 50, lambda x: self._update_param('max_radius', x))
        cv2.createTrackbar('Max Motion Distance', self.trackbar_window, self.detection_params['max_motion_distance'], 200, lambda x: self._update_param('max_motion_distance', x))
        cv2.createTrackbar('ROI Percentage', self.trackbar_window, int(self.detection_params['roi_percentage'] * 100), 100, lambda x: self._update_param('roi_percentage', x / 100))
    
    def _update_hsv(self, key: str, index: int, value: int):
        """Update HSV range values."""
        if key in self.hsv_ranges:
            self.hsv_ranges[key][index] = value
    
    def _update_param(self, key: str, value: float):
        """Update detection parameter values."""
        if key in self.detection_params:
            self.detection_params[key] = value
    
    def create_ball_color_masks(self, hsv_frame):
        """Create color masks using current HSV ranges."""
        # Red ball masks
        lower_red1 = np.array(self.hsv_ranges['red_lower1'])
        upper_red1 = np.array(self.hsv_ranges['red_upper1'])
        mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        
        lower_red2 = np.array(self.hsv_ranges['red_lower2'])
        upper_red2 = np.array(self.hsv_ranges['red_upper2'])
        mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        
        mask_red = mask_red1 + mask_red2
        
        # White ball mask
        lower_white = np.array(self.hsv_ranges['white_lower'])
        upper_white = np.array(self.hsv_ranges['white_upper'])
        mask_white = cv2.inRange(hsv_frame, lower_white, upper_white)
        
        ball_mask = mask_red + mask_white
        
        return ball_mask, mask_red, mask_white
    
    def filter_by_circularity(self, contours):
        """Filter contours by circularity using current parameters."""
        circular_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 20:
                continue
                
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
                
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if (self.detection_params['min_circularity'] <= 
                circularity <= self.detection_params['max_circularity']):
                circular_contours.append(contour)
        
        return circular_contours
    
    def filter_by_size(self, contours):
        """Filter contours by size using current parameters."""
        size_filtered = []
        
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            
            if (self.detection_params['min_radius'] <= 
                radius <= self.detection_params['max_radius']):
                size_filtered.append((contour, (int(x), int(y)), radius))
        
        return size_filtered
    
    def create_roi_mask(self, frame_shape):
        """Create ROI mask using current percentage."""
        height, width = frame_shape[:2]
        
        roi_top = int(height * (1 - self.detection_params['roi_percentage']) / 2)
        roi_bottom = int(height * (1 + self.detection_params['roi_percentage']) / 2)
        roi_left = int(width * (1 - self.detection_params['roi_percentage']) / 2)
        roi_right = int(width * (1 + self.detection_params['roi_percentage']) / 2)
        
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[roi_top:roi_bottom, roi_left:roi_right] = 255
        
        return mask, (roi_left, roi_top, roi_right, roi_bottom)
    
    def detect_ball(self, frame):
        """Enhanced ball detection with current parameters."""
        try:
            # Preprocessing
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            lab = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            processed_frame = cv2.bilateralFilter(enhanced, 9, 75, 75)
            
            # Create ROI mask
            roi_mask, (roi_left, roi_top, roi_right, roi_bottom) = self.create_roi_mask(frame.shape)
            
            # HSV color filtering
            hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
            ball_mask, red_mask, white_mask = self.create_ball_color_masks(hsv)
            
            # Apply ROI mask
            ball_mask = cv2.bitwise_and(ball_mask, roi_mask)
            
            # Morphological operations
            kernel = np.ones((3, 3), np.uint8)
            ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_CLOSE, kernel)
            ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Circularity filtering
            circular_contours = self.filter_by_circularity(contours)
            
            if not circular_contours:
                return None
            
            # Size filtering
            size_filtered = self.filter_by_size(circular_contours)
            
            if not size_filtered:
                return None
            
            # Select best candidate
            best_candidate = None
            best_score = -float('inf')
            
            for contour, (x, y), radius in size_filtered:
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
            
            return best_candidate
            
        except Exception as e:
            print(f"Error in ball detection: {e}")
            return None
    
    def process_frame(self, frame):
        """Process frame and return visualization."""
        # Detect ball
        ball_pos = self.detect_ball(frame)
        
        # Create visualization
        vis_frame = frame.copy()
        
        # Draw ROI
        roi_mask, (roi_left, roi_top, roi_right, roi_bottom) = self.create_roi_mask(frame.shape)
        cv2.rectangle(vis_frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
        
        # Draw detected ball
        if ball_pos:
            cv2.circle(vis_frame, ball_pos, 15, (0, 0, 255), 3)
            cv2.putText(vis_frame, f'Ball: {ball_pos}', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Create color mask visualization
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ball_mask, red_mask, white_mask = self.create_ball_color_masks(hsv)
        
        # Apply ROI to mask
        roi_mask, _ = self.create_roi_mask(frame.shape)
        ball_mask = cv2.bitwise_and(ball_mask, roi_mask)
        
        # Convert mask to BGR for display
        mask_display = cv2.cvtColor(ball_mask, cv2.COLOR_GRAY2BGR)
        
        # Combine original and mask
        combined = np.hstack([vis_frame, mask_display])
        
        return combined, ball_pos
    
    def save_parameters(self, filename='ball_detection_params.json'):
        """Save current parameters to file."""
        params = {
            'hsv_ranges': self.hsv_ranges,
            'detection_params': self.detection_params
        }
        
        with open(filename, 'w') as f:
            json.dump(params, f, indent=4)
        
        print(f"Parameters saved to {filename}")
    
    def load_parameters(self, filename='ball_detection_params.json'):
        """Load parameters from file."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                params = json.load(f)
            
            self.hsv_ranges = params.get('hsv_ranges', self.hsv_ranges)
            self.detection_params = params.get('detection_params', self.detection_params)
            
            print(f"Parameters loaded from {filename}")
    
    def run_calibration(self, video_source=0):
        """Run the calibration tool with live video."""
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print("Error: Could not open video source")
            return
        
        print("Cricket Ball Detection Calibrator")
        print("Controls:")
        print("- Press 's' to save parameters")
        print("- Press 'l' to load parameters")
        print("- Press 'q' to quit")
        print("- Adjust trackbars to tune detection")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            vis_frame, ball_pos = self.process_frame(frame)
            
            # Display
            cv2.imshow(self.window_name, vis_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.save_parameters()
            elif key == ord('l'):
                self.load_parameters()
        
        cap.release()
        cv2.destroyAllWindows()

def main():
    """Main function to run the calibrator."""
    calibrator = BallDetectionCalibrator()
    
    # Try to load existing parameters
    calibrator.load_parameters()
    
    # Run calibration
    calibrator.run_calibration()

if __name__ == "__main__":
    main() 