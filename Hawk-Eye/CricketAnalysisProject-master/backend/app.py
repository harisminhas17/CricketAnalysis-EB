# Monkey patch for Python 3.13 compatibility
import sys
if sys.version_info >= (3, 13):
    import ssl
    if not hasattr(ssl, 'wrap_socket'):
        ssl.wrap_socket = ssl.SSLContext.wrap_socket

# Monkey patch for imghdr module (removed in Python 3.13)
try:
    import imghdr
except ImportError:
    import types
    imghdr = types.ModuleType("imghdr")
    def what(file, h=None):
        if h is None:
            if isinstance(file, str):
                with open(file, 'rb') as f:
                    h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        if h.startswith(b'\xff\xd8'):
            return 'jpeg'
        if h.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
            return 'gif'
        if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
            return 'webp'
        return None
    imghdr.what = what
    sys.modules["imghdr"] = imghdr

import os
import cv2
import json
import logging
import traceback
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import config
from track_ball import track_ball_movement, classify_shot_zone, analyze_lbw_possibility
from ball_by_ball_analysis import analyze_ball_by_ball
from fitness_analysis import analyze_player_movement
from heatmap import create_shot_zone_heatmap, create_impact_zone_heatmap
from analyze_video import extract_frames, detect_objects_in_frames, analyze_video_real_time
from social_sharing import SocialSharing
from training_mode import TrainingMode
from match_mode import MatchMode
from data_export import DataExporter
from video_trimmer import VideoTrimmer
from multi_camera_tracker import MultiCameraTracker
from real_time_metrics import RealTimeMetrics
from performance_visualization import draw_performance_flags, create_performance_summary, create_flag_timeline
from historical_analysis import HistoricalAnalyzer
from historical_visualization import create_form_trajectory_plot, create_comparison_plot, create_zone_evolution_plot, create_performance_heatmap
from advanced_analytics import AdvancedAnalytics
from impact_zone_analytics import ImpactZoneAnalyzer
from real_time_feedback import RealTimeFeedback
from tagging import TaggingSystem
from notification_system import NotificationSystem
from user_panel import UserPanel
from feedback_dashboard import FeedbackDashboard
from data_export import DataExporter
from edge_detection import EdgeDetection
from frame_annotation import FrameAnnotator
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from multi_camera_tracker import MultiCameraTracker, CameraConfig
from flask_cors import CORS
from flask_socketio import SocketIO
from models import db, Video, GalleryItem
import json
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from typing import Dict, Any
import uuid
from training_mode import TrainingMode
from match_mode import MatchMode
import time
import base64
import threading
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from multi_camera_tracker import MultiCameraTracker, CameraConfig
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from analyze_video import extract_frames, detect_objects_in_frames
from track_ball import track_ball_movement
from heatmap import create_shot_zone_heatmap, create_impact_zone_heatmap
from fitness_analysis import (
    analyze_player_movement,
    FitnessMetrics,
    detect_player_position
)
from historical_analysis import HistoricalAnalyzer
from real_time_feedback import RealTimeFeedback
from social_sharing import SocialSharing
from data_export import DataExporter, ExportConfig
from frame_analysis import FrameAnalyzer
import tempfile
from tagging import TaggingSystem, Player, Event, Tag
from video_trimmer import VideoTrimmer
from social_api import social_bp
from hawkeye_visualization import analyze_delivery_with_hawkeye
from gallery import GalleryManager
from social_feed import SocialFeed
from comment_system import CommentSystem

# Correct imports for Hawkeye analysis
# from lbw_predictor import analyze_delivery_with_hawkeye  # old, remove or comment out

# Correct imports for frame analysis
from analyze_video import extract_frames, detect_objects_in_frames
# from frame_analysis import extract_frames, detect_objects_in_frames  # old, remove or comment out

# Add back the import for the newly created NotificationSystem module
from notification_system import NotificationSystem

# Add back the import for the newly created UserPanel module
from user_panel import UserPanel

# Utility to ensure absolute paths
def abs_path(path):
    """Convert relative paths to absolute paths based on config.BASE_DIR"""
    if os.path.isabs(path):
        return path
    return os.path.join(config.BASE_DIR, path)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a file handler for logging
