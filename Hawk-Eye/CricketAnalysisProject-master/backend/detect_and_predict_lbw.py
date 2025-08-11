import cv2
import os
import numpy as np
from ultralytics import YOLO
from lbw_predictor import LBWPredictor
import glob

def analyze_lbw_video(video_path, output_dir=None):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found at: {video_path}")

    model_path = 'runs/cricket_ball_train5/weights/best.pt'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"YOLO model not found at: {model_path}")

    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    predictor = LBWPredictor()
    output_path = None

    if output_dir:
        output_path = os.path.join(output_dir, 'lbw_analysis_output.mp4')
        os.makedirs(output_dir, exist_ok=True)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    else:
        out = None

    frame_idx = 0
    ball_detections = []
    ball_trajectory = []
    last_ball_position = None
    BALL_CLASS_ID = 1  # adjust based on your dataset
    MIN_BALL_SIZE = 3
    MAX_BALL_SIZE = 60

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.2)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        confidences = results[0].boxes.conf.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy() if hasattr(results[0].boxes, 'cls') else None

        current_ball_position = None
        best_conf = 0

        for i, (box, conf) in enumerate(zip(boxes, confidences)):
            if conf < 0.2:
                continue
            if class_ids is not None and class_ids[i] != BALL_CLASS_ID:
                continue

            x1, y1, x2, y2 = box.astype(int)
            w, h = x2 - x1, y2 - y1
            aspect_ratio = w / h if h != 0 else 0
            if not (MIN_BALL_SIZE <= w <= MAX_BALL_SIZE and 0.5 <= aspect_ratio <= 1.5):
                continue

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if conf > best_conf:
                best_conf = conf
                current_ball_position = (cx, cy)

            ball_detections.append({
                'frame': frame_idx,
                'position': (cx, cy),
                'confidence': float(conf),
                'bbox': [x1, y1, x2, y2]
            })

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"Ball {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        if current_ball_position:
            ball_trajectory.append(current_ball_position)
            last_ball_position = current_ball_position
        elif last_ball_position:
            ball_trajectory.append(last_ball_position)

        if len(ball_trajectory) > 30:
            ball_trajectory = ball_trajectory[-30:]

        for i in range(1, len(ball_trajectory)):
            pt1 = ball_trajectory[i - 1]
            pt2 = ball_trajectory[i]
            cv2.line(frame, pt1, pt2, (255, 255, 255), 2)

        if current_ball_position:
            x, y = current_ball_position
            cv2.circle(frame, (x, y), 12, (255, 255, 255), -1)
            cv2.circle(frame, (x, y), 12, (0, 0, 255), 2)

        if out:
            out.write(frame)

        frame_idx += 1

    cap.release()
    if out:
        out.release()

    return {
        'total_frames': frame_idx,
        'ball_detections': ball_detections,
        'output_video': output_path,
        'status': 'success'
    }

if __name__ == "__main__":
    video_path = 'uploads/video.mp4'
    if not os.path.exists(video_path):
        video_files = glob.glob('uploads/*.mp4')
        if not video_files:
            raise FileNotFoundError("No video found.")
        video_path = video_files[0]

    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)

    result = analyze_lbw_video(video_path, output_dir)
    print(f"✅ Done. Output video: {result['output_video']}")
