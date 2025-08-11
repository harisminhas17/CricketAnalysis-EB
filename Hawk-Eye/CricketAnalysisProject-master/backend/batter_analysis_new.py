from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import numpy as np
from datetime import datetime

class ShotType(Enum):
    DRIVE = "drive"
    CUT = "cut"
    PULL = "pull"
    HOOK = "hook"
    SWEEP = "sweep"
    DEFENSIVE = "defensive"
    LEAVE = "leave"

class ShotQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"

@dataclass
class ShotAnalysis:
    shot_type: ShotType
    quality: ShotQuality
    confidence: float
    footwork: str
    head_position: Tuple[float, float]
    bat_angle: float
    contact_point: Tuple[float, float]
    follow_through: float
    timestamp: datetime

class BatterAnalyzer:
    def __init__(self):
        self.shot_history: List[ShotAnalysis] = []
        self.stance_analysis: Dict[str, float] = {
            "head_position": 0.0,
            "bat_angle": 0.0,
            "footwork": "neutral"
        }
        self.performance_metrics: Dict[str, float] = {
            "shot_quality_avg": 0.0,
            "footwork_consistency": 0.0,
            "head_position_stability": 0.0
        }

    def analyze_shot(self, frame: np.ndarray, keypoints: Dict[str, Tuple[float, float]], bat_angle: float, contact_point: Tuple[float, float]) -> ShotAnalysis:
        shot_type = self._classify_shot_type(bat_angle, contact_point)
        quality = self._assess_shot_quality(keypoints, bat_angle, contact_point)
        confidence = self._calculate_confidence(keypoints)
        footwork = self._analyze_footwork(keypoints)
        head_position = keypoints.get("head", (0.0, 0.0))
        follow_through = self._calculate_follow_through(keypoints, bat_angle)
        analysis = ShotAnalysis(
            shot_type=shot_type,
            quality=quality,
            confidence=confidence,
            footwork=footwork,
            head_position=head_position,
            bat_angle=bat_angle,
            contact_point=contact_point,
            follow_through=follow_through,
            timestamp=datetime.now()
        )
        self.shot_history.append(analysis)
        self._update_metrics(analysis)
        return analysis

    def _classify_shot_type(self, bat_angle: float, contact_point: Tuple[float, float]) -> ShotType:
        x, y = contact_point
        if bat_angle > 45: return ShotType.DRIVE
        elif bat_angle < -45: return ShotType.PULL
        elif x > 0.7: return ShotType.CUT
        elif x < 0.3: return ShotType.HOOK
        elif y < 0.3: return ShotType.SWEEP
        else: return ShotType.DEFENSIVE

    def _assess_shot_quality(self, keypoints: Dict[str, Tuple[float, float]], bat_angle: float, contact_point: Tuple[float, float]) -> ShotQuality:
        head_stability = self._calculate_head_stability(keypoints)
        bat_angle_score = self._score_bat_angle(bat_angle)
        contact_score = self._score_contact_point(contact_point)
        footwork_score = self._score_footwork(keypoints)
        total_score = (head_stability + bat_angle_score + contact_score + footwork_score) / 4
        if total_score >= 0.8: return ShotQuality.EXCELLENT
        elif total_score >= 0.6: return ShotQuality.GOOD
        elif total_score >= 0.4: return ShotQuality.AVERAGE
        else: return ShotQuality.POOR

    def _calculate_confidence(self, keypoints: Dict[str, Tuple[float, float]]) -> float:
        required_points = ["head", "shoulders", "hips", "knees", "ankles"]
        missing_points = sum(1 for point in required_points if point not in keypoints)
        base_confidence = 1.0 - (missing_points / len(required_points))
        quality_score = self._assess_keypoint_quality(keypoints)
        return (base_confidence + quality_score) / 2

    def _analyze_footwork(self, keypoints: Dict[str, Tuple[float, float]]) -> str:
        if "left_foot" not in keypoints or "right_foot" not in keypoints: return "unknown"
        left_foot = keypoints["left_foot"]
        right_foot = keypoints["right_foot"]
        foot_distance = np.sqrt((left_foot[0] - right_foot[0])**2 + (left_foot[1] - right_foot[1])**2)
        if foot_distance < 0.2: return "closed"
        elif foot_distance > 0.4: return "open"
        else: return "neutral"

    def _calculate_follow_through(self, keypoints: Dict[str, Tuple[float, float]], bat_angle: float) -> float:
        if "bat_top" not in keypoints or "bat_bottom" not in keypoints: return 0.0
        bat_top = keypoints["bat_top"]
        bat_bottom = keypoints["bat_bottom"]
        dx = bat_top[0] - bat_bottom[0]
        dy = bat_top[1] - bat_bottom[1]
        current_angle = np.degrees(np.arctan2(dy, dx))
        return abs(current_angle - bat_angle)

    def _update_metrics(self, analysis: ShotAnalysis):
        qualities = {ShotQuality.EXCELLENT: 1.0, ShotQuality.GOOD: 0.75, ShotQuality.AVERAGE: 0.5, ShotQuality.POOR: 0.25}
        self.performance_metrics["shot_quality_avg"] = (self.performance_metrics["shot_quality_avg"] * len(self.shot_history) + qualities[analysis.quality]) / (len(self.shot_history) + 1)
        if len(self.shot_history) > 1:
            last_footwork = self.shot_history[-2].footwork
            self.performance_metrics["footwork_consistency"] = (self.performance_metrics["footwork_consistency"] * (len(self.shot_history) - 1) + (1.0 if last_footwork == analysis.footwork else 0.0)) / len(self.shot_history)
            last_head = self.shot_history[-2].head_position
            current_head = analysis.head_position
            head_movement = np.sqrt((last_head[0] - current_head[0])**2 + (last_head[1] - current_head[1])**2)
            self.performance_metrics["head_position_stability"] = (self.performance_metrics["head_position_stability"] * (len(self.shot_history) - 1) + (1.0 - min(head_movement, 1.0))) / len(self.shot_history)

    def get_performance_summary(self) -> Dict:
        return {
            "total_shots": len(self.shot_history),
            "shot_quality_average": round(self.performance_metrics["shot_quality_avg"], 2),
            "footwork_consistency": round(self.performance_metrics["footwork_consistency"], 2),
            "head_position_stability": round(self.performance_metrics["head_position_stability"], 2),
            "shot_distribution": self._get_shot_distribution(),
            "recent_trends": self._get_recent_trends()
        }

    def _get_shot_distribution(self) -> Dict[str, int]:
        distribution = {shot_type.value: 0 for shot_type in ShotType}
        for shot in self.shot_history: distribution[shot.shot_type.value] += 1
        return distribution

    def _get_recent_trends(self, num_shots: int = 5) -> Dict:
        recent_shots = self.shot_history[-num_shots:]
        if not recent_shots: return {"average_quality": 0.0, "most_common_shot": "N/A", "footwork_trend": "N/A"}
        qualities = {ShotQuality.EXCELLENT: 1.0, ShotQuality.GOOD: 0.75, ShotQuality.AVERAGE: 0.5, ShotQuality.POOR: 0.25}
        return {
            "average_quality": round(sum(qualities[shot.quality] for shot in recent_shots) / len(recent_shots), 2),
            "most_common_shot": max(set(shot.shot_type.value for shot in recent_shots), key=lambda x: sum(1 for s in recent_shots if s.shot_type.value == x)),
            "footwork_trend": max(set(shot.footwork for shot in recent_shots), key=lambda x: sum(1 for s in recent_shots if s.footwork == x))
        }

    def _calculate_head_stability(self, keypoints: Dict[str, Tuple[float, float]]) -> float:
        if "head" not in keypoints: return 0.0
        head_pos = keypoints["head"]
        ideal_pos = (0.5, 0.5)
        distance = np.sqrt((head_pos[0] - ideal_pos[0])**2 + (head_pos[1] - ideal_pos[1])**2)
        return 1.0 - min(distance, 1.0)

    def _score_bat_angle(self, bat_angle: float) -> float:
        ideal_angles = {ShotType.DRIVE: 45, ShotType.CUT: 30, ShotType.PULL: -45, ShotType.HOOK: -60, ShotType.SWEEP: -30, ShotType.DEFENSIVE: 0}
        closest_type = min(ideal_angles.items(), key=lambda x: abs(x[1] - bat_angle))[0]
        deviation = abs(ideal_angles[closest_type] - bat_angle)
        return 1.0 - min(deviation / 90.0, 1.0)

    def _score_contact_point(self, contact_point: Tuple[float, float]) -> float:
        x, y = contact_point
        ideal_points = {ShotType.DRIVE: (0.5, 0.5), ShotType.CUT: (0.7, 0.4), ShotType.PULL: (0.3, 0.4), ShotType.HOOK: (0.2, 0.3), ShotType.SWEEP: (0.5, 0.2), ShotType.DEFENSIVE: (0.5, 0.6)}
        closest_point = min(ideal_points.values(), key=lambda p: np.sqrt((p[0] - x)**2 + (p[1] - y)**2))
        distance = np.sqrt((closest_point[0] - x)**2 + (closest_point[1] - y)**2)
        return 1.0 - min(distance, 1.0)

    def _score_footwork(self, keypoints: Dict[str, Tuple[float, float]]) -> float:
        if "left_foot" not in keypoints or "right_foot" not in keypoints: return 0.0
        left_foot = keypoints["left_foot"]
        right_foot = keypoints["right_foot"]
        foot_distance = np.sqrt((left_foot[0] - right_foot[0])**2 + (left_foot[1] - right_foot[1])**2)
        ideal_distance = 0.3
        return 1.0 - min(abs(foot_distance - ideal_distance), 1.0)

    def _assess_keypoint_quality(self, keypoints: Dict[str, Tuple[float, float]]) -> float:
        required_points = ["head", "shoulders", "hips", "knees", "ankles"]
        present_points = sum(1 for point in required_points if point in keypoints)
        return present_points / len(required_points) 