import cv2
import numpy as np
from typing import List, Dict, Any
import logging

# Set up logging
logger = logging.getLogger(__name__)

class BallByBallAnalyzer:
    def __init__(self):
        self.line_categories = ['Off', 'Middle', 'Leg']
        self.length_categories = ['Full', 'Good', 'Short']
        self.ball_types = ['Fast', 'Medium', 'Spin']
        self.result_types = ['Dot', 'Single', 'Boundary', 'Wicket']

    def analyze_ball(self, frame: np.ndarray, ball_positions: List[tuple], 
                    frame_index: int, total_frames: int) -> Dict[str, Any]:
        """Analyze a single ball delivery."""
        # Calculate ball trajectory
        trajectory = self._calculate_trajectory(ball_positions)
        
        if not trajectory['valid']:
            return {
                'type': 'Unknown',
                'line': 'Unknown',
                'length': 'Unknown',
                'pace': 0,
                'result': 'Unknown',
                'strengths': ['No ball tracking data available'],
                'weaknesses': ['Unable to analyze delivery without ball tracking']
            }
        
        # Determine ball type based on speed and movement
        ball_type = self._determine_ball_type(trajectory)
        
        # Analyze line and length
        line = self._analyze_line(trajectory)
        length = self._analyze_length(trajectory)
        
        # Calculate pace
        pace = self._calculate_pace(trajectory)
        
        # Determine result
        result = self._determine_result(trajectory)
        
        # Analyze strengths and weaknesses
        strengths, weaknesses = self._analyze_performance(trajectory, ball_type, line, length)
        
        return {
            'type': ball_type,
            'line': line,
            'length': length,
            'pace': pace,
            'result': result,
            'strengths': strengths,
            'weaknesses': weaknesses
        }

    def _calculate_trajectory(self, positions: List[tuple]) -> Dict[str, Any]:
        """Calculate ball trajectory characteristics."""
        if not positions or len(positions) < 2:
            return {
                'speed': 0,
                'angle': 0,
                'movement': 0,
                'valid': False
            }
        
        # Calculate speed
        distances = []
        for i in range(len(positions) - 1):
            dx = positions[i+1][0] - positions[i][0]
            dy = positions[i+1][1] - positions[i][1]
            distance = np.sqrt(dx*dx + dy*dy)
            distances.append(distance)
        
        avg_speed = np.mean(distances) if distances else 0
        
        # Calculate angle
        start_pos = positions[0]
        end_pos = positions[-1]
        angle = np.arctan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
        
        # Calculate movement (deviation from straight line)
        straight_line = np.linspace(start_pos, end_pos, len(positions))
        deviations = [np.linalg.norm(np.array(p) - np.array(s)) 
                     for p, s in zip(positions, straight_line)]
        movement = np.mean(deviations) if deviations else 0
        
        return {
            'speed': avg_speed,
            'angle': angle,
            'movement': movement,
            'valid': True
        }

    def _determine_ball_type(self, trajectory: Dict[str, Any]) -> str:
        """Determine the type of ball based on trajectory characteristics."""
        if trajectory['movement'] > 5:
            return 'Spin'
        elif trajectory['speed'] > 30:
            return 'Fast'
        else:
            return 'Medium'

    def _analyze_line(self, trajectory: Dict[str, Any]) -> str:
        """Analyze the line of the delivery."""
        angle = trajectory['angle']
        if angle < -0.5:
            return 'Leg'
        elif angle > 0.5:
            return 'Off'
        else:
            return 'Middle'

    def _analyze_length(self, trajectory: Dict[str, Any]) -> str:
        """Analyze the length of the delivery."""
        speed = trajectory['speed']
        if speed < 20:
            return 'Full'
        elif speed < 40:
            return 'Good'
        else:
            return 'Short'

    def _calculate_pace(self, trajectory: Dict[str, Any]) -> float:
        """Calculate the pace of the delivery in km/h."""
        # Convert pixel speed to km/h (approximate conversion)
        return trajectory['speed'] * 2.5

    def _determine_result(self, trajectory: Dict[str, Any]) -> str:
        """Determine the result of the delivery."""
        # This would typically involve more complex analysis
        # For now, we'll use a simple random distribution
        return np.random.choice(self.result_types)

    def _analyze_performance(self, trajectory: Dict[str, Any], 
                           ball_type: str, line: str, length: str) -> tuple:
        """Analyze strengths and weaknesses of the delivery."""
        strengths = []
        weaknesses = []
        
        # Analyze speed consistency
        if trajectory['speed'] > 25:
            strengths.append("Good pace maintained")
        else:
            weaknesses.append("Pace could be improved")
        
        # Analyze line accuracy
        if line == 'Middle':
            strengths.append("Good line control")
        else:
            weaknesses.append("Line could be more consistent")
        
        # Analyze length
        if length == 'Good':
            strengths.append("Optimal length")
        else:
            weaknesses.append(f"Length could be adjusted ({length} delivery)")
        
        # Analyze movement
        if ball_type == 'Spin' and trajectory['movement'] > 5:
            strengths.append("Good spin and drift")
        elif ball_type == 'Fast' and trajectory['movement'] < 2:
            strengths.append("Good seam position")
        else:
            weaknesses.append("Could improve ball movement")
        
        return strengths, weaknesses

def analyze_ball_by_ball(video_path: str, ball_positions: List[List[tuple]]) -> List[Dict[str, Any]]:
    """Analyze a video ball by ball based on actual tracked ball positions."""
    try:
        logger.info(f"Starting ball-by-ball analysis for video: {video_path}")
        analyzer = BallByBallAnalyzer()
        
        ball_analysis = []
        
        # If we have ball positions, analyze them
        if ball_positions and len(ball_positions) > 0:
            # For each delivery (each list of positions)
            for delivery_index, positions in enumerate(ball_positions):
                if positions and len(positions) > 0:
                    # Analyze this delivery
                    analysis = analyzer.analyze_ball(
                        frame=None,  # We don't need the frame for position-based analysis
                        ball_positions=positions,
                        frame_index=delivery_index,
                        total_frames=len(positions)
                    )
                    ball_analysis.append(analysis)
                    logger.info(f"Analyzed delivery {delivery_index + 1} with {len(positions)} positions")
                else:
                    # Empty delivery - create a default analysis
                    analysis = analyzer.analyze_ball(
                        frame=None,
                        ball_positions=[],
                        frame_index=delivery_index,
                        total_frames=0
                    )
                    ball_analysis.append(analysis)
        else:
            # No ball positions available - create a single default analysis
            logger.warning("No ball positions available for analysis")
            analysis = analyzer.analyze_ball(
                frame=None,
                ball_positions=[],
                frame_index=0,
                total_frames=0
            )
            ball_analysis.append(analysis)
        
        logger.info(f"Completed ball-by-ball analysis. Analyzed {len(ball_analysis)} deliveries.")
        return ball_analysis
        
    except Exception as e:
        logger.error(f"Error in ball-by-ball analysis: {str(e)}")
        return []

# Make the function available at module level
__all__ = ['analyze_ball_by_ball'] 