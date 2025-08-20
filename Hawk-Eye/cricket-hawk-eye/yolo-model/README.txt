Your YOLO model package

Files:
- best.pt        -> trained weights (use this)
- data.yaml      -> class names (ball, bat, player)
- requirements.txt

Classes:
  0: ball
  1: bat
  2: player

Quick start (local/Cursor terminal):
------------------------------------
# 1) Python venv (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 2) Install Ultralytics + deps
pip install -r requirements.txt

# 3) Install PyTorch (pick ONE based on your machine):
# CPU only:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# OR NVIDIA GPU (CUDA 12.x example):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4) Quick test (Python):
from ultralytics import YOLO
m = YOLO("best.pt")
m.predict(source="path_or_folder_or_video.mp4", imgsz=1280, conf=0.25, save=True)

# 5) OR CLI:
yolo predict model=best.pt source=path/to/images_or_video imgsz=1280 conf=0.25 save=True

Tips:
- Ball chhota object hota hai; agar miss ho to conf=0.15 try karein.
- Outputs 'runs/predict/*' me save honge.
