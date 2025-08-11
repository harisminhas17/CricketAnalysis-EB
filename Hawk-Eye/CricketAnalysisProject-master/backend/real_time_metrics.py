import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

@dataclass
class BallMetrics:
    speed: float  # km/h
    length: str  # full, good, short, etc.
    line: str  # off, middle, leg
    movement: Tuple[float, float]  # (swing, seam)
    bounce: float  # height of bounce
    timestamp: datetime

@dataclass
class ShotMetrics:
    type: str  # drive, cut, pull, etc.
    power: float  # 0-100
    timing: float  # 0-100
    placement: Tuple[float, float]  # (x, y) coordinates
    result: str  # boundary, single, dot ball, etc.
    timestamp: datetime

class RealTimeMetrics:
    def __init__(self):
        self.ball_metrics: List[BallMetrics] = []
        self.shot_metrics: List[ShotMetrics] = []
        self.current_over: List[BallMetrics] = []
        self.over_count: int = 0
        self.total_runs: int = 0
        self.total_boundaries: int = 0
        self.total_dots: int = 0
        self.strike_rate: float = 0.0
        self.run_rate: float = 0.0
        self.last_update: datetime = datetime.now()

    def add_ball_metrics(self, metrics: BallMetrics):
        """Add ball metrics for the current delivery."""
        self.ball_metrics.append(metrics)
        self.current_over.append(metrics)
        
        # Check if over is complete
        if len(self.current_over) == 6:
            self.over_count += 1
            self.current_over = []
        
        self.last_update = datetime.now()

    def add_shot_metrics(self, metrics: ShotMetrics):
        """Add shot metrics for the current delivery."""
        self.shot_metrics.append(metrics)
        
        # Update statistics
        if metrics.result == "boundary":
            self.total_boundaries += 1
            self.total_runs += 4 if metrics.result == "4" else 6
        elif metrics.result == "dot":
            self.total_dots += 1
        elif metrics.result in ["1", "2", "3"]:
            self.total_runs += int(metrics.result)
        
        # Update rates
        total_balls = len(self.ball_metrics)
        if total_balls > 0:
            self.strike_rate = (self.total_runs / total_balls) * 100
            self.run_rate = (self.total_runs / (self.over_count + len(self.current_over)/6)) * 6
        
        self.last_update = datetime.now()

    def get_current_over_summary(self) -> Dict:
        """Get summary of the current over."""
        if not self.current_over:
            return {
                "balls_bowled": 0,
                "runs": 0,
                "wickets": 0,
                "extras": 0
            }
        
        runs = sum(1 for ball in self.current_over if ball.result in ["1", "2", "3", "4", "6"])
        extras = sum(1 for ball in self.current_over if ball.result in ["wide", "no-ball"])
        
        return {
            "balls_bowled": len(self.current_over),
            "runs": runs,
            "extras": extras,
            "balls": [self._format_ball(ball) for ball in self.current_over]
        }

    def get_match_summary(self) -> Dict:
        """Get overall match summary."""
        return {
            "total_runs": self.total_runs,
            "total_boundaries": self.total_boundaries,
            "total_dots": self.total_dots,
            "strike_rate": round(self.strike_rate, 2),
            "run_rate": round(self.run_rate, 2),
            "overs_completed": self.over_count,
            "current_over": self.get_current_over_summary()
        }

    def get_recent_trends(self, num_balls: int = 12) -> Dict:
        """Get recent performance trends."""
        recent_balls = self.ball_metrics[-num_balls:]
        recent_shots = self.shot_metrics[-num_balls:]
        
        if not recent_balls:
            return {
                "average_speed": 0,
                "common_length": "N/A",
                "common_line": "N/A",
                "boundary_percentage": 0
            }
        
        speeds = [ball.speed for ball in recent_balls]
        lengths = [ball.length for ball in recent_balls]
        lines = [ball.line for ball in recent_balls]
        boundaries = sum(1 for shot in recent_shots if shot.result in ["4", "6"])
        
        return {
            "average_speed": round(np.mean(speeds), 1),
            "common_length": max(set(lengths), key=lengths.count),
            "common_line": max(set(lines), key=lines.count),
            "boundary_percentage": round((boundaries / len(recent_shots)) * 100, 1) if recent_shots else 0
        }

    def _format_ball(self, ball: BallMetrics) -> Dict:
        """Format ball metrics for JSON serialization."""
        return {
            "speed": ball.speed,
            "length": ball.length,
            "line": ball.line,
            "movement": ball.movement,
            "bounce": ball.bounce,
            "timestamp": ball.timestamp.isoformat()
        }

    def export_metrics(self, filepath: str):
        """Export all metrics to a JSON file."""
        data = {
            "ball_metrics": [self._format_ball(ball) for ball in self.ball_metrics],
            "shot_metrics": [
                {
                    "type": shot.type,
                    "power": shot.power,
                    "timing": shot.timing,
                    "placement": shot.placement,
                    "result": shot.result,
                    "timestamp": shot.timestamp.isoformat()
                }
                for shot in self.shot_metrics
            ],
            "match_summary": self.get_match_summary(),
            "recent_trends": self.get_recent_trends()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def reset(self):
        """Reset all metrics."""
        self.__init__() 