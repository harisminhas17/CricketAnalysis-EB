from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import cv2
import torch
from pathlib import Path
# Force YOLOv5 for trained models
try:
    import yolov5
    YOLO_VERSION = "v5"
    print("✅ Using YOLOv5 library for trained models")
except ImportError:
    try:
        from ultralytics import YOLO
        YOLO_VERSION = "v8"
        print("⚠️  YOLOv5 not available, using YOLOv8")
    except ImportError:
        YOLO_VERSION = "none"
        print("❌ No YOLO library found")
import tempfile
import shutil
from datetime import datetime
import json

app = Flask(__name__, template_folder='.')
CORS(app)

# Global variables
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_yolo_model():
    """Load the Cricket-Specific YOLO model"""
    try:
        # Try to load your trained cricket models first
        trained_model_paths = [
            Path('../Bat-Ball-Tracking-System-main/results/best.pt'),  # Best trained model (from pages dir)
            Path('../Bat-Ball-Tracking-System-main/results/last.pt'),  # Last checkpoint (from pages dir)
            Path('Bat-Ball-Tracking-System-main/results/best.pt'),     # Alternative path
            Path('Bat-Ball-Tracking-System-main/results/last.pt')      # Alternative path
        ]
        
        for model_path in trained_model_paths:
            if model_path.exists():
                try:
                    if YOLO_VERSION == "v8":
                        model = YOLO(str(model_path))
                        print(f"✅ Loaded trained model with YOLOv8: {model_path}")
                    elif YOLO_VERSION == "v5":
                        # Load YOLOv5 model with proper error handling
                        try:
                            import yolov5
                            model = yolov5.load(str(model_path))
                            print(f"✅ Loaded trained model with YOLOv5: {model_path}")
                            print(f"   Model classes: {model.names if hasattr(model, 'names') else 'Unknown'}")
                        except Exception as e:
                            print(f"❌ YOLOv5 loading failed: {e}")
                            # Try alternative loading method with torch.hub
                            try:
                                import torch
                                torch.hub.set_dir('.')
                                model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), trust_repo=True, force_reload=True)
                                print(f"✅ Loaded trained model with torch.hub: {model_path}")
                                print(f"   Model classes: {model.names if hasattr(model, 'names') else 'Unknown'}")
                            except Exception as e2:
                                print(f"❌ Alternative loading also failed: {e2}")
                                continue
                    else:
                        print(f"❌ No compatible YOLO library found")
                        continue
                    
                    return model, True, f"Trained Cricket Model: {model_path.name}"
                except Exception as e:
                    print(f"❌ Error loading {model_path}: {e}")
                    continue
        
        # Try alternative cricket model paths (old structure)
        alternative_paths = [
            'Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/best.pt',
            'Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/last.pt',
            'Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/epoch_20.pt',
            '../Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/best.pt'
        ]
        
        for path in alternative_paths:
            if Path(path).exists():
                try:
                    if YOLO_VERSION == "v8":
                        model = YOLO(str(path))
                        print(f"✅ Loaded alternative model with YOLOv8: {path}")
                    elif YOLO_VERSION == "v5":
                        try:
                            import yolov5
                            model = yolov5.load(str(path))
                            print(f"✅ Loaded alternative model with YOLOv5: {path}")
                        except Exception as e:
                            print(f"❌ YOLOv5 alternative loading failed: {e}")
                            continue
                    else:
                        continue
                    
                    return model, True, "Cricket-Specific Trained Model (Alternative)"
                except Exception as e:
                    print(f"❌ Error loading alternative model {path}: {e}")
                    continue
        
        # Fallback to general model if cricket model not found
        general_model_path = Path('../../../yolo11n.pt')
        if general_model_path.exists():
            try:
                if YOLO_VERSION == "v8":
                    model = YOLO(str(general_model_path))
                    print(f"⚠️  Using fallback model with YOLOv8: {general_model_path}")
                    return model, True, "General YOLO11n Model (Fallback)"
                elif YOLO_VERSION == "v5":
                    print(f"⚠️  YOLOv5 fallback not available for general model")
                else:
                    print(f"⚠️  No compatible YOLO library for fallback")
            except Exception as e:
                print(f"❌ Error loading fallback model: {e}")
        
        print("❌ No YOLO models found")
        return None, False, "No YOLO model found"
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None, False, f"Error loading model: {str(e)}"

