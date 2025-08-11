#!/usr/bin/env python3
"""
Test script to verify server model loading
"""

import sys
import os
from pathlib import Path

# Add the server directory to path
sys.path.append('CricketAnalysisProject-master/YOLO Model/pages')

def test_model_loading():
    """Test if the server can load the trained model"""
    print("=== Testing Server Model Loading ===")
    
    try:
        # Import the server module
        from server import load_yolo_model
        
        print("✅ Server module imported successfully")
        
        # Test model loading
        print("\n🔍 Testing model loading...")
        model, success, model_info = load_yolo_model()
        
        if success:
            print(f"✅ Model loaded successfully!")
            print(f"   Model info: {model_info}")
            
            if model:
                print(f"   Model type: {type(model).__name__}")
                if hasattr(model, 'names'):
                    print(f"   Classes: {model.names}")
                if hasattr(model, 'device'):
                    print(f"   Device: {model.device}")
            
            return True
        else:
            print(f"❌ Model loading failed: {model_info}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_model_files():
    """Check if trained model files exist"""
    print("\n=== Checking Model Files ===")
    
    # Check various possible paths
    possible_paths = [
        'CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/results/best.pt',
        'CricketAnalysisProject-master/YOLO Model/Bat-Ball-Tracking-System-main/results/last.pt',
        'Bat-Ball-Tracking-System-main/results/best.pt',
        'Bat-Ball-Tracking-System-main/results/last.pt'
    ]
    
    found_models = []
    for path in possible_paths:
        if Path(path).exists():
            size_mb = Path(path).stat().st_size / (1024 * 1024)
            found_models.append((path, size_mb))
            print(f"✅ Found: {path} ({size_mb:.1f} MB)")
        else:
            print(f"❌ Not found: {path}")
    
    if found_models:
        print(f"\n🎯 Found {len(found_models)} trained model(s)")
        return True
    else:
        print("\n❌ No trained models found!")
        return False

def main():
    print("🚀 Testing Cricket Analysis Server Model Loading\n")
    
    # Check model files first
    models_exist = check_model_files()
    
    if not models_exist:
        print("\n❌ Cannot test model loading without model files")
        return
    
    # Test model loading
    print("\n" + "="*50)
    success = test_model_loading()
    
    if success:
        print("\n🎉 Everything is working! You can now run the server.")
        print("\n📝 To start the server:")
        print("   cd 'CricketAnalysisProject-master/YOLO Model/pages'")
        print("   python server.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("\n❌ Model loading failed. Check the errors above.")

if __name__ == "__main__":
    main()
