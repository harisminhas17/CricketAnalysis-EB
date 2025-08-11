import os
import sys
import pkg_resources
import subprocess
import platform
import cv2
import numpy as np
from dotenv import load_dotenv

# Optional imports - these are not required for basic functionality
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

def check_python_version():
    required_version = (3, 7)
    current_version = sys.version_info
    if current_version < required_version:
        print(f"❌ Python version {required_version[0]}.{required_version[1]} or higher is required")
        return False
    print(f"✅ Python version {current_version[0]}.{current_version[1]}.{current_version[2]}")
    return True

def check_pip_packages():
    # Core required packages for the project
    required_packages = {
        'flask': '2.0.1',
        'flask-cors': '3.0.10',
        'flask-socketio': '5.1.1',
        'opencv-python': '4.5.3.56',
        'numpy': '1.21.2',
        'ultralytics': '8.3.0',
        'python-dotenv': '0.19.0',
        'tweepy': '4.0.0',
        'google-auth-oauthlib': '0.4.6',
        'google-api-python-client': '2.19.1',
        'eventlet': '0.33.0',
        'werkzeug': '2.0.2',
        'psutil': '5.9.0',
        'gunicorn': '20.1.0',
        'flask-limiter': '2.4.1',
        'waitress': '2.1.2'
    }
    
    # Optional packages (for advanced features)
    optional_packages = {
        'tensorflow': '2.6.0',
        'pandas': '1.3.3',
        'scikit-learn': '0.24.2',
        'pillow': '8.3.2',
        'boto3': '1.18.44',
        'google-auth-httplib2': '0.1.0',
        'python-engineio': '4.2.1',
        'python-socketio': '5.4.0'
    }
    
    print("📦 Checking required packages...")
    all_installed = True
    for package, version in required_packages.items():
        try:
            installed = pkg_resources.get_distribution(package)
            if installed.version != version:
                print(f"⚠️ {package} version mismatch: required {version}, installed {installed.version}")
                all_installed = False
            else:
                print(f"✅ {package} version {version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} not installed")
            all_installed = False
    
    print("\n📦 Checking optional packages...")
    for package, version in optional_packages.items():
        try:
            installed = pkg_resources.get_distribution(package)
            if installed.version != version:
                print(f"⚠️ {package} (optional) version mismatch: required {version}, installed {installed.version}")
            else:
                print(f"✅ {package} (optional) version {version}")
        except pkg_resources.DistributionNotFound:
            print(f"⚠️ {package} (optional) not installed - some advanced features may not work")
    
    return all_installed

def check_environment_variables():
    # Core required environment variables
    required_vars = [
        'FLASK_APP',
        'FLASK_ENV',
        'SECRET_KEY'
    ]
    
    # Optional environment variables (for advanced features)
    optional_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_BUCKET_NAME',
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'INSTAGRAM_CLIENT_ID',
        'INSTAGRAM_CLIENT_SECRET',
        'YOUTUBE_CLIENT_ID',
        'YOUTUBE_CLIENT_SECRET'
    ]
    
    load_dotenv()
    
    print("🔧 Checking required environment variables...")
    all_set = True
    for var in required_vars:
        if not os.getenv(var):
            print(f"❌ Environment variable {var} not set")
            all_set = False
        else:
            print(f"✅ Environment variable {var} is set")
    
    print("\n🔧 Checking optional environment variables...")
    for var in optional_vars:
        if not os.getenv(var):
            print(f"⚠️ Environment variable {var} not set (optional)")
        else:
            print(f"✅ Environment variable {var} is set")
    
    return all_set

def check_gpu():
    if not TENSORFLOW_AVAILABLE:
        print("⚠️ TensorFlow not available - GPU check skipped")
        return True  # Not critical for basic functionality
    
    try:
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU available: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"  - {gpu}")
            return True
        else:
            print("⚠️ No GPU available, using CPU")
            return True  # Not critical for basic functionality
    except:
        print("❌ Error checking GPU availability")
        return True  # Not critical for basic functionality

def check_opencv():
    try:
        print(f"✅ OpenCV version: {cv2.__version__}")
        return True
    except:
        print("❌ Error checking OpenCV")
        return False

def check_system_info():
    print("\nSystem Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python Location: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")

def main():
    print("Checking system requirements...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("PIP Packages", check_pip_packages),
        ("Environment Variables", check_environment_variables),
        ("GPU", check_gpu),
        ("OpenCV", check_opencv)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name} Check:")
        if not check_func():
            all_passed = False
    
    check_system_info()
    
    if all_passed:
        print("\n✅ All checks passed!")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 