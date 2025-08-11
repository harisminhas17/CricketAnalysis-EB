# Cricket Ball & Bat Detection - YOLO 11 Model Usage Guide

## 🎯 **Quick Start for Users**

### **Prerequisites:**
```bash
pip install ultralytics flask flask-cors opencv-python numpy
```

### **1. Download the Model**
The trained model files are large and not in git. You need to:
- Download `best.pt` from the releases or contact the repository owner
- Place it in: `CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/best.pt`

### **2. Run the Backend**
```bash
cd CricketAnalysisProject-master
python app.py
```

### **3. Open the Frontend**
- Open `CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/frontend.html` in your browser
- Or serve it with: `python -m http.server 8000`

### **4. Use the System**
- Upload cricket videos
- Adjust confidence threshold (50% recommended)
- Process videos to detect balls and bats

## 🏗️ **For Developers - Complete Setup**

### **Model Training (if you want to retrain):**

1. **Prepare Dataset:**
   ```bash
   cd "CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main"
   python convert_csv_to_yolo.py
   ```

2. **Train the Model:**
   ```bash
   python train_yolo11.py
   ```

3. **Test the Model:**
   ```bash
   python test_yolo11.py
   ```

### **Model Performance:**
- **mAP50: 93.36%** - Excellent detection accuracy
- **Classes:** Ball (0), Bat (1)
- **Recommended Confidence:** 50%
- **Training Data:** 824 images with 1,859 annotations

## 📁 **File Structure:**
```
CricketAnalysisProject-master/
├── app.py                          # Flask backend
├── CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/
│   ├── frontend.html               # Web interface
│   ├── convert_csv_to_yolo.py     # Data conversion
│   ├── train_yolo11.py            # Training script
│   ├── test_yolo11.py             # Testing script
│   ├── data.yaml                   # Dataset config
│   └── runs/train/yolo11_ball_detect/weights/
│       └── best.pt                 # Trained model (5.2MB)
```

## ⚙️ **Configuration Options:**

### **Confidence Threshold:**
- **10-30%:** More detections, may include false positives
- **50%:** Balanced (recommended)
- **70-90%:** Fewer detections, more accurate

### **Detection Filtering:**
- **Ball size:** 50-2000 pixels²
- **Bat size:** 1000-50000 pixels²
- **Bat aspect ratio:** > 1.5 (longer than wide)

## 🚀 **API Usage:**

### **Backend Endpoint:**
```
POST /detect
Content-Type: multipart/form-data

Parameters:
- file: Video file (MP4/AVI)
- start: Start time in seconds (optional)
- end: End time in seconds (optional)
- confidence: Confidence threshold 0.1-0.9 (optional)

Response: Processed video with detection boxes
```

## 📊 **Model Details:**
- **Architecture:** YOLO 11 (custom)
- **Input Size:** 640x640
- **Classes:** 2 (ball, bat)
- **Training:** 50 epochs, 824 images
- **Accuracy:** 93.36% mAP50

## 🔧 **Troubleshooting:**

### **Model Not Found:**
```bash
# Check if model exists
ls "CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/runs/train/yolo11_ball_detect/weights/best.pt"
```

### **Dependencies Missing:**
```bash
pip install ultralytics flask flask-cors opencv-python numpy
```

### **Video Not Playing:**
- Check browser console for errors
- Ensure backend is running on port 5000
- Try different video formats (MP4 recommended)

## 📝 **Notes:**
- Model trained on cricket-specific dataset
- May not work well on other sports
- Confidence threshold affects detection quality
- Video trimming requires ffmpeg (not included)

## 🤝 **Support:**
For issues or questions, check the repository issues or contact the maintainer. 