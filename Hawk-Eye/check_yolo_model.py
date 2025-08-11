import os
from pathlib import Path
import torch

def check_yolo_model():
    """
    Check if YOLO model is ready for testing
    """
    print("=== YOLO Model Check ===")
    
    # Check if model file exists
    model_path = Path('yolo11n.pt')
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ YOLO model found: {model_path}")
        print(f"   Size: {size_mb:.1f} MB")
    else:
        print(f"❌ YOLO model not found: {model_path}")
        print("   Please make sure yolo11n.pt is in the current directory")
        return False
    
    # Check if ultralytics is installed
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics YOLO library available")
    except ImportError:
        print("❌ Ultralytics not installed")
        print("   Run: pip install ultralytics")
        return False
    
    # Check if torch is available
    try:
        print(f"✅ PyTorch available: {torch.__version__}")
    except:
        print("❌ PyTorch not available")
        return False
    
    # Try to load the model
    try:
        model = YOLO(str(model_path))
        print("✅ Model loaded successfully")
        
        # Get model info
        print(f"   Model type: {type(model).__name__}")
        print(f"   Classes: {model.names}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def test_simple_inference():
    """
    Test simple inference on a dummy image
    """
    print("\n=== Testing Simple Inference ===")
    
    try:
        from ultralytics import YOLO
        import numpy as np
        
        # Load model
        model = YOLO('yolo11n.pt')
        
        # Create a dummy image (black image)
        dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
        
        # Run inference
        results = model(dummy_image, conf=0.5)
        
        print("✅ Simple inference test passed")
        print(f"   Results type: {type(results)}")
        print(f"   Number of results: {len(results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple inference test failed: {e}")
        return False

def main():
    print("🔍 Checking YOLO model setup...\n")
    
    # Check model
    model_ready = check_yolo_model()
    
    if model_ready:
        print("\n✅ YOLO model is ready!")
        
        # Test inference
        inference_ready = test_simple_inference()
        
        if inference_ready:
            print("\n🎉 Everything is working! You can now test on cricket videos.")
            print("\n📝 Usage:")
            print("   python simple_yolo_test.py your_cricket_video.mp4")
            print("   python simple_yolo_test.py your_video.mp4 --confidence 0.7")
        else:
            print("\n❌ Model loaded but inference failed. Check dependencies.")
    else:
        print("\n❌ YOLO model is not ready. Please fix the issues above.")

if __name__ == "__main__":
    main()