log_file = os.path.join(config.BASE_DIR, 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(file_handler)

try:
    # Load environment variables
    logger.debug("Loading environment variables...")
    load_dotenv()

    app = Flask(__name__)

    # Configure Flask
    logger.debug("Configuring Flask...")
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config['BASE_DIR'] = config.BASE_DIR
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure CORS
    logger.debug("Configuring CORS...")
    CORS(app, resources={
        r"/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Initialize extensions
    logger.debug("Initializing database...")
    db.init_app(app)
    logger.debug("Initializing SocketIO...")
    socketio = SocketIO(app, cors_allowed_origins=config.CORS_ORIGINS)

    # Initialize YOLO model
    logger.debug("Loading YOLO model...")
    try:
        model = YOLO('yolov8n.pt')
        logger.debug("YOLO model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading YOLO model: {e}")
        model = None

    # Create upload folders
    logger.debug("Creating upload folders...")
    for folder in [config.UPLOAD_FOLDER, config.FRAMES_FOLDER, config.ANNOTATED_FOLDER, config.ANALYSIS_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        logger.debug(f"Created directory: {folder}")

    # Add a dedicated folder for social media uploads
    SOCIAL_UPLOADS_FOLDER = os.path.join(config.UPLOAD_FOLDER, 'social')
    os.makedirs(SOCIAL_UPLOADS_FOLDER, exist_ok=True)

    # Initialize managers
    logger.debug("Initializing managers...")
    training_mode = TrainingMode()
    match_mode = MatchMode()

    # Create database tables
    logger.debug("Creating database tables...")
    with app.app_context():
        db.create_all()

    frame_analyzer = FrameAnalyzer()

    tagging_system = TaggingSystem()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

    def normalize_file_path(file_path):
        """Normalize file path for web compatibility (replace backslashes with forward slashes)"""
        if file_path:
            return file_path.replace('\\', '/')
        return file_path

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        return send_from_directory(abs_path(config.UPLOAD_FOLDER), filename)

    @app.route('/analysis_files/<path:filename>')
    def serve_analysis_file(filename):
        """Serve files from the analysis output directory"""
        logger.info(f"Serving analysis file: {filename}")
        logger.info(f"Analysis folder: {abs_path(config.ANALYSIS_FOLDER)}")
        file_path = os.path.join(abs_path(config.ANALYSIS_FOLDER), filename)
        logger.info(f"Full file path: {file_path}")
        logger.info(f"File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            logger.info(f"File exists, serving: {file_path}")
            file_size = os.path.getsize(file_path)
            logger.info(f"File size: {file_size} bytes")
            
            # Set correct MIME type based on file extension
            if filename.lower().endswith('.mp4'):
                mimetype = 'video/mp4'
            elif filename.lower().endswith('.png'):
                mimetype = 'image/png'
            elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                mimetype = 'image/jpeg'
            elif filename.lower().endswith('.json'):
                mimetype = 'application/json'
            else:
                mimetype = None
            
            response = send_from_directory(
                abs_path(config.ANALYSIS_FOLDER), 
                filename, 
                as_attachment=False,
                mimetype=mimetype
            )
            
            # Add headers for video streaming
            if filename.lower().endswith('.mp4'):
                response.headers['Accept-Ranges'] = 'bytes'
                response.headers['Content-Length'] = str(file_size)
                response.headers['Cache-Control'] = 'public, max-age=3600'
            
            return response
        else:
            logger.error(f"File does not exist: {file_path}")
            return jsonify({'error': 'File not found'}), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'error': f'File too large. Maximum file size is {config.MAX_CONTENT_LENGTH / (1024*1024)}MB.'
        }), 413

    @app.route('/analyze', methods=['POST'])
    def analyze_video():
        try:
            logger.info("Received video upload request")
            analysis_type = request.form.get('analysis_type', 'all')

            # Check if video file is present
            if 'video' not in request.files:
                logger.error("No video file in request")
                return jsonify({'error': 'No video file provided'}), 400

            file = request.files['video']
            if file.filename == '':
                logger.error("Empty filename")
                return jsonify({'error': 'No selected file'}), 400

            if not allowed_file(file.filename):
                logger.error(f"Invalid file type: {file.filename}")
                return jsonify({'error': 'Invalid file type'}), 400

            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), f'{timestamp}_{filename}')
            file.save(video_path)
            logger.info(f"Video saved to: {video_path}")

            # Prepare output variables
            frames_dir = annotated_dir = None
            ball_positions = shot_zones = lbw_analysis = None
            shot_zone_heatmap_path = impact_zone_heatmap_path = None
            fitness_metrics = None
            ball_analysis = None
            hawkeye_video_filename = None
            hawkeye_json_path = None

            # Extract frames (needed for most analyses)
            if analysis_type in ['all', 'ball_tracking', 'shot_analysis', 'fitness_analysis', 'lbw_analysis', 'historical_analysis', 'performance_metrics']:
                frames_dir = os.path.join(abs_path(config.FRAMES_FOLDER), f'{timestamp}_{filename.rsplit('.', 1)[0]}')
                os.makedirs(frames_dir, exist_ok=True)
                logger.info(f"Created frames directory: {frames_dir}")
                try:
                    logger.info("Starting frame extraction")
                    extract_frames(video_path, frames_dir)
                    logger.info(f"Frames extracted to: {frames_dir}")
                except Exception as e:
                    logger.error(f"Error extracting frames: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return jsonify({'error': f'Failed to extract frames: {str(e)}'}), 500

            # Detect objects in frames (needed for ball tracking, shot, lbw, enhanced ball tracking)
            if analysis_type in ['all', 'ball_tracking', 'shot_analysis', 'lbw_analysis', 'enhanced_ball_tracking']:
                annotated_dir = os.path.join(abs_path(config.ANNOTATED_FOLDER), f'{timestamp}_{filename.rsplit('.', 1)[0]}')
                os.makedirs(annotated_dir, exist_ok=True)
                logger.info(f"Created annotated directory: {annotated_dir}")
                try:
                    logger.info("Starting object detection")
                    detect_objects_in_frames(frames_dir, annotated_dir)
                    logger.info(f"Objects detected and saved to: {annotated_dir}")
                except Exception as e:
                    logger.error(f"Error detecting objects: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    return jsonify({'error': f'Failed to detect objects: {str(e)}'}), 500

            # Enhanced ball tracking and LBW analysis
            if analysis_type in ['all', 'ball_tracking', 'lbw_analysis', 'enhanced_ball_tracking']:
                try:
                    logger.info("Starting comprehensive video analysis with all object detection")
                    
                    # Import the comprehensive analyzer
                    from comprehensive_video_analysis import integrate_with_analyze_endpoint
                    
                    # Run comprehensive analysis
                    comprehensive_result = integrate_with_analyze_endpoint(video_path)
                    
                    if comprehensive_result['success']:
                        # Extract results from comprehensive analysis
                        hawkeye_video_filename = os.path.basename(comprehensive_result['output_video'])
                        hawkeye_json_path = comprehensive_result['results_json']
                        
                        # Parse ball positions from comprehensive results
                        analysis_results = comprehensive_result['analysis_results']
                        ball_positions = analysis_results.get('trajectory_points', [])
                        
                        # Convert to expected format
                        if ball_positions:
                            ball_positions = [{'frame': pos['frame'], 'position': pos['position']} for pos in ball_positions]
                        
                        # Extract shot zones and LBW analysis
                        shot_zones = analysis_results.get('shot_analysis', [])
                        lbw_analysis = analysis_results.get('lbw_analysis', {})
                        
                        logger.info(f"Comprehensive analysis completed successfully")
                        logger.info(f"Output video: {comprehensive_result['output_video']}")
                        logger.info(f"Results JSON: {comprehensive_result['results_json']}")
                        
                    else:
                        logger.error(f"Comprehensive analysis failed: {comprehensive_result.get('error', 'Unknown error')}")
                        ball_positions = []
                        shot_zones = []
                        lbw_analysis = {}
                        hawkeye_video_filename = None
                        hawkeye_json_path = None
                    
                except Exception as e:
                    logger.error(f"Error in comprehensive video analysis: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    ball_positions = []
                    shot_zones = []
                    lbw_analysis = {}
                    hawkeye_video_filename = None
                    hawkeye_json_path = None

            # Heatmaps (shot analysis, historical)
            if analysis_type in ['all', 'shot_analysis', 'historical_analysis']:
                try:
                    logger.info("Creating heatmaps")
                    shot_zone_heatmap_path = os.path.join(abs_path(config.ANALYSIS_FOLDER), f'{timestamp}_shot_zone_heatmap.png')
                    impact_zone_heatmap_path = os.path.join(abs_path(config.ANALYSIS_FOLDER), f'{timestamp}_impact_zone_heatmap.png')
                    
                    if shot_zones and len(shot_zones) > 0:
                        create_shot_zone_heatmap(shot_zones, shot_zone_heatmap_path)
                    else:
                        shot_zone_heatmap_path = None
                        logger.warning("No shot zones available for heatmap creation")
                    
                    # Only create impact zone heatmap if we have ball positions
                    if ball_positions and len(ball_positions) > 0:
                        positions = []
                        for pos in ball_positions:
                            if isinstance(pos, dict) and 'position' in pos:
                                positions.append(pos['position'])
                            else:
                                positions.append(pos)
                        
                        if positions:
                            create_impact_zone_heatmap(positions, impact_zone_heatmap_path, trajectory=positions)
                        else:
                            impact_zone_heatmap_path = None
                    else:
                        impact_zone_heatmap_path = None
                        logger.warning("No ball positions available for impact zone heatmap creation")
                    
                    logger.info("Heatmaps created successfully")
                except Exception as e:
                    logger.error(f"Error creating heatmaps: {str(e)}")
                    shot_zone_heatmap_path = None
                    impact_zone_heatmap_path = None

            # Fitness analysis
            if analysis_type in ['all', 'fitness_analysis', 'performance_metrics']:
                try:
                    logger.info("Analyzing player movement")
                    # Get video FPS for fitness analysis
                    cap = cv2.VideoCapture(video_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    cap.release()
                    
                    # Get list of frame files
                    frame_files = [f for f in os.listdir(frames_dir) if f.endswith(('.jpg', '.png'))]
                    frame_files.sort()
                    
                    # Load frames for analysis
                    frames = []
                    for frame_file in frame_files[:100]:  # Limit to first 100 frames for performance
                        frame_path = os.path.join(frames_dir, frame_file)
                        frame = cv2.imread(frame_path)
                        if frame is not None:
                            frames.append(frame)
                    
                    if frames and fps:
                        fitness_metrics = analyze_player_movement(frames, fps)
                    else:
                        fitness_metrics = {}
                    logger.info("Player movement analysis completed")
                except Exception as e:
                    logger.error(f"Error analyzing player movement: {str(e)}")
                    fitness_metrics = {}

            # Ball-by-ball analysis (shot, historical)
            if analysis_type in ['all', 'shot_analysis', 'historical_analysis']:
                try:
                    logger.info("Starting ball-by-ball analysis")
                    # Convert ball_positions to the format expected by analyze_ball_by_ball
                    ball_positions_list = []
                    if ball_positions:
                        # Extract positions from ball_positions (which are dicts with 'position' key)
                        positions = []
                        for pos in ball_positions:
                            if isinstance(pos, dict) and 'position' in pos:
                                positions.append(pos['position'])
                            else:
                                positions.append(pos)
                        
                        # Pass as a single delivery (list of positions)
                        ball_positions_list = [positions] if positions else []
                    
                    ball_analysis = analyze_ball_by_ball(video_path, ball_positions_list)
                    logger.info("Ball-by-ball analysis completed")
                except Exception as e:
                    logger.error(f"Error in ball-by-ball analysis: {str(e)}")
                    ball_analysis = []

            # Prepare response based on requested analysis
            response_data = {'status': 'success'}
            if frames_dir:
                response_data['frames_dir'] = frames_dir
            if annotated_dir:
                response_data['annotated_dir'] = annotated_dir
            if analysis_type in ['all', 'ball_tracking', 'lbw_analysis', 'enhanced_ball_tracking']:
                response_data['ballPositions'] = ball_positions
                response_data['zones'] = shot_zones
                response_data['lbwAnalysis'] = lbw_analysis
                response_data['hawkeye_video'] = hawkeye_video_filename
                response_data['hawkeye_json'] = hawkeye_json_path
                logger.info(f"Response hawkeye_video field: {hawkeye_video_filename}")
                logger.info(f"Full response data keys: {list(response_data.keys())}")
            if analysis_type in ['all', 'shot_analysis', 'historical_analysis']:
                response_data['shot_zone_heatmap'] = shot_zone_heatmap_path
                response_data['impact_zone_heatmap'] = impact_zone_heatmap_path
                response_data['ballByBall'] = ball_analysis
            if analysis_type in ['all', 'fitness_analysis', 'performance_metrics']:
                response_data['fitness_metrics'] = fitness_metrics

            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_numpy_types(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy_types(item) for item in obj]
                return obj
            
            # Convert response data
            response_data = convert_numpy_types(response_data)
            
            logger.info("Analysis completed successfully")
            logger.info(f"Final response data: {response_data}")
            return jsonify(response_data)

        except Exception as e:
            logger.error(f"Unexpected error in analyze_video: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy"})

    @app.route('/api/training/start', methods=['POST'])
    def start_training():
        """Start a new training session"""
        try:
            data = request.json
            player_id = data.get('player_id')
            selected_drills = data.get('drills', [])
            
            session = training_mode.start_training_session(player_id, selected_drills)
            
            return jsonify({
                "status": "success",
                "session_id": session.id
            })
            
        except Exception as e:
            logger.error(f"Error starting training session: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/training/complete', methods=['POST'])
    def complete_training():
        """Complete a training session"""
        try:
            data = request.json
            session_id = data.get('session_id')
            drill_id = data.get('drill_id')
            feedback = data.get('feedback', {})
            metrics = data.get('metrics', {})
            
            training_mode.complete_drill(session_id, drill_id, feedback, metrics)
            
            return jsonify({"status": "success"})
            
        except Exception as e:
            logger.error(f"Error completing training session: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/match/start', methods=['POST'])
    def start_match():
        """Start a new match"""
        try:
            data = request.json
            team1_id = data.get('team1_id')
            team1_name = data.get('team1_name')
            team2_id = data.get('team2_id')
            team2_name = data.get('team2_name')
            players = data.get('players', {})
            
            match = match_mode.create_match(
                team1_id,
                team1_name,
                team2_id,
                team2_name,
                players
            )
            
            match = match_mode.start_match(match.id)
            
            return jsonify({
                "status": "success",
                "match_id": match.id
            })
            
        except Exception as e:
            logger.error(f"Error starting match: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/match/ball', methods=['POST'])
    def record_ball():
        """Record a ball in the current match"""
        try:
            data = request.json
            match_id = data.get('match_id')
            runs = data.get('runs', 0)
            extras = data.get('extras', 0)
            wicket = data.get('wicket', False)
            shot_type = data.get('shot_type')
            zone = data.get('zone')
            result = data.get('result')
            
            match = match_mode.record_ball(
                match_id,
                runs,
                extras,
                wicket,
                shot_type,
                zone,
                result
            )
            
            return jsonify({
                "status": "success",
                "match": match_mode.get_match_summary(match.id)
            })
            
        except Exception as e:
            logger.error(f"Error recording ball: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/match/end', methods=['POST'])
    def end_match():
        """End the current match"""
        try:
            data = request.json
            match_id = data.get('match_id')
            winner_id = data.get('winner_id')
            
            match = match_mode.end_match(match_id, winner_id)
            
            return jsonify({
                "status": "success",
                "match": match_mode.get_match_summary(match.id)
            })
            
        except Exception as e:
            logger.error(f"Error ending match: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/share', methods=['POST'])
    def share_content():
        """Share content to social media"""
        try:
            data = request.json
            content_id = data.get('content_id')
            platform = data.get('platform')
            
            if platform == 'twitter':
                api_key = data.get('api_key')
                api_secret = data.get('api_secret')
                access_token = data.get('access_token')
                access_token_secret = data.get('access_token_secret')
                
                share_url = SocialSharing().share_to_twitter(
                    content_id,
                    api_key,
                    api_secret,
                    access_token,
                    access_token_secret
                )
            elif platform == 'facebook':
                access_token = data.get('access_token')
                page_id = data.get('page_id')
                
                share_url = SocialSharing().share_to_facebook(
                    content_id,
                    access_token,
                    page_id
                )
            else:
                raise ValueError(f"Unsupported platform: {platform}")
            
            return jsonify({
                "status": "success",
                "share_url": share_url
            })
            
        except Exception as e:
            logger.error(f"Error sharing content: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/export', methods=['POST'])
    def export_data():
        """Export data in specified format"""
        try:
            data = request.json
            export_data = data.get('data')
            format = data.get('format', 'json')
            include_metrics = data.get('include_metrics', True)
            include_media = data.get('include_media', True)
            include_timestamps = data.get('include_timestamps', True)
            compression = data.get('compression', False)
            
            config = ExportConfig(
                format=format,
                include_metrics=include_metrics,
                include_media=include_media,
                include_timestamps=include_timestamps,
                compression=compression
            )
            
            export_path = DataExporter().export_analysis_data(
                export_data,
                config
            )
            
            return send_file(
                export_path,
                as_attachment=True,
                download_name=os.path.basename(export_path)
            )
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/analyze', methods=['POST'])
    def api_analyze_video():
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({'error': 'No video file selected'}), 400
        
        # Save the video file
        video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), secure_filename(video_file.filename))
        video_file.save(video_path)
        
        try:
            # Get ball positions from the request
            ball_positions = request.json.get('ball_positions', [])
            
            # Perform ball-by-ball analysis
            ball_analysis = analyze_ball_by_ball(video_path, ball_positions)
            
            # Prepare the analysis response
            analysis_response = {
                'ballByBall': ball_analysis,
                'status': 'success',
                'message': 'Analysis completed successfully'
            }
            
            return jsonify(analysis_response)
        
        except Exception as e:
            app.logger.error(f"Error during analysis: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/extract-frames', methods=['POST'])
    def extract_frames_endpoint():
        try:
            data = request.json
            video_url = data.get('videoUrl')
            
            if not video_url:
                return jsonify({'error': 'Video URL is required'}), 400

            # Extract frames from video
            frames_data = frame_analyzer.extract_frames(video_url)
            return jsonify(frames_data)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/frame-metadata/<int:frame_index>', methods=['GET'])
    def get_frame_metadata(frame_index):
        try:
            metadata = frame_analyzer.get_frame_metadata(frame_index)
            return jsonify(metadata)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/save-annotation', methods=['POST'])
    def save_annotation():
        try:
            data = request.json
            frame_index = data.get('frameIndex')
            annotation = data.get('annotation')

            if not frame_index or not annotation:
                return jsonify({'error': 'Frame index and annotation are required'}), 400

            success = frame_analyzer.save_annotation(frame_index, annotation)
            if success:
                return jsonify(frame_analyzer.get_annotations(frame_index))
            else:
                return jsonify({'error': 'Failed to save annotation'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/export-frame/<int:frame_index>', methods=['POST'])
    def export_frame(frame_index):
        try:
            # Create temporary file for the exported frame
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                success = frame_analyzer.export_annotated_frame(frame_index, temp_file.name)
                
                if success:
                    return send_file(
                        temp_file.name,
                        mimetype='image/jpeg',
                        as_attachment=True,
                        download_name=f'frame_{frame_index}.jpg'
                    )
                else:
                    return jsonify({'error': 'Failed to export frame'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/delete-annotation', methods=['POST'])
    def delete_annotation():
        try:
            data = request.json
            frame_index = data.get('frameIndex')
            annotation_id = data.get('annotationId')

            if not frame_index or annotation_id is None:
                return jsonify({'error': 'Frame index and annotation ID are required'}), 400

            success = frame_analyzer.delete_annotation(frame_index, annotation_id)
            if success:
                return jsonify(frame_analyzer.get_annotations(frame_index))
            else:
                return jsonify({'error': 'Failed to delete annotation'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/update-annotation', methods=['POST'])
    def update_annotation():
        try:
            data = request.json
            frame_index = data.get('frameIndex')
            annotation_id = data.get('annotationId')
            new_data = data.get('newData')

            if not all([frame_index, annotation_id, new_data]):
                return jsonify({'error': 'Frame index, annotation ID, and new data are required'}), 400

            success = frame_analyzer.update_annotation(frame_index, annotation_id, new_data)
            if success:
                return jsonify(frame_analyzer.get_annotations(frame_index))
            else:
                return jsonify({'error': 'Failed to update annotation'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/gallery/<user_id>', methods=['GET'])
    def get_gallery_items(user_id):
        try:
            item_type = request.args.get('type', 'all')
            tags = request.args.get('tags', '').split(',') if request.args.get('tags') else None
            
            items = SocialSharing().get_gallery_items(user_id, item_type, tags)
            return jsonify([{
                'id': item.id,
                'type': item.type,
                'title': item.title,
                'description': item.description,
                'file_path': normalize_file_path(item.file_path),
                'thumbnail_path': normalize_file_path(item.thumbnail_path),
                'created_at': item.created_at.isoformat(),
                'tags': item.tags,
                'metadata': item.metadata
            } for item in items])
        except Exception as e:
            logger.error(f"Error getting gallery items: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/share/<item_id>', methods=['POST'])
    def share_item(item_id):
        try:
            data = request.json
            platform = data.get('platform')
            title = data.get('title')
            description = data.get('description')
            tags = data.get('tags', [])
            
            # Get the item from gallery
            items = SocialSharing().get_gallery_items(data.get('user_id'))
            item = next((i for i in items if i.id == item_id), None)
            
            if not item:
                return jsonify({'error': 'Item not found'}), 404
            
            # Share based on platform
            if platform == 'twitter':
                SocialSharing().share_to_twitter(item, description)
            elif platform == 'instagram':
                SocialSharing().share_to_instagram(item, description)
            elif platform == 'youtube':
                SocialSharing().share_to_youtube(item, title, description, tags)
            else:
                return jsonify({'error': 'Invalid platform'}), 400
            
            return jsonify({'message': f'Successfully shared to {platform}'})
        except Exception as e:
            logger.error(f"Error sharing item: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/gallery/upload', methods=['POST'])
    def upload_to_gallery():
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            user_id = request.form.get('user_id')
            item_type = request.form.get('type')
            title = request.form.get('title')
            description = request.form.get('description')
            tags = request.form.get('tags', '').split(',')
            metadata = json.loads(request.form.get('metadata', '{}'))
            
            if not all([user_id, item_type, title, description]):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Save file temporarily
            temp_path = os.path.join('temp', file.filename)
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)
            
            # Save to gallery
            item = SocialSharing().save_to_gallery(
                user_id=user_id,
                item_type=item_type,
                file_path=temp_path,
                title=title,
                description=description,
                tags=tags,
                metadata=metadata
            )
            
            # Clean up temp file
            os.remove(temp_path)
            
            return jsonify({
                'id': item.id,
                'type': item.type,
                'title': item.title,
                'description': item.description,
                'file_path': normalize_file_path(item.file_path),
                'thumbnail_path': normalize_file_path(item.thumbnail_path),
                'created_at': item.created_at.isoformat(),
                'tags': item.tags,
                'metadata': item.metadata
            })
        except Exception as e:
            logger.error(f"Error uploading to gallery: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/players', methods=['GET'])
    def get_players():
        team = request.args.get('team')
        if team:
            players = tagging_system.get_players_by_team(team)
        else:
            players = list(tagging_system.players.values())
        return jsonify([vars(p) for p in players])

    @app.route('/api/players', methods=['POST'])
    def add_player():
        data = request.json
        player = Player(**data)
        pid = tagging_system.add_player(player)
        return jsonify({'id': pid}), 201

    @app.route('/api/events', methods=['GET'])
    def get_events():
        event_type = request.args.get('type')
        if event_type:
            events = tagging_system.get_events_by_type(event_type)
        else:
            events = list(tagging_system.events.values())
        return jsonify([vars(e) for e in events])

    @app.route('/api/events', methods=['POST'])
    def add_event():
        data = request.json
        event = Event(**data)
        eid = tagging_system.add_event(event)
        return jsonify({'id': eid}), 201

    @app.route('/api/tags/<video_id>', methods=['GET'])
    def get_tags(video_id):
        player_id = request.args.get('player_id')
        event_id = request.args.get('event_id')
        if player_id:
            tags = tagging_system.get_tags_by_player(video_id, player_id)
        elif event_id:
            tags = tagging_system.get_tags_by_event(video_id, event_id)
        else:
            tags = tagging_system.get_tags(video_id)
        return jsonify([vars(t) for t in tags])

    @app.route('/api/tags/<video_id>', methods=['POST'])
    def add_tag(video_id):
        data = request.json
        tag = Tag(
            id=data.get('id', ''),
            video_id=video_id,
            timestamp=data['timestamp'],
            position=data['position'],
            player_id=data.get('player_id'),
            event_id=data.get('event_id'),
            text=data.get('text'),
            metadata=data.get('metadata', {}),
            created_at=datetime.now()
        )
        tid = tagging_system.add_tag(video_id, tag)
        return jsonify({'id': tid}), 201

    @app.route('/api/tags/<video_id>/<tag_id>', methods=['PUT'])
    def update_tag(video_id, tag_id):
        updates = request.json
        success = tagging_system.update_tag(video_id, tag_id, updates)
        return jsonify({'success': success})

    @app.route('/api/tags/<video_id>/<tag_id>', methods=['DELETE'])
    def delete_tag(video_id, tag_id):
        success = tagging_system.delete_tag(video_id, tag_id)
        return jsonify({'success': success})

    @app.route('/api/tags-for-sharing/<video_id>', methods=['GET'])
    def get_tags_for_sharing(video_id):
        player_ids = request.args.getlist('player_id')
        event_types = request.args.getlist('event_type')
        start_time = request.args.get('start_time', type=float)
        end_time = request.args.get('end_time', type=float)
        time_range = (start_time, end_time) if start_time is not None and end_time is not None else None
        tags = tagging_system.get_tags_for_sharing(
            video_id,
            player_ids=player_ids if player_ids else None,
            event_types=event_types if event_types else None,
            time_range=time_range
        )
        return jsonify([vars(t) for t in tags])

    @app.route('/api/trim-video', methods=['POST'])
    def trim_video():
        """Trim a video file and return the trimmed video"""
        try:
            # Check if video file is present
            if 'video' not in request.files:
                return jsonify({'error': 'No video file provided'}), 400
            
            file = request.files['video']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Get trim parameters
            start_time = float(request.form.get('start_time', 0))
            end_time = float(request.form.get('end_time', 0))
            
            if start_time < 0 or end_time <= start_time:
                return jsonify({'error': 'Invalid time range'}), 400
            
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), f'temp_{timestamp}_{filename}')
            file.save(temp_video_path)
            
            try:
                # Trim the video
                trimmer = VideoTrimmer()
                trimmed_video_path = trimmer.trim_video(
                    temp_video_path, 
                    start_time, 
                    end_time
                )
                
                # Read the trimmed video file
                with open(trimmed_video_path, 'rb') as f:
                    video_data = f.read()
                
                # Clean up temporary files
                os.remove(temp_video_path)
                os.remove(trimmed_video_path)
                
                # Return the trimmed video as a file download
                from io import BytesIO
                trimmed_filename = f'trimmed_{filename}'
                
                return send_file(
                    BytesIO(video_data),
                    mimetype='video/mp4',
                    as_attachment=True,
                    download_name=trimmed_filename
                )
                
            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                raise e
                
        except Exception as e:
            logger.error(f"Error trimming video: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/video-info', methods=['POST'])
    def get_video_info():
        """Get video information including duration, fps, dimensions"""
        try:
            if 'video' not in request.files:
                return jsonify({'error': 'No video file provided'}), 400
            
            file = request.files['video']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), f'temp_{timestamp}_{filename}')
            file.save(temp_video_path)
            
            try:
                # Get video info
                trimmer = VideoTrimmer()
                video_info = trimmer.get_video_info(temp_video_path)
                
                # Clean up temp file
                os.remove(temp_video_path)
                
                return jsonify({
                    'status': 'success',
                    'video_info': video_info
                })
                
            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(temp_video_path):
                    os.remove(temp_video_path)
                raise e
                
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/upload', methods=['POST'])
    def upload_media():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            # Generate a unique filename to prevent overwrites
            filename = secure_filename(file.filename)
            unique_id = uuid.uuid4().hex
            unique_filename = f"{unique_id}_{filename}"
            
            # Save the file to the social uploads folder
            save_path = os.path.join(SOCIAL_UPLOADS_FOLDER, unique_filename)
            file.save(save_path)

            # Construct the public URL for the file
            # The path needs to be relative to the 'uploads' folder for the existing endpoint
            relative_path = os.path.join('social', unique_filename).replace('\\', '/')
            file_url = f"/uploads/{relative_path}"

            return jsonify({'url': file_url}), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400

    @app.route('/api/enhanced-ball-tracking', methods=['POST'])
    def enhanced_ball_tracking():
        """Enhanced ball tracking endpoint using the improved detection system."""
        try:
            logger.info("Received enhanced ball tracking request")
            
            # Check if video file is present
            if 'video' not in request.files:
                logger.error("No video file in request")
                return jsonify({'error': 'No video file provided'}), 400

            file = request.files['video']
            if file.filename == '':
                logger.error("Empty filename")
                return jsonify({'error': 'No selected file'}), 400

            if not allowed_file(file.filename):
                logger.error(f"Invalid file type: {file.filename}")
                return jsonify({'error': 'Invalid file type'}), 400

            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), f'{timestamp}_{filename}')
            file.save(video_path)
            logger.info(f"Video saved to: {video_path}")

            # Extract frames for ball tracking
            frames_dir = os.path.join(abs_path(config.FRAMES_FOLDER), f'{timestamp}_{filename.rsplit('.', 1)[0]}')
            os.makedirs(frames_dir, exist_ok=True)
            
            try:
                logger.info("Starting frame extraction for enhanced ball tracking")
                extract_frames(video_path, frames_dir)
                logger.info(f"Frames extracted to: {frames_dir}")
            except Exception as e:
                logger.error(f"Error extracting frames: {str(e)}")
                return jsonify({'error': f'Failed to extract frames: {str(e)}'}), 500

            # Create annotated frames for enhanced ball tracking
            annotated_dir = os.path.join(abs_path(config.ANNOTATED_FOLDER), f'{timestamp}_{filename.rsplit('.', 1)[0]}')
            os.makedirs(annotated_dir, exist_ok=True)
            
            try:
                logger.info("Starting object detection for enhanced ball tracking")
                detect_objects_in_frames(frames_dir, annotated_dir)
                logger.info(f"Objects detected and saved to: {annotated_dir}")
            except Exception as e:
                logger.error(f"Error detecting objects: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return jsonify({'error': f'Failed to detect objects: {str(e)}'}), 500

            # Create output directory for ball tracking analysis
            ball_tracking_output_dir = os.path.join(abs_path(config.ANALYSIS_FOLDER), f'{timestamp}_enhanced_ball_tracking')
            os.makedirs(ball_tracking_output_dir, exist_ok=True)

            # Use the enhanced ball tracking system
            from track_ball import track_ball_movement, analyze_lbw_possibility
            
            # Track ball movement using enhanced detection
            ball_positions, shot_zones, lbw_analysis = track_ball_movement(
                frames_dir, 
                os.path.join(ball_tracking_output_dir, 'enhanced_ball_tracking_results.json')
            )

            # Create ball tracking visualization video
            hawkeye_video_filename = None
            try:
                import cv2
                
                # Read the original video
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Create output video writer
                output_video_path = os.path.join(ball_tracking_output_dir, 'enhanced_ball_tracking_video.mp4')
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
                
                frame_count = 0
                ball_positions_dict = {pos['frame']: pos['position'] for pos in ball_positions}
                
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Draw ball position if detected in this frame
                    if frame_count in ball_positions_dict:
                        ball_pos = ball_positions_dict[frame_count]
                        cv2.circle(frame, tuple(map(int, ball_pos)), 15, (0, 0, 255), 3)
                        cv2.putText(frame, f'Ball: ({ball_pos[0]}, {ball_pos[1]})', 
                                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Add frame number and tracking info
                    cv2.putText(frame, f'Frame: {frame_count}', (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(frame, f'Enhanced Tracking', (10, 90), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    out.write(frame)
                    frame_count += 1
                
                cap.release()
                out.release()
                
                hawkeye_video_filename = os.path.basename(output_video_path)
                logger.info(f"Enhanced ball tracking video created: {output_video_path}")
                
            except Exception as e:
                logger.error(f"Error creating enhanced ball tracking video: {str(e)}")
                hawkeye_video_filename = None

            # Prepare response
            response_data = {
                'status': 'success',
                'message': 'Enhanced ball tracking completed successfully',
                'ball_positions': ball_positions,
                'shot_zones': shot_zones,
                'lbw_analysis': lbw_analysis,
                'total_detections': len(ball_positions),
                'video_filename': hawkeye_video_filename,
                'analysis_timestamp': timestamp,
                'annotated_frames_dir': os.path.basename(annotated_dir),
                'frames_dir': os.path.basename(frames_dir)
            }

            logger.info(f"Enhanced ball tracking completed. Found {len(ball_positions)} ball positions.")
            return jsonify(response_data)

        except Exception as e:
            logger.error(f"Error in enhanced ball tracking: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Enhanced ball tracking failed: {str(e)}'}), 500

    @app.route('/api/analyze-real-time', methods=['POST'])
    def analyze_video_real_time_endpoint():
        """Real-time video analysis with immediate ball tracking."""
        try:
            logger.info("Received real-time video analysis request")
            
            # Check if video file is present
            if 'video' not in request.files:
                return jsonify({'error': 'No video file provided'}), 400

            file = request.files['video']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400

            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400

            # Save uploaded file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_path = os.path.join(abs_path(config.UPLOAD_FOLDER), f'{timestamp}_{filename}')
            file.save(video_path)
            logger.info(f"Video saved to: {video_path}")

            # Create output directory for real-time analysis
            real_time_output_dir = os.path.join(abs_path(config.ANALYSIS_FOLDER), f'{timestamp}_real_time')
            
            # Run real-time analysis
            real_time_results = analyze_video_real_time(video_path, real_time_output_dir)
            
            # Prepare response
            response_data = {
                'status': 'success',
                'message': 'Real-time analysis completed successfully',
                'video_path': video_path,
                'output_video': real_time_results.get('output_video'),
                'trajectory_data': real_time_results.get('trajectory_data'),
                'total_frames_processed': real_time_results.get('total_frames_processed'),
                'frames_with_ball': real_time_results.get('frames_with_ball'),
                'tracking_efficiency': real_time_results.get('tracking_efficiency'),
                'ball_positions': real_time_results.get('ball_positions'),
                'timestamps': real_time_results.get('timestamps')
            }
            
            logger.info(f"Real-time analysis completed. Trajectory points: {len(real_time_results.get('ball_positions', []))}")
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Error in real-time video analysis: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Real-time analysis failed: {str(e)}'}), 500

    def analyze_lbw_with_yolo(video_path: str, output_dir: str) -> Dict[str, Any]:
        """
        Advanced LBW analysis using trained YOLO model and LBW predictor.
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save output files
            
        Returns:
            Dictionary containing LBW analysis results
        """
        try:
            from ultralytics import YOLO
            from lbw_predictor import LBWPredictor
            import cv2
            import os
            
            # Check if YOLO model exists
            model_path = 'runs/cricket_ball_train5/weights/best.pt'
            if not os.path.exists(model_path):
                logger.warning(f"YOLO model not found at {model_path}, using basic LBW analysis")
                return {"error": "YOLO model not found", "lbw_analysis": {}}
            
            # Load trained YOLO model
            model = YOLO(model_path)
            logger.info("YOLO model loaded successfully")
            
            # Initialize video capture
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Initialize LBW predictor
            predictor = LBWPredictor()
            
            # Prepare output video
            output_path = os.path.join(output_dir, 'lbw_analysis_output.mp4')
            os.makedirs(output_dir, exist_ok=True)
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            
            frame_idx = 0
            lbw_results = []
            ball_detections = []
            
            logger.info("Starting advanced LBW analysis...")
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Run YOLO inference on the frame
                results = model(frame)
                boxes = results[0].boxes.xyxy.cpu().numpy()
                confidences = results[0].boxes.conf.cpu().numpy()
                
                frame_analysis = {
                    'frame': frame_idx,
                    'detections': [],
                    'lbw_decision': None
                }
                
                for box, conf in zip(boxes, confidences):
                    if conf < 0.5:  # Confidence threshold
                        continue
                    
                    x1, y1, x2, y2 = box.astype(int)
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    
                    # Store ball detection
                    ball_detections.append({
                        'frame': frame_idx,
                        'position': (cx, cy),
                        'confidence': float(conf),
                        'bbox': [x1, y1, x2, y2]
                    })
                    
                    # Add ball state to predictor (simulated 3D coordinates)
                    predictor.add_ball_state(
                        position=(0.0, 0.6, 0.0),  # Approx starting position in meters
                        velocity=(0.0, -15.0, 0.0),  # Falling towards batsman
                        timestamp=frame_idx / fps
                    )
                    
                    # Analyze LBW
                    result = predictor.analyze_lbw(
                        pad_impact_position=(0.0, 0.3, 0.0),
                        pitch_location="middle"
                    )
                    
                    frame_analysis['detections'].append({
                        'position': (cx, cy),
                        'confidence': float(conf),
                        'bbox': [x1, y1, x2, y2],
                        'lbw_result': result
                    })
                    
                    # Draw bounding box and center
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"Conf: {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Display LBW result
                    if result and 'lbw' in result:
                        label = f"LBW: {'Yes' if result['lbw'] else 'No'} ({result.get('confidence', 0):.1f}%)"
                        cv2.putText(frame, label, (x1, y2 + 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        
                        frame_analysis['lbw_decision'] = result
                
                lbw_results.append(frame_analysis)
                out.write(frame)
                frame_idx += 1
            
            # Cleanup
            cap.release()
            out.release()
            
            # Calculate overall LBW statistics
            total_detections = len(ball_detections)
            lbw_decisions = [r['lbw_decision'] for r in lbw_results if r['lbw_decision']]
            
            if lbw_decisions:
                lbw_count = sum(1 for d in lbw_decisions if d.get('lbw', False))
                lbw_percentage = (lbw_count / len(lbw_decisions)) * 100
                avg_confidence = sum(d.get('confidence', 0) for d in lbw_decisions) / len(lbw_decisions)
            else:
                lbw_count = 0
                lbw_percentage = 0
                avg_confidence = 0
            
            analysis_result = {
                'total_frames': frame_idx,
                'ball_detections': ball_detections,
                'lbw_results': lbw_results,
                'lbw_statistics': {
                    'total_detections': total_detections,
                    'lbw_decisions': len(lbw_decisions),
                    'lbw_count': lbw_count,
                    'lbw_percentage': lbw_percentage,
                    'average_confidence': avg_confidence
                },
                'output_video': output_path,
                'status': 'success'
            }
            
            logger.info(f"Advanced LBW analysis completed. Found {total_detections} ball detections, {lbw_count} LBW decisions")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in advanced LBW analysis: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    # Register blueprints
    app.register_blueprint(social_bp, url_prefix='/api/social')

    if __name__ == '__main__':
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)

except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise
