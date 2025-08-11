import cv2
import numpy as np
import json
import os
from typing import List, Tuple, Dict, Any, Optional
from lbw_predictor import LBWPredictor, BallState
import logging

logger = logging.getLogger(__name__)

class HawkeyeVisualization:
    """
    Hawkeye-style ball tracking visualization with LBW prediction.
    Provides real-time ball trajectory visualization and LBW decision support.
    """
    
    def __init__(self):
        self.lbw_predictor = LBWPredictor()
        self.trajectory_points = []
        self.predicted_trajectory = []
        self.lbw_decision = None
        self.frame_width = 1920
        self.frame_height = 1080
        
        # Visualization settings
        self.trajectory_color = (255, 255, 255)  # White line
        self.predicted_color = (0, 255, 255)     # Yellow for predicted path
        self.lbw_color = (0, 0, 255)             # Red for LBW
        self.ball_color = (255, 255, 255)        # White ball
        self.stumps_color = (0, 255, 0)          # Green stumps
        
        # Line thickness
        self.trajectory_thickness = 3
        self.predicted_thickness = 2
        self.ball_radius = 8
        
    def set_frame_dimensions(self, width: int, height: int):
        """Set frame dimensions for proper scaling."""
        self.frame_width = width
        self.frame_height = height
    
    def add_ball_position(self, position: Tuple[int, int], frame_number: int):
        """Add a new ball position to the trajectory."""
        self.trajectory_points.append({
            'position': position,
            'frame': frame_number,
            'timestamp': frame_number / 30.0  # Assuming 30 FPS
        })
        
        # Update LBW predictor if we have enough points
        if len(self.trajectory_points) >= 3:
            self._update_lbw_prediction()
    
    def _update_lbw_prediction(self):
        """Update LBW prediction based on current trajectory."""
        if len(self.trajectory_points) < 3:
            return
        
        # Get recent positions
        recent_points = self.trajectory_points[-3:]
        
        # Calculate velocities
        velocities = []
        for i in range(1, len(recent_points)):
            prev_pos = recent_points[i-1]['position']
            curr_pos = recent_points[i]['position']
            
            # Convert to 3D coordinates (assuming z=0 for 2D tracking)
            prev_3d = (prev_pos[0], prev_pos[1], 0)
            curr_3d = (curr_pos[0], curr_pos[1], 0)
            
            # Calculate velocity (pixels per frame)
            vx = (curr_3d[0] - prev_3d[0]) * 30  # Convert to pixels per second
            vy = (curr_3d[1] - prev_3d[1]) * 30
            vz = 0
            
            velocities.append((vx, vy, vz))
        
        # Add ball state to predictor
        latest_pos = recent_points[-1]['position']
        latest_vel = velocities[-1]
        
        self.lbw_predictor.add_ball_state(
            position=(latest_pos[0], latest_pos[1], 0),
            velocity=latest_vel,
            timestamp=recent_points[-1]['timestamp']
        )
        
        # Predict trajectory
        if len(self.lbw_predictor.ball_states) > 0:
            latest_state = self.lbw_predictor.ball_states[-1]
            self.predicted_trajectory = self.lbw_predictor.predict_trajectory(latest_state)
    
    def analyze_lbw(self, pad_impact_position: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
        """Analyze LBW possibility and return decision."""
        if len(self.trajectory_points) < 3:
            return {
                'lbw_possible': False,
                'confidence': 0.0,
                'decision': 'Not enough data',
                'impact_point': None,
                'stump_hit': None
            }
        
        # Get latest ball position
        latest_pos = self.trajectory_points[-1]['position']
        
        # Convert to 3D coordinates
        ball_3d = (latest_pos[0], latest_pos[1], 0)
        pad_3d = pad_impact_position if pad_impact_position else (latest_pos[0], latest_pos[1], 0)
        
        # Check for pad impact
        pad_impact = self.lbw_predictor.detect_pad_impact(ball_3d, pad_3d)
        
        if pad_impact and self.predicted_trajectory:
            # Check if predicted trajectory hits stumps
            hits_stumps, stump_hit, confidence = self.lbw_predictor.check_stump_intersection(
                self.predicted_trajectory
            )
            
            if hits_stumps:
                self.lbw_decision = {
                    'lbw_possible': True,
                    'confidence': confidence,
                    'decision': 'OUT' if confidence > 0.7 else 'UMPIRE\'S CALL',
                    'impact_point': latest_pos,
                    'stump_hit': stump_hit,
                    'trajectory': self.predicted_trajectory
                }
            else:
                self.lbw_decision = {
                    'lbw_possible': True,
                    'confidence': confidence,
                    'decision': 'NOT OUT',
                    'impact_point': latest_pos,
                    'stump_hit': 'none',
                    'trajectory': self.predicted_trajectory
                }
        else:
            self.lbw_decision = {
                'lbw_possible': False,
                'confidence': 0.0,
                'decision': 'No pad impact detected',
                'impact_point': None,
                'stump_hit': None
            }
        
        return self.lbw_decision
    
    def draw_trajectory(self, frame: np.ndarray) -> np.ndarray:
        """Draw the ball direction (last two positions) on the frame."""
        if len(self.trajectory_points) < 2:
            return frame
        # Only use the last two points for direction
        points = [point['position'] for point in self.trajectory_points[-2:]]
        points = np.array(points, dtype=np.int32)
        cv2.polylines(frame, [points], False, self.trajectory_color, self.trajectory_thickness)
        # Draw ball at current position
        if self.trajectory_points:
            current_pos = self.trajectory_points[-1]['position']
            cv2.circle(frame, current_pos, self.ball_radius, self.ball_color, -1)
            cv2.circle(frame, current_pos, self.ball_radius, (0, 0, 0), 2)  # Black border
        return frame
    
    def draw_predicted_trajectory(self, frame: np.ndarray) -> np.ndarray:
        """Draw the predicted trajectory on the frame."""
        if not self.predicted_trajectory:
            return frame
        
        # Convert 3D trajectory to 2D points
        predicted_points = []
        for point in self.predicted_trajectory:
            x, y, z = point
            # Convert to pixel coordinates (assuming z=0 for 2D)
            pixel_x = int(x)
            pixel_y = int(y)
            predicted_points.append((pixel_x, pixel_y))
        
        if len(predicted_points) >= 2:
            predicted_points = np.array(predicted_points, dtype=np.int32)
            cv2.polylines(frame, [predicted_points], False, self.predicted_color, self.predicted_thickness)
        
        return frame
    
    def draw_stumps(self, frame: np.ndarray) -> np.ndarray:
        """Draw the stumps on the frame."""
        # Stumps position (bottom center of frame)
        stumps_x = self.frame_width // 2
        stumps_y = int(self.frame_height * 0.8)  # 80% down the frame
        
        # Draw stumps (three vertical lines)
        stump_width = 20
        stump_height = 60
        
        # Off stump
        cv2.line(frame, 
                (stumps_x - stump_width, stumps_y), 
                (stumps_x - stump_width, stumps_y - stump_height), 
                self.stumps_color, 3)
        
        # Middle stump
        cv2.line(frame, 
                (stumps_x, stumps_y), 
                (stumps_x, stumps_y - stump_height), 
                self.stumps_color, 3)
        
        # Leg stump
        cv2.line(frame, 
                (stumps_x + stump_width, stumps_y), 
                (stumps_x + stump_width, stumps_y - stump_height), 
                self.stumps_color, 3)
        
        # Draw bails
        cv2.line(frame, 
                (stumps_x - stump_width, stumps_y - stump_height), 
                (stumps_x + stump_width, stumps_y - stump_height), 
                self.stumps_color, 3)
        
        return frame
    
    def draw_lbw_decision(self, frame: np.ndarray) -> np.ndarray:
        """Draw LBW decision information on the frame."""
        if not self.lbw_decision:
            return frame
        
        # Draw decision text
        decision = self.lbw_decision['decision']
        confidence = self.lbw_decision['confidence']
        
        # Set text properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        thickness = 3
        
        # Determine text color based on decision
        if decision == 'OUT':
            text_color = (0, 0, 255)  # Red
        elif decision == 'NOT OUT':
            text_color = (0, 255, 0)  # Green
        else:
            text_color = (0, 255, 255)  # Yellow
        
        # Draw decision text
        text = f"{decision} ({confidence:.2f})"
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (self.frame_width - text_size[0]) // 2
        text_y = 100
        
        # Draw text background
        cv2.rectangle(frame, 
                     (text_x - 10, text_y - text_size[1] - 10),
                     (text_x + text_size[0] + 10, text_y + 10),
                     (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, thickness)
        
        # Draw stump hit information
        if self.lbw_decision['stump_hit'] and self.lbw_decision['stump_hit'] != 'none':
            stump_text = f"Hit: {self.lbw_decision['stump_hit'].upper()} stump"
            stump_text_size = cv2.getTextSize(stump_text, font, 1.0, 2)[0]
            stump_text_x = (self.frame_width - stump_text_size[0]) // 2
            stump_text_y = text_y + 50
            
            cv2.putText(frame, stump_text, (stump_text_x, stump_text_y), 
                       font, 1.0, text_color, 2)
        
        return frame
    
    def process_frame(self, frame: np.ndarray, ball_position: Optional[Tuple[int, int]] = None, 
                     frame_number: int = 0) -> np.ndarray:
        """Process a frame and add ball tracking visualization."""
        # Set frame dimensions
        height, width = frame.shape[:2]
        self.set_frame_dimensions(width, height)
        
        # Add ball position if provided
        if ball_position:
            self.add_ball_position(ball_position, frame_number)
        
        # Draw all visualizations
        frame = self.draw_stumps(frame)
        frame = self.draw_trajectory(frame)
        frame = self.draw_predicted_trajectory(frame)
        frame = self.draw_lbw_decision(frame)
        
        return frame
    
    def get_trajectory_data(self) -> Dict[str, Any]:
        """Get trajectory data for export or analysis."""
        return {
            'trajectory_points': self.trajectory_points,
            'predicted_trajectory': self.predicted_trajectory,
            'lbw_decision': self.lbw_decision,
            'frame_count': len(self.trajectory_points)
        }
    
    def reset(self):
        """Reset the visualization state."""
        self.trajectory_points = []
        self.predicted_trajectory = []
        self.lbw_decision = None
        self.lbw_predictor = LBWPredictor()

def create_hawkeye_video(input_frames_dir: str, output_video_path: str, 
                        ball_positions: List[Dict[str, Any]]) -> str:
    """
    Create a Hawkeye-style video with ball trajectory visualization.
    Accepts ball_positions as a list of dictionaries with frame indices.
    """
    try:
        # Initialize Hawkeye visualization
        hawkeye = HawkeyeVisualization()
        
        # --- Create a lookup map for ball positions ---
        positions_map = {item['frame']: item['position'] for item in ball_positions}
        
        # Get frame files
        frame_files = sorted([f for f in os.listdir(input_frames_dir) 
                            if f.endswith(('.jpg', '.png', '.jpeg'))])
        
        if not frame_files:
            raise ValueError("No frame files found in input directory")
        
        # Read first frame to get dimensions
        first_frame_path = os.path.join(input_frames_dir, frame_files[0])
        first_frame = cv2.imread(first_frame_path)
        
        if first_frame is None:
            raise ValueError("Failed to load first frame")
        
        height, width = first_frame.shape[:2]
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))
        
        # Process each frame
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(input_frames_dir, frame_file)
            frame = cv2.imread(frame_path)
            
            if frame is None:
                logger.warning(f"Failed to load frame: {frame_path}")
                continue
            
            # --- Get ball position for this specific frame from the map ---
            ball_position = positions_map.get(i)
            
            # Process frame with Hawkeye visualization
            # The Hawkeye class will handle drawing only when a position is available
            processed_frame = hawkeye.process_frame(frame, ball_position, i)
            
            # Write frame to video
            out.write(processed_frame)
        
        # Release video writer
        out.release()
        
        logger.info(f"Hawkeye video created: {output_video_path}")
        return output_video_path
        
    except Exception as e:
        logger.error(f"Error creating Hawkeye video: {str(e)}")
        raise

