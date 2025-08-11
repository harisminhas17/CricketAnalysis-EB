import cv2
import numpy as np
from typing import List, Dict, Tuple
import threading
import queue
import time
from dataclasses import dataclass
from scipy.spatial.transform import Rotation
from sklearn.cluster import DBSCAN
import logging

@dataclass
class CameraConfig:
    """Camera configuration including intrinsic and extrinsic parameters"""
    camera_id: int
    resolution: Tuple[int, int]
    fps: int
    matrix: np.ndarray  # Camera matrix
    dist_coeffs: np.ndarray  # Distortion coefficients
    rvec: np.ndarray  # Rotation vector
    tvec: np.ndarray  # Translation vector

class MultiCameraTracker:
    def __init__(self):
        self.cameras: Dict[int, CameraConfig] = {}
        self.camera_captures: Dict[int, cv2.VideoCapture] = {}
        self.frame_queues: Dict[int, queue.Queue] = {}
        self.tracking_threads: Dict[int, threading.Thread] = {}
        self.is_running = False
        self.logger = logging.getLogger(__name__)
        
        # 3D tracking parameters
        self.min_triangulation_angle = 5.0  # Minimum angle between cameras for triangulation
        self.max_reprojection_error = 2.0  # Maximum reprojection error in pixels
        self.ball_radius = 0.0364  # Standard cricket ball radius in meters
        
        # Ball detection parameters
        self.ball_color_lower = np.array([0, 0, 0])  # Black ball
        self.ball_color_upper = np.array([180, 255, 50])
        self.min_ball_radius = 5
        self.max_ball_radius = 30
        
        # Trajectory smoothing
        self.trajectory_window = 10
        self.trajectory_points = []
        
    def add_camera(self, camera_id: int, config: CameraConfig) -> bool:
        """Add a camera to the tracking system"""
        try:
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                self.logger.error(f"Failed to open camera {camera_id}")
                return False
                
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.resolution[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.resolution[1])
            cap.set(cv2.CAP_PROP_FPS, config.fps)
            
            self.cameras[camera_id] = config
            self.camera_captures[camera_id] = cap
            self.frame_queues[camera_id] = queue.Queue(maxsize=30)
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding camera {camera_id}: {str(e)}")
            return False
            
    def start_tracking(self):
        """Start the tracking system"""
        if not self.cameras:
            self.logger.error("No cameras configured")
            return False
            
        self.is_running = True
        
        # Start capture threads for each camera
        for camera_id in self.cameras:
            thread = threading.Thread(
                target=self._capture_frames,
                args=(camera_id,),
                daemon=True
            )
            self.tracking_threads[camera_id] = thread
            thread.start()
            
        # Start processing thread
        self.processing_thread = threading.Thread(
            target=self._process_frames,
            daemon=True
        )
        self.processing_thread.start()
        
        return True
        
    def stop_tracking(self):
        """Stop the tracking system"""
        self.is_running = False
        
        # Wait for threads to finish
        for thread in self.tracking_threads.values():
            thread.join(timeout=1.0)
            
        # Release camera captures
        for cap in self.camera_captures.values():
            cap.release()
            
    def _capture_frames(self, camera_id: int):
        """Capture frames from a camera"""
        while self.is_running:
            ret, frame = self.camera_captures[camera_id].read()
            if ret:
                try:
                    self.frame_queues[camera_id].put(frame, block=False)
                except queue.Full:
                    # Drop oldest frame if queue is full
                    try:
                        self.frame_queues[camera_id].get_nowait()
                        self.frame_queues[camera_id].put(frame, block=False)
                    except queue.Empty:
                        pass
            time.sleep(0.001)  # Small delay to prevent CPU overload
                
    def _process_frames(self):
        """Process frames from all cameras and perform 3D tracking"""
        while self.is_running:
            # Get synchronized frames from all cameras
            frames = {}
            for camera_id, queue in self.frame_queues.items():
                try:
                    frames[camera_id] = queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                    
            if len(frames) < 2:
                continue
                
            # Detect ball in each frame
            ball_positions = {}
            for camera_id, frame in frames.items():
                ball_pos = self._detect_ball(frame, camera_id)
                if ball_pos is not None:
                    ball_positions[camera_id] = ball_pos
                    
            # Triangulate 3D position if we have detections from multiple cameras
            if len(ball_positions) >= 2:
                point_3d = self._triangulate_position(ball_positions)
                if point_3d is not None:
                    self._update_trajectory(point_3d)
                
    def _detect_ball(self, frame: np.ndarray, camera_id: int) -> Tuple[float, float]:
        """Detect ball in a frame using color and shape analysis"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for ball color
        mask = cv2.inRange(hsv, self.ball_color_lower, self.ball_color_upper)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and shape
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:  # Minimum area threshold
                continue
                
            # Fit circle to contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            
            if self.min_ball_radius <= radius <= self.max_ball_radius:
                # Check circularity
                circularity = 4 * np.pi * area / (cv2.arcLength(contour, True) ** 2)
                if circularity > 0.8:  # Circle-like shape
                    return center
                    
        return None
        
    def _triangulate_position(self, ball_positions: Dict[int, Tuple[float, float]]) -> np.ndarray:
        """Triangulate 3D position from multiple camera detections"""
        # Convert 2D positions to normalized coordinates
        points_2d = []
        camera_matrices = []
        
        for camera_id, pos in ball_positions.items():
            config = self.cameras[camera_id]
            
            # Undistort point
            undistorted = cv2.undistortPoints(
                np.array([pos], dtype=np.float32),
                config.matrix,
                config.dist_coeffs
            )[0][0]
            
            points_2d.append(undistorted)
            
            # Get camera matrix for triangulation
            rmat, _ = cv2.Rodrigues(config.rvec)
            camera_matrix = np.hstack((rmat, config.tvec.reshape(3, 1)))
            camera_matrices.append(camera_matrix)
            
        # Triangulate 3D point
        points_4d = cv2.triangulatePoints(
            camera_matrices[0],
            camera_matrices[1],
            points_2d[0],
            points_2d[1]
        )
        
        # Convert to 3D coordinates
        point_3d = points_4d[:3] / points_4d[3]
        
        # Calculate reprojection error
        error = self._calculate_reprojection_error(point_3d, ball_positions)
        
        if error < self.max_reprojection_error:
            return point_3d
            
        return None
        
    def _calculate_reprojection_error(self, point_3d: np.ndarray, 
                                    ball_positions: Dict[int, Tuple[float, float]]) -> float:
        """Calculate reprojection error for the triangulated point"""
        total_error = 0
        count = 0
        
        for camera_id, pos in ball_positions.items():
            config = self.cameras[camera_id]
            
            # Project 3D point to 2D
            projected, _ = cv2.projectPoints(
                point_3d.reshape(1, 1, 3),
                config.rvec,
                config.tvec,
                config.matrix,
                config.dist_coeffs
            )
            
            # Calculate error
            error = np.linalg.norm(projected[0][0] - np.array(pos))
            total_error += error
            count += 1
            
        return total_error / count if count > 0 else float('inf')
        
    def _update_trajectory(self, point_3d: np.ndarray):
        """Update the ball trajectory with smoothing"""
        self.trajectory_points.append(point_3d)
        
        # Keep only the last N points
        if len(self.trajectory_points) > self.trajectory_window:
            self.trajectory_points.pop(0)
            
        # Apply DBSCAN clustering to remove outliers
        if len(self.trajectory_points) >= 3:
            clustering = DBSCAN(eps=0.1, min_samples=2).fit(self.trajectory_points)
            if len(set(clustering.labels_)) > 1:
                # Remove outliers (points labeled as -1)
                self.trajectory_points = [
                    point for point, label in zip(self.trajectory_points, clustering.labels_)
                    if label != -1
                ]
        
    def get_trajectory(self) -> List[np.ndarray]:
        """Get the current ball trajectory"""
        return self.trajectory_points.copy() 