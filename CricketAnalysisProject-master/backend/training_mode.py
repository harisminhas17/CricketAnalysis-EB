import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import os

logger = logging.getLogger(__name__)

@dataclass
class Drill:
    name: str
    description: str
    duration: int  # in minutes
    difficulty: str  # 'beginner', 'intermediate', 'advanced'
    focus_areas: List[str]
    required_equipment: List[str]
    instructions: List[str]

@dataclass
class TrainingSession:
    id: str
    player_id: str
    start_time: datetime
    end_time: Optional[datetime]
    drills: List[Drill]
    completed_drills: List[str]
    feedback: List[Dict[str, Any]]
    metrics: Dict[str, Any]

class TrainingMode:
    def __init__(self, data_dir: str = "data/training"):
        """
        Initialize the training mode manager.
        
        Args:
            data_dir (str): Directory to store training data
        """
        self.data_dir = data_dir
        self.drills_file = os.path.join(data_dir, "drills.json")
        self.sessions_file = os.path.join(data_dir, "sessions.json")
        self._ensure_data_directory()
        self._load_drills()
        
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating data directory: {str(e)}")
            raise
            
    def _load_drills(self):
        """Load available drills from file."""
        try:
            if os.path.exists(self.drills_file):
                with open(self.drills_file, 'r') as f:
                    self.drills = json.load(f)
            else:
                self.drills = self._create_default_drills()
                self._save_drills()
        except Exception as e:
            logger.error(f"Error loading drills: {str(e)}")
            raise
            
    def _save_drills(self):
        """Save drills to file."""
        try:
            with open(self.drills_file, 'w') as f:
                json.dump(self.drills, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving drills: {str(e)}")
            raise
            
    def _create_default_drills(self) -> Dict[str, Any]:
        """
        Create default set of training drills.
        
        Returns:
            Dict[str, Any]: Dictionary of default drills
        """
        return {
            "basic_footwork": {
                "name": "Basic Footwork",
                "description": "Practice basic batting footwork and movement",
                "duration": 15,
                "difficulty": "beginner",
                "focus_areas": ["footwork", "balance", "movement"],
                "required_equipment": ["bat", "cones"],
                "instructions": [
                    "Set up cones in a grid pattern",
                    "Practice moving between cones",
                    "Focus on quick, balanced movements",
                    "Maintain proper batting stance"
                ]
            },
            "shot_selection": {
                "name": "Shot Selection",
                "description": "Practice different shot types and selection",
                "duration": 20,
                "difficulty": "intermediate",
                "focus_areas": ["shot_selection", "technique", "decision_making"],
                "required_equipment": ["bat", "balls", "stumps"],
                "instructions": [
                    "Set up different delivery types",
                    "Practice playing appropriate shots",
                    "Focus on shot selection",
                    "Work on shot execution"
                ]
            },
            "power_hitting": {
                "name": "Power Hitting",
                "description": "Develop power hitting skills",
                "duration": 25,
                "difficulty": "advanced",
                "focus_areas": ["power", "timing", "technique"],
                "required_equipment": ["bat", "balls", "stumps"],
                "instructions": [
                    "Practice hitting through the line",
                    "Focus on bat speed",
                    "Work on timing",
                    "Develop power through proper technique"
                ]
            }
        }
        
    def start_training_session(
        self,
        player_id: str,
        selected_drills: List[str]
    ) -> TrainingSession:
        """
        Start a new training session.
        
        Args:
            player_id (str): Player identifier
            selected_drills (List[str]): List of drill IDs to include
            
        Returns:
            TrainingSession: New training session
        """
        try:
            # Validate selected drills
            drills = []
            for drill_id in selected_drills:
                if drill_id in self.drills:
                    drills.append(self.drills[drill_id])
                else:
                    logger.warning(f"Drill {drill_id} not found")
            
            # Create new session
            session = TrainingSession(
                id=f"session_{int(datetime.now().timestamp())}",
                player_id=player_id,
                start_time=datetime.now(),
                end_time=None,
                drills=drills,
                completed_drills=[],
                feedback=[],
                metrics={}
            )
            
            # Save session
            self._save_session(session)
            
            return session
            
        except Exception as e:
            logger.error(f"Error starting training session: {str(e)}")
            raise
            
    def complete_drill(
        self,
        session_id: str,
        drill_id: str,
        feedback: Dict[str, Any],
        metrics: Dict[str, Any]
    ) -> None:
        """
        Mark a drill as completed and record feedback.
        
        Args:
            session_id (str): Training session identifier
            drill_id (str): Drill identifier
            feedback (Dict[str, Any]): Feedback for the drill
            metrics (Dict[str, Any]): Performance metrics
        """
        try:
            # Load session
            session = self._load_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            # Update session
            session.completed_drills.append(drill_id)
            session.feedback.append(feedback)
            session.metrics.update(metrics)
            
            # Save updated session
            self._save_session(session)
            
        except Exception as e:
            logger.error(f"Error completing drill: {str(e)}")
            raise
            
    def end_training_session(self, session_id: str) -> TrainingSession:
        """
        End a training session.
        
        Args:
            session_id (str): Training session identifier
            
        Returns:
            TrainingSession: Completed training session
        """
        try:
            # Load session
            session = self._load_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            # Update session
            session.end_time = datetime.now()
            
            # Calculate session metrics
            session.metrics.update(self._calculate_session_metrics(session))
            
            # Save updated session
            self._save_session(session)
            
            return session
            
        except Exception as e:
            logger.error(f"Error ending training session: {str(e)}")
            raise
            
    def _load_session(self, session_id: str) -> Optional[TrainingSession]:
        """
        Load a training session from file.
        
        Args:
            session_id (str): Training session identifier
            
        Returns:
            Optional[TrainingSession]: Loaded session if found
        """
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
                    if session_id in sessions:
                        return TrainingSession(**sessions[session_id])
            return None
            
        except Exception as e:
            logger.error(f"Error loading session: {str(e)}")
            return None
            
    def _save_session(self, session: TrainingSession) -> None:
        """
        Save a training session to file.
        
        Args:
            session (TrainingSession): Session to save
        """
        try:
            # Load existing sessions
            sessions = {}
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
            
            # Update sessions
            sessions[session.id] = {
                "id": session.id,
                "player_id": session.player_id,
                "start_time": session.start_time.isoformat(),
                "end_time": session.end_time.isoformat() if session.end_time else None,
                "drills": session.drills,
                "completed_drills": session.completed_drills,
                "feedback": session.feedback,
                "metrics": session.metrics
            }
            
            # Save updated sessions
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            raise
            
    def _calculate_session_metrics(self, session: TrainingSession) -> Dict[str, Any]:
        """
        Calculate overall session metrics.
        
        Args:
            session (TrainingSession): Training session
            
        Returns:
            Dict[str, Any]: Session metrics
        """
        try:
            metrics = {
                "total_duration": 0,
                "completed_drills_count": len(session.completed_drills),
                "completion_rate": 0,
                "average_feedback_score": 0
            }
            
            if session.end_time:
                metrics["total_duration"] = (
                    session.end_time - session.start_time
                ).total_seconds() / 60  # in minutes
            
            if session.drills:
                metrics["completion_rate"] = (
                    len(session.completed_drills) / len(session.drills)
                ) * 100
            
            if session.feedback:
                feedback_scores = [
                    f.get("score", 0) for f in session.feedback
                    if "score" in f
                ]
                if feedback_scores:
                    metrics["average_feedback_score"] = sum(feedback_scores) / len(feedback_scores)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating session metrics: {str(e)}")
            return {} 