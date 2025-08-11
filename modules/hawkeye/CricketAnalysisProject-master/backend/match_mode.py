import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
import json
from datetime import datetime
import threading
import queue
import time
import logging
import os
from scipy.spatial import distance
from scipy.signal import find_peaks

logger = logging.getLogger(__name__)

@dataclass
class MatchEvent:
    timestamp: float
    event_type: str  # 'boundary', 'wicket', 'dot_ball', 'run', 'review'
    confidence: float
    details: Dict
    frame_number: int

@dataclass
class OverlayMetrics:
    bat_speed: float
    ball_speed: float
    shot_type: str
    shot_quality: str
    runs: int
    extras: int
    current_over: str
    required_rate: float
    match_situation: str

@dataclass
class Ball:
    number: int
    runs: int
    extras: int
    wicket: bool
    shot_type: str
    zone: str
    result: str
    timestamp: datetime

@dataclass
class Over:
    number: int
    balls: List[Ball]
    runs: int
    wickets: int
    extras: int

@dataclass
class Match:
    id: str
    date: datetime
    teams: Dict[str, str]  # team_id: team_name
    players: Dict[str, str]  # player_id: player_name
    overs: List[Over]
    current_over: int
    current_ball: int
    total_runs: int
    total_wickets: int
    status: str  # 'not_started', 'in_progress', 'completed'
    winner: Optional[str]

