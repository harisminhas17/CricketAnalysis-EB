#!/usr/bin/env python
"""
Headless-safe YOLO video detector with reliable Windows/FFMPEG handling.
Usage:
  python detect_ball.py --video <path> --out <dir> [--model <best.pt>] [--conf 0.25] [--iou 0.7] [--device cpu] [--imgsz 640]
Prints one final JSON line on success/failure. Also prints progress heartbeats.
"""

import os, sys, time, json
from pathlib import Path

# ---- HEADLESS & WINDOWS SAFETY ----
os.environ.setdefault("PYTHONUNBUFFERED", "1")
os.environ.setdefault("OPENCV_VIDEOIO_PRIORITY_MSMF", "0")  # Prefer FFMPEG on Windows
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")       # OpenMP dup fix

try:
    # Python 3.7+ only
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

import argparse
import cv2
import numpy as np
import torch
from ultralytics import YOLO

torch.set_num_threads(1)   # Avoid CPU oversubscription stalls
cv2.setNumThreads(0)       # OpenCV thread control

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True, help="Path to input video")
    p.add_argument("--out", required=True, help="Output directory (will contain pred/...)")
    p.add_argument("--model", default=str(Path(__file__).parent / "best.pt"), help="Path to best.pt")
    p.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    p.add_argument("--iou", type=float, default=0.7, help="NMS IoU")
    p.add_argument("--device", default="cpu", help='"cpu" or GPU index like "0"')
    p.add_argument("--imgsz", type=int, default=640, help="Inference size")
    return p.parse_args()

def jprint(obj):
    # single-line JSON prints
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()

def open_video_ffmpeg(path: str):
    cap = cv2.VideoCapture(path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        cap.release()
        cap = cv2.VideoCapture(path)  # fallback

    ok, frame = False, None
    start = time.time()
    while time.time() - start < 3:
        ok, frame = cap.read()
        if ok and frame is not None:
            break
        time.sleep(0.05)

    if not ok:
        cap.release()
        jprint({"success": False, "error": "OpenCV could not read first frame (backend/codec)."})
        sys.exit(1)

    # reset to start
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return cap

def get_video_props(cap):
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps is None or fps <= 1 or fps > 240:
        fps = 25.0
    return w, h, float(fps)

def make_writer(out_dir: Path, fps: float, size):
    out_dir.mkdir(parents=True, exist_ok=True)
    pred_dir = out_dir / "pred"
    pred_dir.mkdir(parents=True, exist_ok=True)

    # Try MP4 first
    mp4_path = pred_dir / "annotated.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(mp4_path), fourcc, fps, size)
    if writer.isOpened():
        return writer, mp4_path

    # Fallback to AVI
    avi_path = pred_dir / "annotated.avi"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(str(avi_path), fourcc, fps, size)
    if writer.isOpened():
        return writer, avi_path

    return None, None

def draw_boxes(frame, results, names):
    # results: ultralytics Results
    boxes = getattr(results, "boxes", None)
    if boxes is None:
        return {}, frame

    counts = {}
    xyxy = boxes.xyxy.cpu().numpy() if hasattr(boxes, "xyxy") else []
    cls = boxes.cls.cpu().numpy().astype(int) if hasattr(boxes, "cls") else []
    conf = boxes.conf.cpu().numpy() if hasattr(boxes, "conf") else []

    for i in range(len(xyxy)):
        x1, y1, x2, y2 = xyxy[i].astype(int)
        c = int(cls[i]) if i < len(cls) else -1
        label = names.get(c, str(c))
        counts[label] = counts.get(label, 0) + 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        txt = f"{label} {conf[i]:.2f}" if i < len(conf) else label
        cv2.putText(frame, txt, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 240, 10), 1, cv2.LINE_AA)

    return counts, frame

def main():
    args = parse_args()
    video_path = str(Path(args.video))
    out_dir = Path(args.out)

    if not Path(video_path).exists():
        jprint({"success": False, "error": f"Video not found: {video_path}"})
        sys.exit(1)

    # Model
    model_path = str(Path(args.model))
    if not Path(model_path).exists():
        # Try default next to script
        fallback = Path(__file__).parent / "best.pt"
        if fallback.exists():
            model_path = str(fallback)
        else:
            jprint({"success": False, "error": f"Model file not found: {args.model}"})
            sys.exit(1)

    t0 = time.time()
    try:
        model = YOLO(model_path)
    except Exception as e:
        jprint({"success": False, "error": f"Failed to load model: {e}"})
        sys.exit(1)
    model_load_time = time.time() - t0

    cap = open_video_ffmpeg(video_path)
    w, h, fps = get_video_props(cap)
    if w <= 0 or h <= 0:
        jprint({"success": False, "error": "Invalid video dimensions."})
        sys.exit(1)

    writer, out_path = make_writer(out_dir, fps, (w, h))
    if writer is None:
        jprint({"success": False, "error": "Failed to open VideoWriter (codec)."})
        sys.exit(1)

    # Names
    names = getattr(model, "names", None)
    if names is None:
        names = {}
    # ensure dict[int->str]
    if isinstance(names, list):
        names = {i: n for i, n in enumerate(names)}

    total_counts = {}
    classes_seen = set()

    frame_idx = 0
    last_beat = time.time()

    infer_t = 0.0
    frames_done = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1

            t1 = time.time()
            res = model.predict(
                source=frame,
                conf=args.conf,
                iou=args.iou,
                imgsz=args.imgsz,
                device=args.device,
                verbose=False
            )[0]
            infer_t += (time.time() - t1)
            frames_done += 1

            counts, frame = draw_boxes(frame, res, names)
            for k, v in counts.items():
                total_counts[k] = total_counts.get(k, 0) + v
                classes_seen.add(k)

            writer.write(frame)

            if time.time() - last_beat > 2:
                jprint({"progress": "processing", "frame": frame_idx})
                last_beat = time.time()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        jprint({"success": False, "error": f"Runtime error: {e}"})
        try:
            writer.release()
        except Exception:
            pass
        cap.release()
        sys.exit(1)

    writer.release()
    cap.release()

    annotated_relpath = str(Path("pred") / Path(out_path).name)
    jprint({
        "success": True,
        "counts": total_counts,
        "classes": sorted(list(classes_seen)),
        "annotated_relpath": annotated_relpath,
        "model_load_time": round(model_load_time, 3),
        "inference_time": round(infer_t, 3),
        "video_processing_time": round(time.time() - t0, 3),
        "frames": frames_done,
        "fps": fps
    })

if __name__ == "__main__":
    main()
