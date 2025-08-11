import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum

class FlagType(Enum):
    EDGE_RISK = "edge_risk"
    BAT_LAG = "bat_lag"
    FOOTWORK_ISSUE = "footwork_issue"
    BALANCE_ISSUE = "balance_issue"
    TIMING_ISSUE = "timing_issue"

@dataclass
class PerformanceFlag:
    type: FlagType
    confidence: float
    frame_index: int
    description: str
    severity: float  # 0.0 to 1.0
    position: Tuple[int, int]  # (x, y) coordinates
    metadata: Dict = None

class PerformanceFlagDetector:
    def __init__(self):
        self.flags: List[PerformanceFlag] = []
        self.bat_trajectory: List[Tuple[int, int]] = []
        self.ball_trajectory: List[Tuple[int, int]] = []
        self.player_positions: List[Tuple[int, int]] = []
        
    def detect_flags(self, frame: np.ndarray, frame_index: int, 
                    bat_pos: Optional[Tuple[int, int]] = None,
                    ball_pos: Optional[Tuple[int, int]] = None,
                    player_pos: Optional[Tuple[int, int]] = None) -> List[PerformanceFlag]:
        """Detect performance flags in the current frame."""
        current_flags = []
        
        # Update trajectories
        if bat_pos:
            self.bat_trajectory.append(bat_pos)
        if ball_pos:
            self.ball_trajectory.append(ball_pos)
        if player_pos:
            self.player_positions.append(player_pos)
        
        # Keep only recent history
        max_history = 30  # frames
        if len(self.bat_trajectory) > max_history:
            self.bat_trajectory = self.bat_trajectory[-max_history:]
        if len(self.ball_trajectory) > max_history:
            self.ball_trajectory = self.ball_trajectory[-max_history:]
        if len(self.player_positions) > max_history:
            self.player_positions = self.player_positions[-max_history:]
        
        # Detect edge risk
        if len(self.bat_trajectory) >= 2 and len(self.ball_trajectory) >= 2:
            edge_risk = self._detect_edge_risk()
            if edge_risk:
                current_flags.append(edge_risk)
        
        # Detect bat lag
        if len(self.bat_trajectory) >= 3:
            bat_lag = self._detect_bat_lag()
            if bat_lag:
                current_flags.append(bat_lag)
        
        # Detect footwork issues
        if len(self.player_positions) >= 3:
            footwork_issue = self._detect_footwork_issue()
            if footwork_issue:
                current_flags.append(footwork_issue)
        
        # Detect balance issues
        if len(self.player_positions) >= 3:
            balance_issue = self._detect_balance_issue()
            if balance_issue:
                current_flags.append(balance_issue)
        
        # Detect timing issues
        if len(self.bat_trajectory) >= 2 and len(self.ball_trajectory) >= 2:
            timing_issue = self._detect_timing_issue()
            if timing_issue:
                current_flags.append(timing_issue)
        
        self.flags.extend(current_flags)
        return current_flags
    
    def _detect_edge_risk(self) -> Optional[PerformanceFlag]:
        """Detect if there's a risk of edging the ball."""
        if len(self.bat_trajectory) < 2 or len(self.ball_trajectory) < 2:
            return None
        
        # Calculate bat angle
        bat_dx = self.bat_trajectory[-1][0] - self.bat_trajectory[-2][0]
        bat_dy = self.bat_trajectory[-1][1] - self.bat_trajectory[-2][1]
        bat_angle = np.arctan2(bat_dy, bat_dx)
        
        # Calculate ball angle
        ball_dx = self.ball_trajectory[-1][0] - self.ball_trajectory[-2][0]
        ball_dy = self.ball_trajectory[-1][1] - self.ball_trajectory[-2][1]
        ball_angle = np.arctan2(ball_dy, ball_dx)
        
        # Calculate angle difference
        angle_diff = abs(bat_angle - ball_angle)
        if angle_diff > np.pi:
            angle_diff = 2 * np.pi - angle_diff
        
        # Calculate distance between bat and ball
        bat_pos = self.bat_trajectory[-1]
        ball_pos = self.ball_trajectory[-1]
        distance = np.sqrt((bat_pos[0] - ball_pos[0])**2 + (bat_pos[1] - ball_pos[1])**2)
        
        # Determine edge risk
        if angle_diff > np.pi/4 and distance < 50:  # Thresholds can be adjusted
            confidence = min(1.0, (angle_diff - np.pi/4) / (np.pi/2))
            severity = min(1.0, (np.pi/2 - angle_diff) / (np.pi/4))
            
            return PerformanceFlag(
                type=FlagType.EDGE_RISK,
                confidence=confidence,
                frame_index=len(self.bat_trajectory) - 1,
                description="High risk of edging the ball",
                severity=severity,
                position=bat_pos,
                metadata={
                    'angle_diff': float(angle_diff),
                    'distance': float(distance)
                }
            )
        
        return None
    
    def _detect_bat_lag(self) -> Optional[PerformanceFlag]:
        """Detect if there's bat lag in the shot."""
        if len(self.bat_trajectory) < 3:
            return None
        
        # Calculate bat speed
        bat_speeds = []
        for i in range(1, len(self.bat_trajectory)):
            dx = self.bat_trajectory[i][0] - self.bat_trajectory[i-1][0]
            dy = self.bat_trajectory[i][1] - self.bat_trajectory[i-1][1]
            speed = np.sqrt(dx*dx + dy*dy)
            bat_speeds.append(speed)
        
        # Calculate acceleration
        accelerations = []
        for i in range(1, len(bat_speeds)):
            acc = bat_speeds[i] - bat_speeds[i-1]
            accelerations.append(acc)
        
        # Detect bat lag
        if len(accelerations) >= 2:
            recent_acc = accelerations[-2:]
            if recent_acc[0] < 0 and recent_acc[1] < 0:  # Decelerating
                confidence = min(1.0, abs(recent_acc[0] + recent_acc[1]) / 10.0)
                severity = min(1.0, abs(recent_acc[0] + recent_acc[1]) / 20.0)
                
                return PerformanceFlag(
                    type=FlagType.BAT_LAG,
                    confidence=confidence,
                    frame_index=len(self.bat_trajectory) - 1,
                    description="Bat lag detected - deceleration in swing",
                    severity=severity,
                    position=self.bat_trajectory[-1],
                    metadata={
                        'acceleration': float(recent_acc[1]),
                        'speed': float(bat_speeds[-1])
                    }
                )
        
        return None
    
    def _detect_footwork_issue(self) -> Optional[PerformanceFlag]:
        """Detect footwork issues based on player movement."""
        if len(self.player_positions) < 3:
            return None
        
        # Calculate movement vectors
        movements = []
        for i in range(1, len(self.player_positions)):
            dx = self.player_positions[i][0] - self.player_positions[i-1][0]
            dy = self.player_positions[i][1] - self.player_positions[i-1][1]
            movements.append((dx, dy))
        
        # Calculate movement consistency
        if len(movements) >= 2:
            recent_movements = movements[-2:]
            movement_diff = np.sqrt(
                (recent_movements[0][0] - recent_movements[1][0])**2 +
                (recent_movements[0][1] - recent_movements[1][1])**2
            )
            
            if movement_diff > 20:  # Threshold can be adjusted
                confidence = min(1.0, movement_diff / 50.0)
                severity = min(1.0, movement_diff / 100.0)
                
                return PerformanceFlag(
                    type=FlagType.FOOTWORK_ISSUE,
                    confidence=confidence,
                    frame_index=len(self.player_positions) - 1,
                    description="Inconsistent footwork detected",
                    severity=severity,
                    position=self.player_positions[-1],
                    metadata={
                        'movement_diff': float(movement_diff)
                    }
                )
        
        return None
    
    def _detect_balance_issue(self) -> Optional[PerformanceFlag]:
        """Detect balance issues based on player movement patterns."""
        if len(self.player_positions) < 3:
            return None
        
        # Calculate vertical movement
        vertical_movements = []
        for i in range(1, len(self.player_positions)):
            dy = self.player_positions[i][1] - self.player_positions[i-1][1]
            vertical_movements.append(dy)
        
        # Check for excessive vertical movement
        if len(vertical_movements) >= 2:
            recent_vertical = vertical_movements[-2:]
            vertical_diff = abs(recent_vertical[0] - recent_vertical[1])
            
            if vertical_diff > 15:  # Threshold can be adjusted
                confidence = min(1.0, vertical_diff / 30.0)
                severity = min(1.0, vertical_diff / 60.0)
                
                return PerformanceFlag(
                    type=FlagType.BALANCE_ISSUE,
                    confidence=confidence,
                    frame_index=len(self.player_positions) - 1,
                    description="Balance issue detected - unstable vertical movement",
                    severity=severity,
                    position=self.player_positions[-1],
                    metadata={
                        'vertical_diff': float(vertical_diff)
                    }
                )
        
        return None
    
    def _detect_timing_issue(self) -> Optional[PerformanceFlag]:
        """Detect timing issues between bat and ball movement."""
        if len(self.bat_trajectory) < 2 or len(self.ball_trajectory) < 2:
            return None
        
        # Calculate bat and ball speeds
        bat_dx = self.bat_trajectory[-1][0] - self.bat_trajectory[-2][0]
        bat_dy = self.bat_trajectory[-1][1] - self.bat_trajectory[-2][1]
        bat_speed = np.sqrt(bat_dx*bat_dx + bat_dy*bat_dy)
        
        ball_dx = self.ball_trajectory[-1][0] - self.ball_trajectory[-2][0]
        ball_dy = self.ball_trajectory[-1][1] - self.ball_trajectory[-2][1]
        ball_speed = np.sqrt(ball_dx*ball_dx + ball_dy*ball_dy)
        
        # Calculate timing difference
        speed_ratio = bat_speed / ball_speed if ball_speed > 0 else 0
        
        if speed_ratio < 0.5 or speed_ratio > 2.0:  # Thresholds can be adjusted
            confidence = min(1.0, abs(1.0 - speed_ratio))
            severity = min(1.0, abs(1.0 - speed_ratio) / 2.0)
            
            return PerformanceFlag(
                type=FlagType.TIMING_ISSUE,
                confidence=confidence,
                frame_index=len(self.bat_trajectory) - 1,
                description="Timing issue detected - bat and ball speed mismatch",
                severity=severity,
                position=self.bat_trajectory[-1],
                metadata={
                    'speed_ratio': float(speed_ratio),
                    'bat_speed': float(bat_speed),
                    'ball_speed': float(ball_speed)
                }
            )
        
        return None
    
    def get_flags_for_frame(self, frame_index: int) -> List[PerformanceFlag]:
        """Get all flags for a specific frame."""
        return [flag for flag in self.flags if flag.frame_index == frame_index]
    
    def clear_flags(self):
        """Clear all detected flags."""
        self.flags = []
        self.bat_trajectory = []
        self.ball_trajectory = []
        self.player_positions = [] 