class MatchMode:
    def __init__(self, data_dir: str = "data/matches"):
        """
        Initialize the match mode manager.
        
        Args:
            data_dir (str): Directory to store match data
        """
        self.data_dir = data_dir
        self.matches_file = os.path.join(data_dir, "matches.json")
        self._ensure_data_directory()
        self.event_queue = queue.Queue()
        self.metrics_buffer = []
        self.highlights = []
        self.current_overlay = None
        self.is_running = False
        self.frame_buffer = []
        self.buffer_size = 30  # 1 second at 30fps
        
        # Initialize tracking variables
        self.bat_positions = []
        self.ball_positions = []
        self.player_positions = []
        self.impact_zones = []
        self.last_impact_time = 0
        self.impact_cooldown = 1.0  # seconds
        
        # Initialize detection parameters
        self.boundary_threshold = 0.8
        self.wicket_threshold = 0.7
        self.review_threshold = 0.6
        self.lbw_threshold = 0.75
        
        # Load pre-trained models
        self._load_models()
        
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating data directory: {str(e)}")
            raise
            
    def create_match(
        self,
        team1_id: str,
        team1_name: str,
        team2_id: str,
        team2_name: str,
        players: Dict[str, str]
    ) -> Match:
        """
        Create a new match.
        
        Args:
            team1_id (str): First team identifier
            team1_name (str): First team name
            team2_id (str): Second team identifier
            team2_name (str): Second team name
            players (Dict[str, str]): Dictionary of player_id: player_name
            
        Returns:
            Match: New match object
        """
        try:
            match = Match(
                id=f"match_{int(datetime.now().timestamp())}",
                date=datetime.now(),
                teams={
                    team1_id: team1_name,
                    team2_id: team2_name
                },
                players=players,
                overs=[],
                current_over=0,
                current_ball=0,
                total_runs=0,
                total_wickets=0,
                status="not_started",
                winner=None
            )
            
            # Save match
            self._save_match(match)
            
            return match
            
        except Exception as e:
            logger.error(f"Error creating match: {str(e)}")
            raise
            
    def start_match(self, match_id: str) -> Match:
        """
        Start a match.
        
        Args:
            match_id (str): Match identifier
            
        Returns:
            Match: Updated match object
        """
        try:
            match = self._load_match(match_id)
            if not match:
                raise ValueError(f"Match {match_id} not found")
            
            match.status = "in_progress"
            match.current_over = 1
            match.current_ball = 1
            
            # Create first over
            match.overs.append(Over(
                number=1,
                balls=[],
                runs=0,
                wickets=0,
                extras=0
            ))
            
            # Save updated match
            self._save_match(match)
            
            return match
            
        except Exception as e:
            logger.error(f"Error starting match: {str(e)}")
            raise
            
    def record_ball(
        self,
        match_id: str,
        runs: int,
        extras: int = 0,
        wicket: bool = False,
        shot_type: str = None,
        zone: str = None,
        result: str = None
    ) -> Match:
        """
        Record a ball in the current match.
        
        Args:
            match_id (str): Match identifier
            runs (int): Runs scored
            extras (int): Extra runs
            wicket (bool): Whether a wicket was taken
            shot_type (str): Type of shot played
            zone (str): Zone where the ball was played
            result (str): Result of the ball
            
        Returns:
            Match: Updated match object
        """
        try:
            match = self._load_match(match_id)
            if not match:
                raise ValueError(f"Match {match_id} not found")
            
            if match.status != "in_progress":
                raise ValueError("Match is not in progress")
            
            # Create ball object
            ball = Ball(
                number=match.current_ball,
                runs=runs,
                extras=extras,
                wicket=wicket,
                shot_type=shot_type,
                zone=zone,
                result=result,
                timestamp=datetime.now()
            )
            
            # Add ball to current over
            current_over = match.overs[-1]
            current_over.balls.append(ball)
            current_over.runs += runs + extras
            if wicket:
                current_over.wickets += 1
            
            # Update match totals
            match.total_runs += runs + extras
            if wicket:
                match.total_wickets += 1
            
            # Update ball count
            match.current_ball += 1
            
            # Check if over is complete
            if match.current_ball > 6:
                match.current_ball = 1
                match.current_over += 1
                
                # Create new over if match is not complete
                if match.current_over <= 20:  # Assuming 20-over match
                    match.overs.append(Over(
                        number=match.current_over,
                        balls=[],
                        runs=0,
                        wickets=0,
                        extras=0
                    ))
                else:
                    match.status = "completed"
            
            # Save updated match
            self._save_match(match)
            
            return match
            
        except Exception as e:
            logger.error(f"Error recording ball: {str(e)}")
            raise
            
    def end_match(self, match_id: str, winner_id: str) -> Match:
        """
        End a match and declare the winner.
        
        Args:
            match_id (str): Match identifier
            winner_id (str): Winning team identifier
            
        Returns:
            Match: Updated match object
        """
        try:
            match = self._load_match(match_id)
            if not match:
                raise ValueError(f"Match {match_id} not found")
            
            if match.status != "in_progress":
                raise ValueError("Match is not in progress")
            
            match.status = "completed"
            match.winner = winner_id
            
            # Save updated match
            self._save_match(match)
            
            return match
            
        except Exception as e:
            logger.error(f"Error ending match: {str(e)}")
            raise
            
    def get_match_summary(self, match_id: str) -> Dict[str, Any]:
        """
        Get a summary of the match.
        
        Args:
            match_id (str): Match identifier
            
        Returns:
            Dict[str, Any]: Match summary
        """
        try:
            match = self._load_match(match_id)
            if not match:
                raise ValueError(f"Match {match_id} not found")
            
            # Calculate over-by-over statistics
            over_stats = []
            for over in match.overs:
                over_stats.append({
                    "over_number": over.number,
                    "runs": over.runs,
                    "wickets": over.wickets,
                    "extras": over.extras,
                    "run_rate": over.runs / len(over.balls) if over.balls else 0
                })
            
            # Calculate shot distribution
            shot_distribution = {}
            for over in match.overs:
                for ball in over.balls:
                    if ball.shot_type:
                        shot_distribution[ball.shot_type] = shot_distribution.get(ball.shot_type, 0) + 1
            
            # Calculate zone distribution
            zone_distribution = {}
            for over in match.overs:
                for ball in over.balls:
                    if ball.zone:
                        zone_distribution[ball.zone] = zone_distribution.get(ball.zone, 0) + 1
            
            return {
                "match_id": match.id,
                "date": match.date.isoformat(),
                "teams": match.teams,
                "status": match.status,
                "winner": match.winner,
                "total_runs": match.total_runs,
                "total_wickets": match.total_wickets,
                "current_over": match.current_over,
                "current_ball": match.current_ball,
                "over_stats": over_stats,
                "shot_distribution": shot_distribution,
                "zone_distribution": zone_distribution
            }
            
        except Exception as e:
            logger.error(f"Error getting match summary: {str(e)}")
            raise
            
    def _load_match(self, match_id: str) -> Optional[Match]:
        """
        Load a match from file.
        
        Args:
            match_id (str): Match identifier
            
        Returns:
            Optional[Match]: Loaded match if found
        """
        try:
            if os.path.exists(self.matches_file):
                with open(self.matches_file, 'r') as f:
                    matches = json.load(f)
                    if match_id in matches:
                        return Match(**matches[match_id])
            return None
            
        except Exception as e:
            logger.error(f"Error loading match: {str(e)}")
            return None
            
    def _save_match(self, match: Match) -> None:
        """
        Save a match to file.
        
        Args:
            match (Match): Match to save
        """
        try:
            # Load existing matches
            matches = {}
            if os.path.exists(self.matches_file):
                with open(self.matches_file, 'r') as f:
                    matches = json.load(f)
            
            # Update matches
            matches[match.id] = {
                "id": match.id,
                "date": match.date.isoformat(),
                "teams": match.teams,
                "players": match.players,
                "overs": [
                    {
                        "number": over.number,
                        "balls": [
                            {
                                "number": ball.number,
                                "runs": ball.runs,
                                "extras": ball.extras,
                                "wicket": ball.wicket,
                                "shot_type": ball.shot_type,
                                "zone": ball.zone,
                                "result": ball.result,
                                "timestamp": ball.timestamp.isoformat()
                            }
                            for ball in over.balls
                        ],
                        "runs": over.runs,
                        "wickets": over.wickets,
                        "extras": over.extras
                    }
                    for over in match.overs
                ],
                "current_over": match.current_over,
                "current_ball": match.current_ball,
                "total_runs": match.total_runs,
                "total_wickets": match.total_wickets,
                "status": match.status,
                "winner": match.winner
            }
            
            # Save updated matches
            with open(self.matches_file, 'w') as f:
                json.dump(matches, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving match: {str(e)}")
            raise
        
    def start_analysis(self, video_path: str):
        """Start real-time match analysis"""
        self.is_running = True
        self.cap = cv2.VideoCapture(video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # Start processing threads
        threading.Thread(target=self._process_frames, daemon=True).start()
        threading.Thread(target=self._generate_highlights, daemon=True).start()
        
    def _process_frames(self):
        """Process video frames in real-time"""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Add frame to buffer
            self.frame_buffer.append(frame)
            if len(self.frame_buffer) > self.buffer_size:
                self.frame_buffer.pop(0)
            
            # Process frame for events and metrics
            events = self._detect_events(frame)
            metrics = self._calculate_metrics(frame)
            
            # Update overlay
            self.current_overlay = self._create_overlay(frame, metrics)
            
            # Queue events for highlight generation
            for event in events:
                self.event_queue.put(event)
                
    def _detect_events(self, frame) -> List[MatchEvent]:
        """Detect significant match events"""
        events = []
        
        # Detect boundaries
        if self._detect_boundary(frame):
            events.append(MatchEvent(
                timestamp=time.time(),
                event_type='boundary',
                confidence=0.9,
                details={'type': 'boundary'},
                frame_number=len(self.frame_buffer)
            ))
            
        # Detect wickets
        if self._detect_wicket(frame):
            events.append(MatchEvent(
                timestamp=time.time(),
                event_type='wicket',
                confidence=0.85,
                details={'type': 'wicket'},
                frame_number=len(self.frame_buffer)
            ))
            
        # Detect reviews
        if self._detect_review(frame):
            events.append(MatchEvent(
                timestamp=time.time(),
                event_type='review',
                confidence=0.8,
                details={'type': 'review'},
                frame_number=len(self.frame_buffer)
            ))
            
        return events
        
    def _calculate_metrics(self, frame) -> OverlayMetrics:
        """Calculate real-time metrics for overlay"""
        # Calculate bat speed
        bat_speed = self._calculate_bat_speed(frame)
        
        # Calculate ball speed
        ball_speed = self._calculate_ball_speed(frame)
        
        # Detect shot type and quality
        shot_type, shot_quality = self._analyze_shot(frame)
        
        # Get match situation
        runs, extras, current_over, required_rate = self._get_match_situation()
        
        return OverlayMetrics(
            bat_speed=bat_speed,
            ball_speed=ball_speed,
            shot_type=shot_type,
            shot_quality=shot_quality,
            runs=runs,
            extras=extras,
            current_over=current_over,
            required_rate=required_rate,
            match_situation=self._get_match_situation_text()
        )
        
    def _create_overlay(self, frame, metrics: OverlayMetrics) -> np.ndarray:
        """Create real-time overlay with metrics"""
        overlay = frame.copy()
        
        # Add metrics to overlay
        cv2.putText(overlay, f"Bat Speed: {metrics.bat_speed:.1f} km/h", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(overlay, f"Ball Speed: {metrics.ball_speed:.1f} km/h", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(overlay, f"Shot: {metrics.shot_type}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(overlay, f"Quality: {metrics.shot_quality}", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add match situation
        cv2.putText(overlay, f"Runs: {metrics.runs}/{metrics.extras}", (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(overlay, f"Over: {metrics.current_over}", (10, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(overlay, f"RRR: {metrics.required_rate:.2f}", (10, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return overlay
        
    def _generate_highlights(self):
        """Generate highlights from detected events"""
        while self.is_running:
            try:
                event = self.event_queue.get(timeout=1)
                
                # Get relevant frames from buffer
                start_frame = max(0, event.frame_number - 15)  # 0.5s before
                end_frame = min(len(self.frame_buffer), event.frame_number + 15)  # 0.5s after
                
                highlight_clip = self.frame_buffer[start_frame:end_frame]
                
                # Save highlight
                self._save_highlight(highlight_clip, event)
                
            except queue.Empty:
                continue
                
    def _save_highlight(self, frames: List[np.ndarray], event: MatchEvent):
        """Save highlight clip to file"""
        if not frames:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"highlights/{timestamp}_{event.event_type}.mp4"
        
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))
        
        for frame in frames:
            out.write(frame)
            
        out.release()
        
        # Add to highlights list
        self.highlights.append({
            'filename': filename,
            'event_type': event.event_type,
            'timestamp': event.timestamp,
            'confidence': event.confidence,
            'details': event.details
        })
        
    def get_current_overlay(self) -> Optional[np.ndarray]:
        """Get the current overlay frame"""
        return self.current_overlay
        
    def get_highlights(self) -> List[Dict]:
        """Get list of generated highlights"""
        return self.highlights
        
    def stop_analysis(self):
        """Stop match analysis"""
        self.is_running = False
        if hasattr(self, 'cap'):
            self.cap.release()
            
    # Helper methods for event detection
    def _detect_boundary(self, frame) -> bool:
        """Detect if a boundary was scored using ball tracking and field detection"""
        try:
            # Detect ball position
            ball_pos = self._track_ball(frame)
            if ball_pos is None:
                return False
            
            # Check if ball is near boundary
            frame_height, frame_width = frame.shape[:2]
            boundary_zone = 0.1  # 10% of frame width/height
            
            is_near_boundary = (
                ball_pos[0] < boundary_zone * frame_width or
                ball_pos[0] > (1 - boundary_zone) * frame_width or
                ball_pos[1] < boundary_zone * frame_height or
                ball_pos[1] > (1 - boundary_zone) * frame_height
            )
            
            # Check if ball is moving towards boundary
            if len(self.ball_positions) >= 2:
                prev_pos = self.ball_positions[-2]
                velocity = np.array(ball_pos) - np.array(prev_pos)
                speed = np.linalg.norm(velocity)
                
                if is_near_boundary and speed > 10:  # Minimum speed threshold
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in boundary detection: {str(e)}")
            return False
        
    def _detect_wicket(self, frame) -> bool:
        """Detect if a wicket was taken using player and ball tracking"""
        try:
            # Detect players and ball
            players = self._detect_players(frame)
            ball_pos = self._track_ball(frame)
            
            if ball_pos is None or not players:
                return False
            
            # Check for ball-bat impact
            impact_detected = self._detect_impact(frame)
            
            # Check for stumps disturbance
            stumps_disturbed = self._check_stumps_disturbance(frame)
            
            # Check for player reaction
            player_reaction = self._detect_player_reaction(frame, players)
            
            # Combine evidence
            evidence_score = (
                0.4 * impact_detected +
                0.4 * stumps_disturbed +
                0.2 * player_reaction
            )
            
            return evidence_score > self.wicket_threshold
            
        except Exception as e:
            logger.error(f"Error in wicket detection: {str(e)}")
            return False
        
    def _detect_review(self, frame) -> bool:
        """Detect if a review is being taken using player and umpire tracking"""
        try:
            # Detect players and umpires
            players = self._detect_players(frame)
            umpires = self._detect_umpires(frame)
            
            if not players or not umpires:
                return False
            
            # Check for review signal
            review_signal = self._detect_review_signal(frame, umpires)
            
            # Check for player appeal
            player_appeal = self._detect_player_appeal(frame, players)
            
            # Check for third umpire communication
            third_umpire_comm = self._detect_third_umpire_comm(frame)
            
            # Combine evidence
            evidence_score = (
                0.4 * review_signal +
                0.3 * player_appeal +
                0.3 * third_umpire_comm
            )
            
            return evidence_score > self.review_threshold
            
        except Exception as e:
            logger.error(f"Error in review detection: {str(e)}")
            return False
        
    def _calculate_bat_speed(self, frame) -> float:
        """Calculate bat speed using motion tracking"""
        try:
            # Track bat position
            bat_pos = self._track_bat(frame)
            if bat_pos is None or len(self.bat_positions) < 2:
                return 0.0
            
            # Calculate velocity
            prev_pos = self.bat_positions[-2]
            velocity = np.array(bat_pos) - np.array(prev_pos)
            speed = np.linalg.norm(velocity)
            
            # Convert to km/h (assuming 30fps video)
            speed_kmh = speed * 30 * 3.6
            
            return speed_kmh
            
        except Exception as e:
            logger.error(f"Error in bat speed calculation: {str(e)}")
            return 0.0
        
    def _calculate_ball_speed(self, frame) -> float:
        """Calculate ball speed using trajectory analysis"""
        try:
            # Track ball position
            ball_pos = self._track_ball(frame)
            if ball_pos is None or len(self.ball_positions) < 2:
                return 0.0
            
            # Calculate velocity
            prev_pos = self.ball_positions[-2]
            velocity = np.array(ball_pos) - np.array(prev_pos)
            speed = np.linalg.norm(velocity)
            
            # Convert to km/h (assuming 30fps video)
            speed_kmh = speed * 30 * 3.6
            
            return speed_kmh
            
        except Exception as e:
            logger.error(f"Error in ball speed calculation: {str(e)}")
            return 0.0
        
    def _analyze_shot(self, frame) -> Tuple[str, str]:
        """Analyze shot type and quality using pose estimation and shot classification"""
        try:
            # Detect player pose
            pose = self._estimate_pose(frame)
            if pose is None:
                return "unknown", "unknown"
            
            # Extract shot features
            shot_features = self._extract_shot_features(frame, pose)
            
            # Classify shot type
            shot_type = self._classify_shot(shot_features)
            
            # Assess shot quality
            shot_quality = self._assess_shot_quality(shot_features)
            
            return shot_type, shot_quality
            
        except Exception as e:
            logger.error(f"Error in shot analysis: {str(e)}")
            return "unknown", "unknown"
        
    def _predict_lbw(self, frame) -> Tuple[bool, float]:
        """Predict LBW using ball tracking and impact analysis"""
        try:
            # Track ball trajectory
            ball_pos = self._track_ball(frame)
            if ball_pos is None:
                return False, 0.0
            
            # Detect player position
            player_pos = self._detect_batsman(frame)
            if player_pos is None:
                return False, 0.0
            
            # Calculate impact point
            impact_point = self._calculate_impact_point(ball_pos, player_pos)
            
            # Check if impact is in line with stumps
            in_line = self._check_impact_line(impact_point)
            
            # Calculate probability
            probability = self._calculate_lbw_probability(impact_point, in_line)
            
            return probability > self.lbw_threshold, probability
            
        except Exception as e:
            logger.error(f"Error in LBW prediction: {str(e)}")
            return False, 0.0
        
    # Helper methods for tracking and detection
    def _track_ball(self, frame) -> Optional[Tuple[float, float]]:
        """Track ball position using computer vision"""
        try:
            # Convert frame to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define ball color range
            lower = np.array([0, 100, 100])
            upper = np.array([10, 255, 255])
            
            # Create mask
            mask = cv2.inRange(hsv, lower, upper)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get largest contour
                ball_contour = max(contours, key=cv2.contourArea)
                
                # Get center
                M = cv2.moments(ball_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Update ball positions
                    self.ball_positions.append((cx, cy))
                    if len(self.ball_positions) > 30:  # Keep last 30 positions
                        self.ball_positions.pop(0)
                    
                    return (cx, cy)
            
            return None
            
        except Exception as e:
            logger.error(f"Error in ball tracking: {str(e)}")
            return None
    
    def _track_bat(self, frame) -> Optional[Tuple[float, float]]:
        """Track bat position using pose estimation"""
        try:
            # Detect player pose
            pose = self._estimate_pose(frame)
            if pose is None:
                return None
            
            # Get bat position from pose
            bat_pos = self._get_bat_position(pose)
            
            # Update bat positions
            self.bat_positions.append(bat_pos)
            if len(self.bat_positions) > 30:  # Keep last 30 positions
                self.bat_positions.pop(0)
            
            return bat_pos
            
        except Exception as e:
            logger.error(f"Error in bat tracking: {str(e)}")
            return None
    
    def _detect_players(self, frame):
        """Detect players in the frame."""
        if self.player_detector is None:
            return []
            
        try:
            # Prepare frame for detection
            blob = cv2.dnn.blobFromImage(
                frame, 1/255.0, (416, 416),
                swapRB=True, crop=False
            )
            
            # Set input and run detection
            self.player_detector.setInput(blob)
            layer_names = self.player_detector.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.player_detector.getUnconnectedOutLayers()]
            outputs = self.player_detector.forward(output_layers)
            
            # Process detections
            height, width = frame.shape[:2]
            boxes = []
            confidences = []
            
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > 0.5 and class_id == 0:  # 0 is person class
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        x = int(center_x - w/2)
                        y = int(center_y - h/2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
            
            # Apply non-maximum suppression
            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            
            return [boxes[i] for i in indices]
            
        except Exception as e:
            logger.error(f"Error in player detection: {str(e)}")
            return []

    def _estimate_pose(self, frame, bbox):
        """Estimate player pose."""
        if self.pose_estimator is None:
            return None
            
        try:
            x, y, w, h = bbox
            player = frame[y:y+h, x:x+w]
            
            # Resize for pose estimation
            player = cv2.resize(player, (368, 368))
            
            # Prepare input
            blob = cv2.dnn.blobFromImage(
                player, 1/255.0, (368, 368),
                (0, 0, 0), swapRB=False, crop=False
            )
            
            # Run pose estimation
            self.pose_estimator.setInput(blob)
            output = self.pose_estimator.forward()
            
            # Process output
            points = []
            for i in range(15):  # 15 keypoints
                probMap = output[0, i, :, :]
                probMap = cv2.resize(probMap, (w, h))
                
                minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
                
                if prob > 0.1:
                    points.append((x + point[0], y + point[1]))
                else:
                    points.append(None)
            
            return points
            
        except Exception as e:
            logger.error(f"Error in pose estimation: {str(e)}")
            return None

    def _classify_shot(self, frame, bbox, pose_points):
        """Classify cricket shot."""
        if self.shot_classifier is None:
            return "unknown", 0.0
            
        try:
            x, y, w, h = bbox
            player = frame[y:y+h, x:x+w]
            
            # Resize for classification
            player = cv2.resize(player, (224, 224))
            
            # Prepare input
            blob = cv2.dnn.blobFromImage(
                player, 1/255.0, (224, 224),
                (0, 0, 0), swapRB=True, crop=False
            )
            
            # Run classification
            self.shot_classifier.setInput(blob)
            output = self.shot_classifier.forward()
            
            # Get prediction
            shot_types = ['defense', 'drive', 'pull', 'sweep', 'cut']
            shot_idx = np.argmax(output[0])
            confidence = float(output[0][shot_idx])
            
            return shot_types[shot_idx], confidence
            
        except Exception as e:
            logger.error(f"Error in shot classification: {str(e)}")
            return "unknown", 0.0
        
    def _detect_impact(self, frame) -> bool:
        """Detect ball-bat impact using motion analysis"""
        try:
            current_time = time.time()
            if current_time - self.last_impact_time < self.impact_cooldown:
                return False
            
            # Get ball and bat positions
            ball_pos = self._track_ball(frame)
            bat_pos = self._track_bat(frame)
            
            if ball_pos is None or bat_pos is None:
                return False
            
            # Calculate distance
            dist = distance.euclidean(ball_pos, bat_pos)
            
            # Check for impact
            if dist < 20:  # Impact threshold
                self.last_impact_time = current_time
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error in impact detection: {str(e)}")
            return False
    
    def _check_stumps_disturbance(self, frame) -> bool:
        """Check if stumps were disturbed using motion analysis"""
        try:
            # Define stump region
            height, width = frame.shape[:2]
            stump_region = frame[int(height*0.4):int(height*0.6), int(width*0.45):int(width*0.55)]
            
            # Calculate motion
            if len(self.frame_buffer) > 1:
                prev_frame = self.frame_buffer[-2]
                prev_stump_region = prev_frame[int(height*0.4):int(height*0.6), int(width*0.45):int(width*0.55)]
                
                # Calculate difference
                diff = cv2.absdiff(stump_region, prev_stump_region)
                motion = np.mean(diff)
                
                return motion > 30  # Motion threshold
            
            return False
            
        except Exception as e:
            logger.error(f"Error in stump disturbance check: {str(e)}")
            return False
    
    def _detect_player_reaction(self, frame, players: List[Dict]) -> float:
        """Detect player reaction to wicket"""
        try:
            if not players:
                return 0.0
            
            # Get player pose
            pose = self._estimate_pose(frame)
            if pose is None:
                return 0.0
            
            # Analyze pose for celebration/reaction
            reaction_score = self._analyze_pose_for_reaction(pose)
            
            return reaction_score
            
        except Exception as e:
            logger.error(f"Error in player reaction detection: {str(e)}")
            return 0.0
    
    def _analyze_pose_for_reaction(self, pose: np.ndarray) -> float:
        """Analyze pose for celebration/reaction"""
        try:
            if pose is None:
                return 0.0
            
            # Check for raised arms
            arms_raised = self._check_arms_raised(pose)
            
            # Check for jumping
            jumping = self._check_jumping(pose)
            
            # Check for running
            running = self._check_running(pose)
            
            # Combine scores
            reaction_score = (
                0.4 * arms_raised +
                0.3 * jumping +
                0.3 * running
            )
            
            return reaction_score
            
        except Exception as e:
            logger.error(f"Error in pose analysis: {str(e)}")
            return 0.0
    
    def _check_arms_raised(self, pose: np.ndarray) -> float:
        """Check if player's arms are raised"""
        try:
            if pose is None:
                return 0.0
            
            # Get shoulder and wrist positions
            left_shoulder = pose[5]
            right_shoulder = pose[2]
            left_wrist = pose[7]
            right_wrist = pose[4]
            
            if None in [left_shoulder, right_shoulder, left_wrist, right_wrist]:
                return 0.0
            
            # Check if wrists are above shoulders
            arms_raised = (
                left_wrist[1] < left_shoulder[1] and
                right_wrist[1] < right_shoulder[1]
            )
            
            return 1.0 if arms_raised else 0.0
            
        except Exception as e:
            logger.error(f"Error in arms raised check: {str(e)}")
            return 0.0
    
    def _check_jumping(self, pose: np.ndarray) -> float:
        """Check if player is jumping"""
        try:
            if pose is None:
                return 0.0
            
            # Get ankle positions
            left_ankle = pose[15]
            right_ankle = pose[12]
            
            if None in [left_ankle, right_ankle]:
                return 0.0
            
            # Check if ankles are off ground
            ankles_off_ground = (
                left_ankle[1] < 0.8 and  # Normalized height
                right_ankle[1] < 0.8
            )
            
            return 1.0 if ankles_off_ground else 0.0
            
        except Exception as e:
            logger.error(f"Error in jumping check: {str(e)}")
            return 0.0
    
    def _check_running(self, pose: np.ndarray) -> float:
        """Check if player is running"""
        try:
            if pose is None:
                return 0.0
            
            # Get hip and knee positions
            left_hip = pose[11]
            right_hip = pose[8]
            left_knee = pose[13]
            right_knee = pose[10]
            
            if None in [left_hip, right_hip, left_knee, right_knee]:
                return 0.0
            
            # Check for running motion
            running_motion = (
                abs(left_hip[1] - left_knee[1]) > 0.2 and  # Leg extension
                abs(right_hip[1] - right_knee[1]) > 0.2
            )
            
            return 1.0 if running_motion else 0.0
            
        except Exception as e:
            logger.error(f"Error in running check: {str(e)}")
            return 0.0
    
    def _load_models(self):
        """Load required ML models."""
        try:
            # Create models directory if it doesn't exist
            os.makedirs('models', exist_ok=True)
            
            # Initialize all models as None
            self.player_detector = None
            self.pose_estimator = None
            self.shot_classifier = None
            
            # Check if YOLOv4 model files exist
            cfg_path = os.path.join('models', 'yolov4.cfg')
            weights_path = os.path.join('models', 'yolov4.weights')
            
            if os.path.exists(cfg_path) and os.path.exists(weights_path):
                try:
                    # Load YOLOv4 for player detection
                    self.player_detector = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
                    logger.info("Successfully loaded YOLOv4 model")
                except Exception as e:
                    logger.warning(f"Failed to load YOLOv4 model: {str(e)}")
            else:
                logger.warning("YOLOv4 model files not found. Player detection will be disabled.")
                logger.info("Please download the model files from: https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights")
                logger.info("And place them in the 'models' directory.")
            
            # Check if pose estimation model exists
            pose_model_path = 'models/graph_opt.pb'
            if os.path.exists(pose_model_path):
                try:
                    # Load pose estimation model
                    self.pose_estimator = cv2.dnn.readNetFromTensorflow(pose_model_path)
                    logger.info("Successfully loaded pose estimation model")
                except Exception as e:
                    logger.warning(f"Failed to load pose estimation model: {str(e)}")
            else:
                logger.warning("Pose estimation model (graph_opt.pb) not found. Pose estimation will be disabled.")
            
            # Check if shot classification model exists
            shot_model_path = 'models/shot_classifier.pb'
            if os.path.exists(shot_model_path):
                try:
                    # Load shot classification model
                    self.shot_classifier = cv2.dnn.readNetFromTensorflow(shot_model_path)
                    logger.info("Successfully loaded shot classification model")
                except Exception as e:
                    logger.warning(f"Failed to load shot classification model: {str(e)}")
            else:
                logger.warning("Shot classification model (shot_classifier.pb) not found. Shot classification will be disabled.")
            
            # Log summary of loaded models
            loaded_models = []
            if self.player_detector is not None:
                loaded_models.append("YOLOv4")
            if self.pose_estimator is not None:
                loaded_models.append("Pose Estimation")
            if self.shot_classifier is not None:
                loaded_models.append("Shot Classification")
            
            if loaded_models:
                logger.info(f"Successfully loaded models: {', '.join(loaded_models)}")
            else:
                logger.warning("No ML models loaded. Advanced features will be disabled.")
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            self.player_detector = None
            self.pose_estimator = None
            self.shot_classifier = None
        
    def _get_match_situation(self) -> Tuple[int, int, str, float]:
        """Get current match situation"""
        # Implement match situation tracking
        return 0, 0, "0.0", 0.0
        
    def _get_match_situation_text(self) -> str:
        """Get text description of match situation"""
        # Implement match situation text generation
        return "Match in progress" 