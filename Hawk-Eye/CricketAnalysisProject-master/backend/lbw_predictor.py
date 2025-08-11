import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional, List

@dataclass
class BallState:
    position: Tuple[float, float, float]  # x, y, z coordinates
    velocity: Tuple[float, float, float]  # vx, vy, vz
    spin: Optional[Tuple[float, float, float]] = None  # spin vector (optional)
    timestamp: float = 0.0  # Time in seconds

class LBWPredictor:
    # Cricket pitch constants
    STUMP_HEIGHT = 0.711  # meters
    STUMP_WIDTH = 0.2286  # meters
    GRAVITY = 9.81  # m/s^2
    AIR_DENSITY = 1.225  # kg/m^3
    BALL_RADIUS = 0.0364  # meters
    BALL_MASS = 0.163  # kg
    
    # Enhanced detection thresholds
    PAD_IMPACT_THRESHOLD = 0.15  # Increased from 0.1 to 0.15 meters
    STUMP_IMPACT_THRESHOLD = 0.05  # New threshold for stump impact zone
    MIN_CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence for LBW decision
    TRAJECTORY_STABILITY_THRESHOLD = 0.1  # Maximum allowed deviation in trajectory
    
    def __init__(self):
        self.pad_impact_frame = None
        self.ball_states: List[BallState] = []
        self.time_step = 0.01  # 10ms time step
        self.trajectory_history = []  # Store multiple trajectory predictions
    
    def add_ball_state(self, position: Tuple[float, float, float], 
                      velocity: Tuple[float, float, float],
                      spin: Optional[Tuple[float, float, float]] = None,
                      timestamp: float = 0.0):
        """Add a new ball state to the tracking history."""
        self.ball_states.append(BallState(position, velocity, spin, timestamp))
        
        # Update trajectory history
        if len(self.ball_states) >= 3:  # Need at least 3 points for trajectory analysis
            self._update_trajectory_history()
    
    def _update_trajectory_history(self):
        """Update trajectory history with multiple predictions."""
        if len(self.ball_states) < 3:
            return
            
        # Get last 3 states for trajectory prediction
        recent_states = self.ball_states[-3:]
        
        # Predict trajectories with different initial conditions
        trajectories = []
        for state in recent_states:
            trajectory = self.predict_trajectory(state)
            if trajectory:
                trajectories.append(trajectory)
        
        self.trajectory_history = trajectories
    
    def detect_pad_impact(self, ball_position: Tuple[float, float, float], 
                         pad_position: Tuple[float, float, float]) -> bool:
        """Enhanced pad impact detection with better thresholding."""
        distance = np.sqrt(sum((b - p) ** 2 for b, p in zip(ball_position, pad_position)))
        
        # Check if ball is in the pad impact zone
        in_impact_zone = distance < self.PAD_IMPACT_THRESHOLD
        
        # Additional checks for pad impact
        if in_impact_zone:
            # Check if ball is moving towards the pad
            if len(self.ball_states) >= 2:
                prev_pos = np.array(self.ball_states[-2].position)
                curr_pos = np.array(ball_position)
                pad_pos = np.array(pad_position)
                
                # Calculate if ball is moving towards pad
                ball_direction = curr_pos - prev_pos
                pad_direction = pad_pos - curr_pos
                angle = np.arccos(np.dot(ball_direction, pad_direction) / 
                                (np.linalg.norm(ball_direction) * np.linalg.norm(pad_direction)))
                
                # Ball is moving towards pad if angle is less than 90 degrees
                return angle < np.pi/2
        
        return in_impact_zone
    
    def calculate_drag_force(self, velocity: np.ndarray) -> np.ndarray:
        """Enhanced drag force calculation with variable drag coefficient."""
        speed = np.linalg.norm(velocity)
        if speed == 0:
            return np.zeros(3)
        
        # Variable drag coefficient based on speed
        # Higher speeds have lower drag coefficient
        cd = 0.47 * (1 - 0.1 * min(speed/50, 1))  # Adjusts for high-speed effects
        area = np.pi * self.BALL_RADIUS ** 2
        
        # Drag force with enhanced model
        drag_force = -0.5 * self.AIR_DENSITY * cd * area * speed * velocity
        return drag_force
    
    def calculate_magnus_force(self, velocity: np.ndarray, 
                             spin: np.ndarray) -> np.ndarray:
        """Enhanced Magnus force calculation with variable coefficient."""
        if spin is None or np.all(spin == 0):
            return np.zeros(3)
        
        # Variable Magnus coefficient based on spin rate
        spin_rate = np.linalg.norm(spin)
        cm = 0.5 * (1 + 0.2 * min(spin_rate/100, 1))  # Adjusts for high spin rates
        
        # Enhanced Magnus force calculation
        magnus_force = cm * np.cross(velocity, spin)
        return magnus_force
    
    def predict_trajectory(self, initial_state: BallState, 
                         time_steps: int = 50) -> List[Tuple[float, float, float]]:
        """Enhanced trajectory prediction with improved physics model."""
        trajectory = []
        pos = np.array(initial_state.position)
        vel = np.array(initial_state.velocity)
        spin = np.array(initial_state.spin) if initial_state.spin else np.zeros(3)
        
        for _ in range(time_steps):
            # Calculate forces with enhanced models
            drag_force = self.calculate_drag_force(vel)
            magnus_force = self.calculate_magnus_force(vel, spin)
            
            # Total force (including gravity)
            total_force = drag_force + magnus_force
            total_force[1] -= self.GRAVITY * self.BALL_MASS
            
            # Update velocity using improved integration
            acceleration = total_force / self.BALL_MASS
            vel = vel + acceleration * self.time_step
            
            # Update position with improved integration
            pos = pos + vel * self.time_step
            
            trajectory.append(tuple(pos))
            
            # Stop if ball hits the ground
            if pos[1] <= 0:
                break
        
        return trajectory
    
    def check_stump_intersection(self, trajectory: List[Tuple[float, float, float]]) -> Tuple[bool, str, float]:
        """Enhanced stump intersection check with improved accuracy."""
        if not trajectory:
            return False, "none", 0.0
            
        # Calculate trajectory stability
        stability = self._calculate_trajectory_stability(trajectory)
        
        # Check each point in trajectory
        for pos in trajectory:
            x, y, z = pos
            
            # Enhanced stump height check with tolerance
            if 0 <= y <= self.STUMP_HEIGHT * 1.1:  # 10% tolerance
                # Enhanced stump width check with tolerance
                if abs(z) <= self.STUMP_WIDTH * 1.2:  # 20% tolerance
                    # Determine which stump would be hit with enhanced accuracy
                    if abs(z) < self.STUMP_IMPACT_THRESHOLD:
                        stump = "middle"
                    elif z > 0:
                        stump = "off"
                    else:
                        stump = "leg"
                    
                    # Calculate confidence with enhanced factors
                    confidence = self._calculate_enhanced_confidence(trajectory, stability)
                    return True, stump, confidence
        
        return False, "none", 0.0
    
    def _calculate_trajectory_stability(self, trajectory: List[Tuple[float, float, float]]) -> float:
        """Calculate trajectory stability based on deviation from expected path."""
        if len(trajectory) < 3:
            return 0.0
            
        positions = np.array(trajectory)
        
        # Calculate expected path (straight line from start to end)
        start_pos = positions[0]
        end_pos = positions[-1]
        expected_path = np.linspace(start_pos, end_pos, len(positions))
        
        # Calculate deviations from expected path
        deviations = np.linalg.norm(positions - expected_path, axis=1)
        stability = 1.0 - np.mean(deviations) / np.linalg.norm(end_pos - start_pos)
        
        return max(0.0, min(1.0, stability))
    
    def _calculate_enhanced_confidence(self, trajectory: List[Tuple[float, float, float]], 
                                     stability: float) -> float:
        """Calculate enhanced confidence score for LBW prediction."""
        if not trajectory:
            return 0.0
        
        # Base confidence factors
        trajectory_length = len(trajectory)
        position_consistency = 1.0 - np.std(np.array(trajectory), axis=0).mean()
        
        # Calculate confidence components
        length_confidence = min(trajectory_length / 20, 1.0)
        stability_confidence = stability
        consistency_confidence = position_consistency
        
        # Weighted combination of confidence factors
        confidence = (
            0.4 * length_confidence +
            0.4 * stability_confidence +
            0.2 * consistency_confidence
        )
        
        # Apply minimum threshold
        if confidence < self.MIN_CONFIDENCE_THRESHOLD:
            confidence = 0.0
            
        return min(max(confidence, 0.0), 1.0) * 100
    
    def analyze_lbw(self, pad_impact_position: Tuple[float, float, float],
                   pitch_location: str) -> dict:
        """Enhanced LBW analysis with improved accuracy."""
        if not self.ball_states:
            return {"lbw": False, "confidence": 0.0, "reason": "No ball tracking data"}
        
        # Get the last ball state before pad impact
        last_state = self.ball_states[-1]
        
        # Predict trajectory from impact point
        trajectory = self.predict_trajectory(last_state)
        
        # Check if ball would hit stumps with enhanced detection
        hits_stumps, stump_hit, confidence = self.check_stump_intersection(trajectory)
        
        # Enhanced pitch location and pad impact line checks
        pitch_in_line = pitch_location in ["middle", "leg"]
        pad_in_line = abs(pad_impact_position[2]) <= self.STUMP_WIDTH * 1.2  # 20% tolerance
        
        # Calculate additional metrics
        impact_velocity = np.linalg.norm(last_state.velocity)
        distance_to_stumps = np.linalg.norm(
            np.array(pad_impact_position) - np.array([0, 0, 0])
        )
        
        # Enhanced LBW decision with multiple factors
        lbw = (
            hits_stumps and 
            pitch_in_line and 
            pad_in_line and 
            confidence >= self.MIN_CONFIDENCE_THRESHOLD * 100
        )
        
        return {
            "lbw": lbw,
            "confidence": confidence,
            "stump_hit": stump_hit,
            "pitch_location": pitch_location,
            "pad_in_line": pad_in_line,
            "impact_velocity": float(impact_velocity),
            "distance_to_stumps": float(distance_to_stumps),
            "trajectory": trajectory,
            "trajectory_stability": float(self._calculate_trajectory_stability(trajectory) * 100)
        } 