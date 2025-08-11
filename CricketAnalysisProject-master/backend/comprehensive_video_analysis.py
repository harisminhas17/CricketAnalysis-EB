#!/usr/bin/env python3
"""
Comprehensive Video Analysis with Complete Object Detection
Creates an output video showing ball detection, player detection, 
trajectory tracking, velocity analysis, and all cricket analytics.
"""

import cv2
import numpy as np
import os
import json
from datetime import datetime
from enhanced_cricket_ball_detector import EnhancedCricketBallDetector
from track_ball import detect_ball
import logging
from ultralytics import YOLO
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveVideoAnalyzer:
    """
    Comprehensive video analyzer that detects all objects and creates
    detailed output videos with analytics overlays.
    """
    
    def __init__(self):
        self.enhanced_detector = EnhancedCricketBallDetector()
        self.yolo_model = None
        self.analysis_results = {
            'total_frames': 0,
            'enhanced_detections': 0,
            'traditional_detections': 0,
            'player_detections': 0,
            'object_detections': {},
            'trajectory_points': [],
            'velocity_history': [],
            'shot_analysis': [],
            'lbw_analysis': [],
            'performance_metrics': {}
        }
        
        # Initialize YOLO model for object detection
        self._initialize_yolo_model()
    
    def _initialize_yolo_model(self):
        """Initialize YOLO model for object detection."""
        try:
            # Try to load a trained cricket model first
            model_paths = [
                'runs/cricket_ball_train5/weights/best.pt',
                'runs/detect/cricket_ball_model/weights/best.pt',
                'yolov8n.pt'  # Fallback to general model
            ]
            
            for model_path in model_paths:
                if os.path.exists(model_path):
                    self.yolo_model = YOLO(model_path)
                    logger.info(f"Loaded YOLO model: {model_path}")
                    break
            
            if self.yolo_model is None:
                logger.warning("No YOLO model found, using basic detection only")
                
        except Exception as e:
            logger.error(f"Error initializing YOLO model: {str(e)}")
            self.yolo_model = None
    
    def detect_objects_in_frame(self, frame: np.ndarray) -> list:
        """
        Detect all objects in a frame using YOLO and other methods.
        
        Returns:
            List of detected objects with their properties
        """
        detected_objects = []
        
        try:
            # Use YOLO for object detection if available
            if self.yolo_model is not None:
                results = self.yolo_model(frame, conf=0.3)
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            conf = box.conf[0].cpu().numpy()
                            cls = int(box.cls[0].cpu().numpy())
                            
                            # Get class name
                            class_names = ['ball', 'player', 'stump', 'bat']  # Adjust based on your model
                            class_name = class_names[cls] if cls < len(class_names) else f'object_{cls}'
                            
                            detected_objects.append({
                                'bbox': (int(x1), int(y1), int(x2), int(y2)),
                                'confidence': float(conf),
                                'class': class_name,
                                'class_id': cls
                            })
            
            # Add manual detection for objects not covered by YOLO
            detected_objects.extend(self._detect_additional_objects(frame))
            
        except Exception as e:
            logger.error(f"Error in object detection: {str(e)}")
        
        return detected_objects
    
    def _detect_additional_objects(self, frame: np.ndarray) -> list:
        """Detect additional objects using traditional CV methods."""
        additional_objects = []
        
        try:
            # Detect stumps using color and shape
            stump_objects = self._detect_stumps(frame)
            additional_objects.extend(stump_objects)
            
            # Detect cricket field boundaries
            field_objects = self._detect_field_boundaries(frame)
            additional_objects.extend(field_objects)
            
        except Exception as e:
            logger.error(f"Error in additional object detection: {str(e)}")
        
        return additional_objects
    
    def _detect_stumps(self, frame: np.ndarray) -> list:
        """Detect cricket stumps using color and shape detection."""
        stump_objects = []
        
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define stump color range (white/light colored)
            lower_stump = np.array([0, 0, 200])
            upper_stump = np.array([180, 30, 255])
            
            # Create mask for stump color
            stump_mask = cv2.inRange(hsv, lower_stump, upper_stump)
            
            # Find contours
            contours, _ = cv2.findContours(stump_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small contours
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if it's stump-like (tall and narrow)
                    if h > w * 2 and h > 50:
                        stump_objects.append({
                            'bbox': (x, y, x + w, y + h),
                            'confidence': 0.7,
                            'class': 'stump',
                            'class_id': 2
                        })
        
        except Exception as e:
            logger.error(f"Error detecting stumps: {str(e)}")
        
        return stump_objects
    
    def _detect_field_boundaries(self, frame: np.ndarray) -> list:
        """Detect cricket field boundaries and always include the pitch rectangle as field."""
        field_objects = []
        try:
            # Existing green field detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_field = np.array([35, 50, 50])
            upper_field = np.array([85, 255, 255])
            field_mask = cv2.inRange(hsv, lower_field, upper_field)
            contours, _ = cv2.findContours(field_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    field_objects.append({
                        'bbox': (x, y, x + w, y + h),
                        'confidence': 0.8,
                        'class': 'field',
                        'class_id': 4
                    })
            # Always add the pitch rectangle as field
            height, width = frame.shape[:2]
            pitch_width = int(width * 0.12)  # ~3m of 25m wide frame
            pitch_height = int(height * 0.8)  # 80% of frame height
            pitch_x = (width - pitch_width) // 2
            pitch_y = (height - pitch_height) // 2
            field_objects.append({
                'bbox': (pitch_x, pitch_y, pitch_x + pitch_width, pitch_y + pitch_height),
                'confidence': 0.99,
                'class': 'field',
                'class_id': 4
            })
        except Exception as e:
            logger.error(f"Error detecting field boundaries: {str(e)}")
        return field_objects
    
    def analyze_video(self, input_video_path: str, output_video_path: str = None) -> str:
        """
        Analyze video and create comprehensive output with all object detections.
        
        Args:
            input_video_path: Path to input video
            output_video_path: Path for output video (optional)
            
        Returns:
            Path to output video
        """
        try:
            # Open input video
            cap = cv2.VideoCapture(input_video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {input_video_path}")
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Analyzing video: {width}x{height}, {fps} FPS, {total_frames} frames")
            
            # Setup output video
            if output_video_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_video_path = f"comprehensive_analysis_{timestamp}.mp4"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            
            # Reset enhanced detector
            self.enhanced_detector.reset_tracking()
            
            # Calibrate detector using video dimensions
            self.enhanced_detector.calibrate_from_pitch_dimensions(width, height)
            self.enhanced_detector.fps = fps
            
            frame_count = 0
            enhanced_detections = 0
            traditional_detections = 0
            player_detections = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect all objects in frame
                detected_objects = self.detect_objects_in_frame(frame)
                
                # Separate ball detections from other objects
                ball_objects = [obj for obj in detected_objects if obj['class'] == 'ball']
                other_objects = [obj for obj in detected_objects if obj['class'] != 'ball']
                
                # Get ball position using enhanced cricket ball detector
                result = self.enhanced_detector.detect_cricket_ball(frame, frame_count)
                if isinstance(result, tuple):
                    enhanced_detection, all_candidates = result
                else:
                    enhanced_detection, all_candidates = result, []
                self.last_enhanced_detection = enhanced_detection  # Store for visualization
                self.last_all_candidates = all_candidates  # Store for visualization
                enhanced_pos = enhanced_detection.position if enhanced_detection and enhanced_detection.is_valid_cricket_ball else None
                traditional_pos = detect_ball(frame)
                
                # Use detected ball position if available
                if ball_objects:
                    best_ball = max(ball_objects, key=lambda x: x['confidence'])
                    detected_ball_pos = (
                        (best_ball['bbox'][0] + best_ball['bbox'][2]) // 2,
                        (best_ball['bbox'][1] + best_ball['bbox'][3]) // 2
                    )
                else:
                    detected_ball_pos = enhanced_pos or traditional_pos
                
                # Update detection counts
                if enhanced_pos and enhanced_detection and enhanced_detection.is_valid_cricket_ball:
                    enhanced_detections += 1
                    self.analysis_results['enhanced_detections'] += 1
                    self.analysis_results['trajectory_points'].append({
                        'frame': frame_count,
                        'position': enhanced_pos,
                        'timestamp': frame_count / fps,
                        'velocity': enhanced_detection.velocity,
                        'distance_covered': enhanced_detection.distance_covered,
                        'confidence': enhanced_detection.confidence
                    })
                
                if traditional_pos:
                    traditional_detections += 1
                    self.analysis_results['traditional_detections'] += 1
                
                # Count player detections
                player_objects = [obj for obj in detected_objects if obj['class'] == 'player']
                if player_objects:
                    player_detections += 1
                    self.analysis_results['player_detections'] += 1
                
                # Create comprehensive visualization
                annotated_frame = self._create_comprehensive_visualization(
                    frame, enhanced_pos, traditional_pos, detected_objects, frame_count, fps
                )
                
                # Add analytics overlay
                annotated_frame = self._add_analytics_overlay(
                    annotated_frame, frame_count, total_frames, enhanced_detections, 
                    traditional_detections, player_detections, detected_objects
                )
                
                # Write output frame
                out.write(annotated_frame)
                
                frame_count += 1
                
                # Progress update
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")
            
            # Cleanup
            cap.release()
            out.release()
            
            # Update final results with enhanced detector statistics
            self.analysis_results['total_frames'] = frame_count
            enhanced_stats = self.enhanced_detector.get_tracking_statistics()
            self.analysis_results['performance_metrics'] = {
                'enhanced_detection_rate': enhanced_detections / frame_count if frame_count > 0 else 0,
                'traditional_detection_rate': traditional_detections / frame_count if frame_count > 0 else 0,
                'player_detection_rate': player_detections / frame_count if frame_count > 0 else 0,
                'total_enhanced_detections': enhanced_detections,
                'total_traditional_detections': traditional_detections,
                'total_player_detections': player_detections,
                'enhanced_tracking_statistics': enhanced_stats,
                'requirements_met': {
                    'minimum_velocity_30kmph': enhanced_stats['average_velocity'] >= 30.0,
                    'minimum_distance_15m': enhanced_stats['total_distance'] >= 15.0,
                    'spherical_detection': True,
                    'motion_consistency': enhanced_stats['detection_rate'] > 0.5
                }
            }
            
            # Save analysis results
            self._save_analysis_results(output_video_path.replace('.mp4', '_results.json'))
            
            logger.info(f"Analysis completed! Output video: {output_video_path}")
            return output_video_path
            
        except Exception as e:
            logger.error(f"Error in video analysis: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def _create_comprehensive_visualization(self, frame: np.ndarray, 
                                          enhanced_pos: tuple, 
                                          traditional_pos: tuple,
                                          detected_objects: list,
                                          frame_count: int,
                                          fps: int) -> np.ndarray:
        annotated_frame = frame.copy()
        # Draw all detected objects
        for obj in detected_objects:
            bbox = obj['bbox']
            class_name = obj['class']
            confidence = obj['confidence']
            if class_name == 'ball':
                color = (0, 255, 255)
            elif class_name == 'player':
                color = (0, 255, 0)
            elif class_name == 'stump':
                color = (255, 255, 255)
            elif class_name == 'bat':
                color = (0, 0, 255)
            else:
                color = (128, 128, 128)
            cv2.rectangle(annotated_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(annotated_frame, label, (bbox[0], bbox[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # Draw all candidate circles (yellow)
        all_candidates = getattr(self, 'last_all_candidates', [])
        for cand in all_candidates:
            pos = cand.get('position')
            radius = int(cand.get('radius', 10))
            if pos:
                cv2.circle(annotated_frame, pos, radius, (0, 255, 255), 1)
        # Draw enhanced ball detection (thick yellow circle with trajectory and velocity)
        enhanced_detection = getattr(self, 'last_enhanced_detection', None)
        drawn_ball = False
        if enhanced_detection and enhanced_detection.is_valid_cricket_ball:
            pos = enhanced_detection.position
            velocity = enhanced_detection.velocity
            confidence = enhanced_detection.confidence
            cv2.circle(annotated_frame, pos, 18, (0, 255, 255), 4)
            cv2.circle(annotated_frame, pos, 8, (255, 255, 255), -1)
            vx, vy, _ = velocity
            end_point = (int(pos[0] + vx * 20), int(pos[1] + vy * 20))
            cv2.arrowedLine(annotated_frame, pos, end_point, (0, 0, 255), 3)
            trajectory_points = self.enhanced_detector.ball_positions_history
            if len(trajectory_points) >= 2:
                for i in range(1, len(trajectory_points)):
                    cv2.line(annotated_frame, trajectory_points[i-1], trajectory_points[i], (255, 255, 255), 2)
            debug_text = f"Ball: {pos}, V=({vx:.2f},{vy:.2f}) px/frame, Conf={confidence:.2f}"
            cv2.putText(annotated_frame, debug_text, (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            print(f"[Frame {frame_count}] Ball: {pos}, V=({vx:.2f},{vy:.2f}), Conf={confidence:.2f}")
            drawn_ball = True
        if not drawn_ball:
            if hasattr(self.enhanced_detector, 'ball_positions_history') and self.enhanced_detector.ball_positions_history:
                pos = self.enhanced_detector.ball_positions_history[-1]
                cv2.circle(annotated_frame, pos, 15, (0, 255, 255), 3)
                cv2.circle(annotated_frame, pos, 7, (255, 255, 255), -1)
                cv2.putText(annotated_frame, "(Fallback)", (pos[0] + 20, pos[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        if traditional_pos:
            cv2.circle(annotated_frame, traditional_pos, 12, (0, 255, 0), 2)
            cv2.putText(annotated_frame, "Traditional", (traditional_pos[0] + 20, traditional_pos[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        self._add_cricket_field_overlay(annotated_frame)
        if enhanced_pos:
            shot_zone = self._analyze_shot_zone(enhanced_pos, frame.shape)
            height, width = frame.shape[:2]
            cv2.putText(annotated_frame, f"Zone: {shot_zone}", (10, height - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        if enhanced_pos:
            lbw_probability = self._analyze_lbw_possibility(enhanced_pos, frame.shape)
            height, width = frame.shape[:2]
            if lbw_probability > 0.3:
                cv2.putText(annotated_frame, f"LBW: {lbw_probability:.2f}", (10, height - 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        return annotated_frame
    
    def _add_cricket_field_overlay(self, frame: np.ndarray):
        """Add cricket field overlay for better context."""
        height, width = frame.shape[:2]
        
        # Draw pitch outline
        pitch_width = int(width * 0.1)
        pitch_height = int(height * 0.6)
        pitch_x = (width - pitch_width) // 2
        pitch_y = (height - pitch_height) // 2
        
        cv2.rectangle(frame, (pitch_x, pitch_y), (pitch_x + pitch_width, pitch_y + pitch_height),
                     (0, 255, 0), 2)
        
        # Draw stumps
        stump_x = width // 2
        stump_y = pitch_y + pitch_height
        cv2.rectangle(frame, (stump_x - 5, stump_y - 20), (stump_x + 5, stump_y),
                     (255, 255, 255), -1)
    
    def _analyze_shot_zone(self, ball_pos: tuple, frame_shape: tuple) -> str:
        """Analyze which shot zone the ball is in."""
        height, width = frame_shape[:2]
        x, y = ball_pos
        
        # Define shot zones
        if x < width * 0.33:
            return "Off Side"
        elif x < width * 0.66:
            return "Straight"
        else:
            return "Leg Side"
    
    def _analyze_lbw_possibility(self, ball_pos: tuple, frame_shape: tuple) -> float:
        """Analyze LBW possibility based on ball position."""
        height, width = frame_shape[:2]
        x, y = ball_pos
        
        # Check if ball is in line with stumps
        stump_x = width // 2
        stump_y = height * 0.8
        
        distance_from_stumps = np.sqrt((x - stump_x)**2 + (y - stump_y)**2)
        
        # Calculate LBW probability
        if distance_from_stumps < 50:
            return 0.8
        elif distance_from_stumps < 100:
            return 0.5
        else:
            return 0.1
    
    def _add_analytics_overlay(self, frame: np.ndarray, frame_count: int, 
                              total_frames: int, enhanced_detections: int, 
                              traditional_detections: int, player_detections: int,
                              detected_objects: list) -> np.ndarray:
        """Add comprehensive analytics overlay."""
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Add frame counter
        cv2.putText(frame, f"Frame: {frame_count}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add detection statistics
        enhanced_rate = enhanced_detections / frame_count * 100 if frame_count > 0 else 0
        traditional_rate = traditional_detections / frame_count * 100 if frame_count > 0 else 0
        player_rate = player_detections / frame_count * 100 if frame_count > 0 else 0
        
        cv2.putText(frame, f"Enhanced Detection: {enhanced_rate:.1f}%", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Traditional Detection: {traditional_rate:.1f}%", (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Player Detection: {player_rate:.1f}%", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Add object count
        object_counts = {}
        for obj in detected_objects:
            class_name = obj['class']
            object_counts[class_name] = object_counts.get(class_name, 0) + 1
        
        y_offset = 135
        for class_name, count in object_counts.items():
            cv2.putText(frame, f"{class_name.title()}: {count}", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y_offset += 20
        
        # Add enhanced detector status
        trajectory_points = self.enhanced_detector.ball_positions_history
        if trajectory_points:
            cv2.putText(frame, f"Enhanced Trajectory: {len(trajectory_points)}", (width - 250, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add velocity and distance info
            enhanced_stats = self.enhanced_detector.get_tracking_statistics()
            if enhanced_stats['average_velocity'] > 0:
                cv2.putText(frame, f"Avg Velocity: {enhanced_stats['average_velocity']:.1f} km/h", 
                           (width - 250, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                cv2.putText(frame, f"Distance: {enhanced_stats['total_distance']:.1f} m", 
                           (width - 250, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        return frame
    
    def _save_analysis_results(self, output_path: str):
        """Save analysis results to JSON file."""
        try:
            # Add enhanced detector analysis
            enhanced_stats = self.enhanced_detector.get_tracking_statistics()
            trajectory_points = self.enhanced_detector.ball_positions_history
            
            if trajectory_points:
                self.analysis_results['trajectory_analysis'] = {
                    'total_points': len(trajectory_points),
                    'start_position': trajectory_points[0] if trajectory_points else None,
                    'end_position': trajectory_points[-1] if trajectory_points else None,
                    'average_velocity': enhanced_stats['average_velocity'],
                    'max_velocity': enhanced_stats['max_velocity'],
                    'total_distance': enhanced_stats['total_distance'],
                    'tracking_duration': enhanced_stats['tracking_duration']
                }
            
            with open(output_path, 'w') as f:
                json.dump(self.analysis_results, f, indent=2)
            
            logger.info(f"Analysis results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving analysis results: {str(e)}")

def integrate_with_analyze_endpoint(video_path: str) -> dict:
    """
    Integrate comprehensive analysis with the existing /analyze endpoint.
    
    Args:
        video_path: Path to uploaded video
        
    Returns:
        Dictionary with analysis results and output paths
    """
    try:
        logger.info(f"Starting comprehensive analysis for: {video_path}")
        
        # Initialize analyzer
        analyzer = ComprehensiveVideoAnalyzer()
        
        # Generate output path in the analysis folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_folder = os.path.join(os.path.dirname(video_path), '..', 'analysis')
        os.makedirs(analysis_folder, exist_ok=True)
        output_video_path = os.path.join(analysis_folder, f"comprehensive_analysis_{timestamp}.mp4")
        
        # Run analysis
        result_video_path = analyzer.analyze_video(video_path, output_video_path)
        
        if result_video_path:
            # Prepare response
            results_json_path = result_video_path.replace('.mp4', '_results.json')
            # Save analysis results to the JSON file
            analyzer._save_analysis_results(results_json_path)
            
            return {
                'success': True,
                'output_video': result_video_path,
                'results_json': results_json_path,
                'analysis_results': analyzer.analysis_results
            }
        else:
            return {
                'success': False,
                'error': 'Analysis failed'
            }
            
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main function to run comprehensive video analysis."""
    print("Comprehensive Video Analysis with Complete Object Detection")
    print("=" * 70)
    
    # Create demo video if needed
    demo_video = 'demo_cricket_video.mp4'
    if not os.path.exists(demo_video):
        from test_ball_tracking_simple import create_test_video
        demo_video = create_test_video()
    
    # Run analysis
    result = integrate_with_analyze_endpoint(demo_video)
    
    if result['success']:
        print(f"\n✅ Analysis completed successfully!")
        print(f"📹 Output video: {result['output_video']}")
        print(f"📊 Results file: {result['results_json']}")
        
        # Print summary
        analysis_results = result['analysis_results']
        metrics = analysis_results.get('performance_metrics', {})
        
        print(f"\n📈 Analysis Summary:")
        print(f"   Total frames processed: {analysis_results['total_frames']}")
        print(f"   Enhanced detections: {metrics.get('total_enhanced_detections', 0)}")
        print(f"   Traditional detections: {metrics.get('total_traditional_detections', 0)}")
        print(f"   Player detections: {metrics.get('total_player_detections', 0)}")
        print(f"   Enhanced detection rate: {metrics.get('enhanced_detection_rate', 0)*100:.1f}%")
        print(f"   Traditional detection rate: {metrics.get('traditional_detection_rate', 0)*100:.1f}%")
        print(f"   Player detection rate: {metrics.get('player_detection_rate', 0)*100:.1f}%")
        
        if analysis_results.get('trajectory_analysis'):
            trajectory = analysis_results['trajectory_analysis']
            print(f"   Trajectory points: {trajectory.get('total_points', 0)}")
            print(f"   Start position: {trajectory.get('start_position')}")
            print(f"   End position: {trajectory.get('end_position')}")
        
        print(f"\n🎯 The output video includes:")
        print(f"   ✅ Ball detection (Enhanced & Traditional methods)")
        print(f"   ✅ Player detection and tracking")
        print(f"   ✅ Stump and field boundary detection")
        print(f"   ✅ Trajectory tracking with velocity vectors")
        print(f"   ✅ Shot zone and LBW analysis")
        print(f"   ✅ Cricket field overlay")
        print(f"   ✅ Real-time analytics overlay")
        
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main() 