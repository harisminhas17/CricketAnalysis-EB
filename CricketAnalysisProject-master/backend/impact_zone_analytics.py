import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ImpactType(Enum):
    BAT = "bat"
    PAD = "pad"
    STUMP = "stump"

@dataclass
class ImpactZone:
    type: ImpactType
    position: Tuple[float, float, float]
    confidence: float
    timestamp: float
    frame_index: int
    metrics: Dict[str, Any]

class ImpactZoneAnalyzer:
    def __init__(self):
        # Impact zone thresholds
        self.BAT_IMPACT_THRESHOLD = 0.1  # meters
        self.PAD_IMPACT_THRESHOLD = 0.15  # meters
        self.STUMP_IMPACT_THRESHOLD = 0.05  # meters
        
        # Zone dimensions
        self.STUMP_HEIGHT = 0.711  # meters
        self.STUMP_WIDTH = 0.2286  # meters
        self.BAT_LENGTH = 0.965  # meters
        self.PAD_HEIGHT = 0.4  # meters
        
        # Impact history
        self.impact_history: List[ImpactZone] = []
        
    def analyze_impact(self, 
                      ball_position: Tuple[float, float, float],
                      ball_velocity: Tuple[float, float, float],
                      bat_position: Optional[Tuple[float, float, float]] = None,
                      pad_position: Optional[Tuple[float, float, float]] = None,
                      stump_position: Optional[Tuple[float, float, float]] = None,
                      frame_index: int = 0,
                      timestamp: float = 0.0) -> List[ImpactZone]:
        """Analyze potential impacts with bat, pad, and stumps."""
        impacts = []
        
        # Check bat impact
        if bat_position:
            bat_impact = self._check_bat_impact(ball_position, bat_position, ball_velocity)
            if bat_impact:
                impacts.append(ImpactZone(
                    type=ImpactType.BAT,
                    position=bat_impact['position'],
                    confidence=bat_impact['confidence'],
                    timestamp=timestamp,
                    frame_index=frame_index,
                    metrics=bat_impact['metrics']
                ))
        
        # Check pad impact
        if pad_position:
            pad_impact = self._check_pad_impact(ball_position, pad_position, ball_velocity)
            if pad_impact:
                impacts.append(ImpactZone(
                    type=ImpactType.PAD,
                    position=pad_impact['position'],
                    confidence=pad_impact['confidence'],
                    timestamp=timestamp,
                    frame_index=frame_index,
                    metrics=pad_impact['metrics']
                ))
        
        # Check stump impact
        if stump_position:
            stump_impact = self._check_stump_impact(ball_position, stump_position, ball_velocity)
            if stump_impact:
                impacts.append(ImpactZone(
                    type=ImpactType.STUMP,
                    position=stump_impact['position'],
                    confidence=stump_impact['confidence'],
                    timestamp=timestamp,
                    frame_index=frame_index,
                    metrics=stump_impact['metrics']
                ))
        
        # Update impact history
        self.impact_history.extend(impacts)
        
        return impacts
    
    def _check_bat_impact(self, 
                         ball_pos: Tuple[float, float, float],
                         bat_pos: Tuple[float, float, float],
                         ball_vel: Tuple[float, float, float]) -> Optional[Dict[str, Any]]:
        """Check for bat impact and calculate impact metrics."""
        distance = np.sqrt(sum((b - p) ** 2 for b, p in zip(ball_pos, bat_pos)))
        
        if distance < self.BAT_IMPACT_THRESHOLD:
            # Calculate impact angle
            impact_angle = np.arctan2(ball_vel[1], ball_vel[0])
            
            # Calculate bat speed (if available)
            bat_speed = np.linalg.norm(ball_vel)
            
            # Calculate impact confidence
            confidence = 1.0 - (distance / self.BAT_IMPACT_THRESHOLD)
            
            return {
                'position': ball_pos,
                'confidence': confidence,
                'metrics': {
                    'impact_angle': float(impact_angle),
                    'bat_speed': float(bat_speed),
                    'distance': float(distance)
                }
            }
        return None
    
    def _check_pad_impact(self,
                         ball_pos: Tuple[float, float, float],
                         pad_pos: Tuple[float, float, float],
                         ball_vel: Tuple[float, float, float]) -> Optional[Dict[str, Any]]:
        """Check for pad impact and calculate impact metrics."""
        distance = np.sqrt(sum((b - p) ** 2 for b, p in zip(ball_pos, pad_pos)))
        
        if distance < self.PAD_IMPACT_THRESHOLD:
            # Calculate impact height relative to pad
            height_diff = ball_pos[1] - pad_pos[1]
            
            # Calculate impact angle
            impact_angle = np.arctan2(ball_vel[1], ball_vel[0])
            
            # Calculate impact confidence
            confidence = 1.0 - (distance / self.PAD_IMPACT_THRESHOLD)
            
            return {
                'position': ball_pos,
                'confidence': confidence,
                'metrics': {
                    'height_diff': float(height_diff),
                    'impact_angle': float(impact_angle),
                    'distance': float(distance)
                }
            }
        return None
    
    def _check_stump_impact(self,
                           ball_pos: Tuple[float, float, float],
                           stump_pos: Tuple[float, float, float],
                           ball_vel: Tuple[float, float, float]) -> Optional[Dict[str, Any]]:
        """Check for stump impact and calculate impact metrics."""
        # Check if ball is at stump height
        if 0 <= ball_pos[1] <= self.STUMP_HEIGHT:
            # Check if ball is within stump width
            if abs(ball_pos[2] - stump_pos[2]) <= self.STUMP_WIDTH:
                # Determine which stump would be hit
                if abs(ball_pos[2] - stump_pos[2]) < self.STUMP_IMPACT_THRESHOLD:
                    stump = "middle"
                elif ball_pos[2] > stump_pos[2]:
                    stump = "off"
                else:
                    stump = "leg"
                
                # Calculate impact confidence
                confidence = 1.0 - (abs(ball_pos[2] - stump_pos[2]) / self.STUMP_WIDTH)
                
                return {
                    'position': ball_pos,
                    'confidence': confidence,
                    'metrics': {
                        'stump': stump,
                        'height': float(ball_pos[1]),
                        'distance': float(abs(ball_pos[2] - stump_pos[2]))
                    }
                }
        return None
    
    def get_impact_summary(self) -> Dict[str, Any]:
        """Get a summary of all impacts detected."""
        if not self.impact_history:
            return {
                'total_impacts': 0,
                'impact_types': {},
                'impact_zones': {},
                'confidence_stats': {}
            }
        
        # Count impact types
        impact_types = {}
        for impact in self.impact_history:
            impact_types[impact.type.value] = impact_types.get(impact.type.value, 0) + 1
        
        # Calculate impact zones
        impact_zones = {
            'bat': {'top': 0, 'middle': 0, 'bottom': 0},
            'pad': {'top': 0, 'middle': 0, 'bottom': 0},
            'stump': {'off': 0, 'middle': 0, 'leg': 0}
        }
        
        for impact in self.impact_history:
            if impact.type == ImpactType.BAT:
                height = impact.position[1]
                if height > self.BAT_LENGTH * 0.7:
                    impact_zones['bat']['top'] += 1
                elif height > self.BAT_LENGTH * 0.3:
                    impact_zones['bat']['middle'] += 1
                else:
                    impact_zones['bat']['bottom'] += 1
            elif impact.type == ImpactType.PAD:
                height = impact.position[1]
                if height > self.PAD_HEIGHT * 0.7:
                    impact_zones['pad']['top'] += 1
                elif height > self.PAD_HEIGHT * 0.3:
                    impact_zones['pad']['middle'] += 1
                else:
                    impact_zones['pad']['bottom'] += 1
            elif impact.type == ImpactType.STUMP:
                stump = impact.metrics.get('stump', 'middle')
                impact_zones['stump'][stump] += 1
        
        # Calculate confidence statistics
        confidence_stats = {
            'bat': {'mean': 0, 'max': 0},
            'pad': {'mean': 0, 'max': 0},
            'stump': {'mean': 0, 'max': 0}
        }
        
        for impact in self.impact_history:
            stats = confidence_stats[impact.type.value]
            stats['mean'] = (stats['mean'] * (impact_types[impact.type.value] - 1) + 
                           impact.confidence) / impact_types[impact.type.value]
            stats['max'] = max(stats['max'], impact.confidence)
        
        return {
            'total_impacts': len(self.impact_history),
            'impact_types': impact_types,
            'impact_zones': impact_zones,
            'confidence_stats': confidence_stats
        } 