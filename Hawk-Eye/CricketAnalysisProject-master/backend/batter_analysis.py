from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import numpy as np
from datetime import datetime

class ShotType(Enum):
    DRIVE = "drive"
    CUT = "cut"
    PULL = "pull"
    SWEEP = "sweep"
    HOOK = "hook"
    DEFENSE = "defense"
    LEAVE = "leave"
    UNKNOWN = "unknown"

class ShotQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    UNKNOWN = "unknown"

@dataclass
class ShotAnalysis:
    timestamp: float
    shot_type: ShotType
    quality: ShotQuality
    bat_speed: float
    impact_position: Tuple[float, float]
    ball_speed: float
    edge_probability: float
    footwork_score: float
    balance_score: float
    head_position: Tuple[float, float]
    bat_angle: float
    follow_through: float
    metrics: Dict[str, float]

class BatterAnalyzer:
    def __init__(self):
        self.shot_history: List[ShotAnalysis] = []

    def analyze_shot(self, frame_data: Dict) -> ShotAnalysis:
        # Dummy logic for demonstration
        shot_type = ShotType.DRIVE
        quality = ShotQuality.GOOD
        bat_speed = frame_data.get('bat_speed', 30.0)
        impact_position = frame_data.get('impact_position', (0.5, 0.5))
        ball_speed = frame_data.get('ball_speed', 25.0)
        edge_probability = frame_data.get('edge_probability', 0.1)
        footwork_score = frame_data.get('footwork_score', 0.8)
        balance_score = frame_data.get('balance_score', 0.85)
        head_position = frame_data.get('head_position', (0.5, 0.5))
        bat_angle = frame_data.get('bat_angle', 45.0)
        follow_through = frame_data.get('follow_through', 0.9)
        metrics = frame_data.get('metrics', {})
        timestamp = frame_data.get('timestamp', datetime.now().timestamp())
        analysis = ShotAnalysis(
            timestamp=timestamp,
            shot_type=shot_type,
            quality=quality,
            bat_speed=bat_speed,
            impact_position=impact_position,
            ball_speed=ball_speed,
            edge_probability=edge_probability,
            footwork_score=footwork_score,
            balance_score=balance_score,
            head_position=head_position,
            bat_angle=bat_angle,
            follow_through=follow_through,
            metrics=metrics
        )
        self.shot_history.append(analysis)
        return analysis

    def get_shot_statistics(self) -> Dict:
        if not self.shot_history:
            return {}
        qualities = [shot.quality for shot in self.shot_history]
        stats = {q.value: qualities.count(q) for q in ShotQuality}
        return stats

    def get_shot_recommendations(self) -> List[str]:
        # Dummy recommendations
        if not self.shot_history:
            return ["Play more shots to get recommendations."]
        last_quality = self.shot_history[-1].quality
        if last_quality == ShotQuality.POOR:
            return ["Work on your footwork.", "Improve your balance."]
        elif last_quality == ShotQuality.AVERAGE:
            return ["Focus on timing.", "Practice shot selection."]
        elif last_quality == ShotQuality.GOOD:
            return ["Keep up the good work!", "Try to maintain consistency."]
        elif last_quality == ShotQuality.EXCELLENT:
            return ["Outstanding! Keep it up."]
        else:
            return ["No specific recommendations."] 