def analyze_delivery_with_hawkeye(frames_dir: str, output_dir: str) -> Dict[str, Any]:
    """
    Analyze a cricket delivery using Hawkeye visualization.
    """
    try:
        # Track ball movement
        from track_ball import track_ball_movement
        
        tracking_output = os.path.join(output_dir, 'tracking_results.json')
        # This now returns a list of dicts: [{'frame': int, 'position': (x, y)}, ...]
        ball_positions_data, shot_zones, lbw_analysis = track_ball_movement(frames_dir, tracking_output)
        
        # Create Hawkeye visualization
        hawkeye = HawkeyeVisualization()
        
        # Add ball positions to Hawkeye
        for item in ball_positions_data:
            hawkeye.add_ball_position(item['position'], item['frame'])
        
        # Analyze LBW
        lbw_result = hawkeye.analyze_lbw()
        
        # Create Hawkeye video
        video_output = os.path.join(output_dir, 'hawkeye_analysis.mp4')
        # Pass the structured data directly to the video creation function
        create_hawkeye_video(frames_dir, video_output, ball_positions_data)
        
        # Get trajectory data
        trajectory_data = hawkeye.get_trajectory_data()
        
        # Compile results
        results = {
            'ball_positions': [item['position'] for item in ball_positions_data], # Keep original format for response if needed
            'shot_zones': shot_zones,
            'lbw_analysis': lbw_analysis,
            'hawkeye_lbw_result': lbw_result,
            'trajectory_data': trajectory_data,
            'video_path': video_output,
            'total_frames': len(ball_positions_data)
        }
        
        # Save results
        results_file = os.path.join(output_dir, 'hawkeye_analysis.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"Hawkeye analysis completed. Results saved to: {results_file}")
        return results
        
    except Exception as e:
        logger.error(f"Error in Hawkeye analysis: {str(e)}")
        raise 