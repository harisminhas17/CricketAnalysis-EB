import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
import time

logger = logging.getLogger(__name__)

@dataclass
class Feedback:
    """Class to store feedback information."""
    message: str
    confidence: float
    category: str
    timestamp: float = field(default_factory=time.time)

class RealTimeFeedback:
    def __init__(self):
        """Initialize the real-time feedback system."""
        self.feedback_history = []
        self.last_feedback_time = 0.0
        self.feedback_cooldown = 2.0  # seconds between feedback messages
        
    def analyze_frame(self, frame: np.ndarray, player_position: Optional[Tuple[float, float]], 
                     ball_position: Optional[Tuple[float, float]], shot_zone: Optional[str]) -> List[Feedback]:
        """
        Analyze a single frame and generate real-time feedback.
        
        Args:
            frame: The video frame to analyze
            player_position: Tuple containing player position (x, y)
            ball_position: Tuple containing ball position (x, y)
            shot_zone: String indicating the shot zone
            
        Returns:
            List of Feedback objects containing analysis results
        """
        feedback_list = []
        
        # Check feedback cooldown
        current_time = time.time()
        if current_time - self.last_feedback_time < self.feedback_cooldown:
            return feedback_list
        
        # Analyze player position
        if player_position:
            # Check stance
            stance_feedback = self.analyze_stance(player_position)
            if stance_feedback:
                feedback_list.append(stance_feedback)
            
            # Check balance
            balance_feedback = self.analyze_balance(player_position)
            if balance_feedback:
                feedback_list.append(balance_feedback)
        
        # Analyze ball position and shot selection
        if ball_position and shot_zone:
            # Check shot selection
            shot_feedback = self.analyze_shot_selection(ball_position, shot_zone)
            if shot_feedback:
                feedback_list.append(shot_feedback)
            
            # Check timing
            timing_feedback = self.analyze_timing(ball_position, player_position)
            if timing_feedback:
                feedback_list.append(timing_feedback)
        
        # Analyze overall technique
        technique_feedback = self.analyze_technique(frame, player_position, ball_position)
        if technique_feedback:
            feedback_list.append(technique_feedback)
        
        # Update feedback history and last feedback time
        if feedback_list:
            self.feedback_history.extend(feedback_list)
            self.last_feedback_time = current_time
        
        return feedback_list
            
    def _analyze_technique(self, frame: np.ndarray, player_position: Optional[Tuple[float, float]], 
                          ball_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """
        Analyze batting technique and provide feedback.
        
        Args:
            frame: The video frame to analyze
            player_position: Tuple containing player position (x, y)
            ball_position: Tuple containing ball position (x, y)
            
        Returns:
            Feedback object if technique issues are detected, None otherwise
        """
        try:
            if player_position is None or ball_position is None:
                return None
                
            # Check head position
            if player_position[1] < 0.2:  # Head too low
                return Feedback(
                    message="Keep your head up and eyes level",
                    confidence=0.8,
                    category="technique"
                )
            
            # Check foot movement
            if abs(ball_position[0] - player_position[0]) > 0.3:
                return Feedback(
                    message="Move your feet to get into position",
                    confidence=0.7,
                    category="technique"
                )
            
            # Check bat position
            if ball_position[1] > 0.8 and player_position[1] < 0.3:
                return Feedback(
                    message="Get your bat down earlier",
                    confidence=0.75,
                    category="technique"
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error in technique analysis: {str(e)}")
            return None
            
    def _analyze_fitness(self, player_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """
        Analyze player's fitness and movement patterns.
        
        Args:
            player_position: Tuple containing player position (x, y)
            
        Returns:
            Feedback object if fitness issues are detected, None otherwise
        """
        try:
            if player_position is None:
                return None
                
            # Check if player is moving efficiently
            if abs(player_position[0]) > 0.4:  # Too much lateral movement
                return Feedback(
                    message="Focus on efficient movement patterns",
                    confidence=0.7,
                    category="fitness"
                )
            return None
            
        except Exception as e:
            logger.error(f"Error in fitness analysis: {str(e)}")
            return None
            
    def _analyze_strategy(self, shot_zone: Optional[str], ball_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """
        Analyze batting strategy and shot selection.
        
        Args:
            shot_zone: String indicating the shot zone
            ball_position: Tuple containing ball position (x, y)
            
        Returns:
            Feedback object if strategy issues are detected, None otherwise
        """
        try:
            if shot_zone is None or ball_position is None:
                return None
                
            # Check if shot selection is appropriate
            if shot_zone == "off_side" and ball_position[0] < 0.3:
                return Feedback(
                    message="Consider playing straighter for this delivery",
                    confidence=0.8,
                    category="strategy"
                )
            return None
            
        except Exception as e:
            logger.error(f"Error in strategy analysis: {str(e)}")
            return None
            
    def _analyze_footwork(self, frame: np.ndarray, player_position: Optional[Tuple[float, float]]) -> float:
        """
        Analyze player's footwork.
        
        Args:
            frame: The video frame to analyze
            player_position: Tuple containing player position (x, y)
            
        Returns:
            Float score between 0 and 1 indicating footwork quality
        """
        try:
            if player_position is None:
                return 0.0
                
            # Check if player is in a good position
            if abs(player_position[0]) < 0.2:
                return 0.8  # Good footwork
            return 0.4  # Needs improvement
            
        except Exception as e:
            logger.error(f"Error in footwork analysis: {str(e)}")
            return 0.0

    def _analyze_bat_swing(self, frame: np.ndarray, player_position: Optional[Tuple[float, float]]) -> float:
        """
        Analyze player's bat swing.
        
        Args:
            frame: The video frame to analyze
            player_position: Tuple containing player position (x, y)
            
        Returns:
            Float score between 0 and 1 indicating bat swing quality
        """
        try:
            if player_position is None:
                return 0.0
                
            # Check if player is in a good position for the shot
            if player_position[1] > 0.3:
                return 0.8  # Good bat position
            return 0.4  # Needs improvement
            
        except Exception as e:
            logger.error(f"Error in bat swing analysis: {str(e)}")
            return 0.0
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all feedback provided during the session.
        
        Returns:
            Dictionary containing feedback summary statistics
        """
        try:
            if not self.feedback_history:
                return {}
                
            # Count feedback by category
            category_counts = {}
            for feedback in self.feedback_history:
                category = feedback.category
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
            
            # Calculate average confidence
            total_confidence = sum(f.confidence for f in self.feedback_history)
            avg_confidence = total_confidence / len(self.feedback_history)
            
            return {
                "total_feedback": len(self.feedback_history),
                "category_distribution": category_counts,
                "average_confidence": avg_confidence,
                "last_feedback_time": self.last_feedback_time
            }
            
        except Exception as e:
            logger.error(f"Error getting feedback summary: {str(e)}")
            return {}

    def analyze_stance(self, player_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """Analyze player's stance and provide feedback."""
        try:
            if player_position is None:
                return None
                
            # Check if player is in a good stance position
            x, y = player_position
            if y < 0.3:  # Too close to the crease
                return Feedback(
                    message="Move back slightly to maintain proper stance",
                    confidence=0.8,
                    category="stance"
                )
            return None
        except Exception as e:
            logger.error(f"Error analyzing stance: {str(e)}")
            return None

    def analyze_balance(self, player_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """Analyze player's balance and provide feedback."""
        try:
            if player_position is None:
                return None
                
            # Check if player is well balanced
            x, y = player_position
            if abs(x) > 0.2:  # Too much weight on one side
                return Feedback(
                    message="Maintain better balance by distributing weight evenly",
                    confidence=0.7,
                    category="balance"
                )
            return None
        except Exception as e:
            logger.error(f"Error analyzing balance: {str(e)}")
            return None

    def analyze_shot_selection(self, ball_position: Tuple[float, float], shot_zone: str) -> Optional[Feedback]:
        """Analyze shot selection based on ball position and zone."""
        try:
            if ball_position is None:
                return None
                
            # Check if shot selection is appropriate for the ball position
            x, y = ball_position
            if shot_zone == "off_side" and x > 0.5:
                return Feedback(
                    message="Consider playing straighter for this delivery",
                    confidence=0.75,
                    category="shot_selection"
                )
            return None
        except Exception as e:
            logger.error(f"Error analyzing shot selection: {str(e)}")
            return None

    def analyze_timing(self, ball_position: Tuple[float, float], player_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """Analyze timing of the shot."""
        try:
            if player_position is None:
                return None
                
            # Check if player is in position to play the shot
            ball_x, ball_y = ball_position
            player_x, player_y = player_position
            if abs(ball_x - player_x) > 0.3:
                return Feedback(
                    message="Get into position earlier to play the shot",
                    confidence=0.7,
                    category="timing"
                )
            return None
        except Exception as e:
            logger.error(f"Error analyzing timing: {str(e)}")
            return None

    def analyze_technique(self, frame: np.ndarray, player_position: Optional[Tuple[float, float]], 
                         ball_position: Optional[Tuple[float, float]]) -> Optional[Feedback]:
        """Analyze overall batting technique."""
        try:
            if player_position is None or ball_position is None:
                return None
                
            # Check if player is moving towards the ball
            ball_x, ball_y = ball_position
            player_x, player_y = player_position
            if ball_x > player_x + 0.2:
                return Feedback(
                    message="Move your feet to get closer to the ball",
                    confidence=0.8,
                    category="technique"
                )
            return None
        except Exception as e:
            logger.error(f"Error analyzing technique: {str(e)}")
            return None 