def analyze_video(video_path, confidence=0.5):
    """Analyze video with YOLO model"""
    model, success, model_info = load_yolo_model()
    
    if not success:
        return {"error": f"YOLO model not found or failed to load: {model_info}"}
    
    try:
        # Get video info
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        cap.release()
        
        # Create unique result folder with confidence level
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        confidence_str = f"conf_{confidence:.1f}".replace('.', '_')  # 0.5 -> conf_0_5
        result_folder = f"results/analysis_{confidence_str}_{timestamp}"
        os.makedirs(result_folder, exist_ok=True)
        
        # Also create confidence-specific uploads folder
        uploads_confidence_folder = f"uploads/confidence_{confidence_str}"
        os.makedirs(uploads_confidence_folder, exist_ok=True)
        
        print(f"🔍 Starting analysis with {model_info}")
        print(f" Video: {video_path}")
        print(f"⚙️ Confidence: {confidence}")
        print(f"📁 Results folder: {result_folder}")
        print(f" Uploads confidence folder: {uploads_confidence_folder}")
        
        # Run YOLO detection
        results = model(
            video_path,
            conf=confidence,
            save=True,
            project=result_folder,
            name='detection',
            verbose=False
        )
        
        # Analyze results
        ball_count = 0
        bat_count = 0
        other_count = 0
        total_frames_processed = 0
        
        for result in results:
            total_frames_processed += 1
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Check for cricket-related objects (cricket-specific model)
                    if hasattr(model, 'names') and model.names:
                        # General model classes
                        if cls == 32:  # sports ball
                            ball_count += 1
                        elif cls == 34:  # baseball bat
                            bat_count += 1
                        else:
                            other_count += 1
                    else:
                        # Cricket-specific model: 0=ball, 1=bat
                        if cls == 0:  # Ball
                            ball_count += 1
                        elif cls == 1:  # Bat
                            bat_count += 1
                        else:
                            other_count += 1
        
        # Find the processed video
        processed_video_path = f"{result_folder}/detection/detection.mp4"
        if not os.path.exists(processed_video_path):
            # Look for the video file
            detection_folder = f"{result_folder}/detection/"
            if os.path.exists(detection_folder):
                for file in os.listdir(detection_folder):
                    if file.endswith(('.mp4', '.avi')):
                        processed_video_path = f"{detection_folder}/{file}"
                        break
        
        print(f"✅ Analysis completed!")
        print(f"📊 Results: {ball_count} balls, {bat_count} bats, {other_count} other objects")
        
        return {
            "success": True,
            "model_info": model_info,
            "video_info": {
                "total_frames": total_frames,
                "fps": fps,
                "duration": duration,
                "confidence": confidence
            },
            "detection_results": {
                "frames_processed": total_frames_processed,
                "ball_detections": ball_count,
                "bat_detections": bat_count,
                "other_detections": other_count,
                "avg_balls_per_frame": ball_count/total_frames_processed if total_frames_processed > 0 else 0,
                "avg_bats_per_frame": bat_count/total_frames_processed if total_frames_processed > 0 else 0
            },
            "processed_video_path": processed_video_path,
            "result_folder": result_folder
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

@app.route('/')
def index():
    return render_template('video_upload.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file uploaded"})
    
    file = request.files['video']
    confidence = float(request.form.get('confidence', 0.5))
    
    if file.filename == '':
        return jsonify({"error": "No file selected"})
    
    if file and allowed_file(file.filename):
        # Save uploaded file in confidence-specific folder
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        confidence_str = f"conf_{confidence:.1f}".replace('.', '_')
        confidence_folder = f"uploads/confidence_{confidence_str}"
        os.makedirs(confidence_folder, exist_ok=True)
        
        filepath = os.path.join(confidence_folder, filename)
        file.save(filepath)
        
        print(f"📁 File uploaded: {filename}")
        print(f"📂 Saved to: {filepath}")
        print(f" Confidence folder: {confidence_folder}")
        
        # Analyze video
        result = analyze_video(filepath, confidence)
        
        return jsonify(result)
    
    return jsonify({"error": "Invalid file type. Supported: MP4, AVI, MOV, MKV"})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/results/<path:filename>')
def get_result(filename):
    return send_file(f"results/{filename}")

@app.route('/status')
def status():
    """Check if YOLO model is available"""
    model, success, model_info = load_yolo_model()
    
    # Get additional model information
    model_details = {}
    if success and model:
        try:
            model_details = {
                "model_type": type(model).__name__,
                "classes": model.names if hasattr(model, 'names') else "Unknown",
                "device": str(model.device) if hasattr(model, 'device') else "Unknown"
            }
        except Exception as e:
            model_details = {"error": str(e)}
    
    return jsonify({
        "model_available": success,
        "model_info": model_info,
        "model_details": model_details
    })

if __name__ == '__main__':
    print("🚀 Starting Cricket Video Analysis Server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🎯 Upload your cricket video and test YOLO detection!")
    
    # Check model status
    model, success, model_info = load_yolo_model()
    if success:
        print(f"✅ {model_info} loaded successfully!")
    else:
        print(f"❌ {model_info}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)