#!/usr/bin/env python3
"""
Startup script for Cricket Analytics Project
This script ensures all dependencies and configurations are properly set up
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'opencv-python', 'numpy', 'ultralytics', 
        'flask-cors', 'flask-socketio', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\nInstall missing packages with: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_environment():
    """Set up environment variables and directories"""
    # Create .env file if it doesn't exist
    env_file = os.path.join('backend', '.env')
    if not os.path.exists(env_file):
        env_content = """# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=cricket-analytics-secret-key-change-in-production

# Database Configuration
DATABASE_URI=sqlite:///video.db

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    
    # Create required directories
    directories = [
        'backend/uploads',
        'backend/uploads/frames',
        'backend/uploads/annotated', 
        'backend/uploads/analysis',
        'backend/uploads/social',
        'backend/static/output',
        'backend/static/profile_pics',
        'backend/logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def initialize_database():
    """Initialize the database"""
    try:
        sys.path.append('backend')
        from init_db import init_database
        init_database()
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    backend_dir = os.path.join(os.getcwd(), 'backend')
    
    if platform.system() == 'Windows':
        subprocess.run(['python', 'app.py'], cwd=backend_dir)
    else:
        subprocess.run(['python3', 'app.py'], cwd=backend_dir)

def start_frontend():
    """Start the frontend development server"""
    print("\n🚀 Starting frontend server...")
    frontend_dir = os.path.join(os.getcwd(), 'frontend')
    
    if platform.system() == 'Windows':
        subprocess.run(['npm', 'start'], cwd=frontend_dir)
    else:
        subprocess.run(['npm', 'start'], cwd=frontend_dir)

def main():
    """Main startup function"""
    print("🔍 Checking Cricket Analytics Project setup...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing")
        sys.exit(1)
    
    # Setup environment
    print("\n⚙️ Setting up environment...")
    setup_environment()
    
    # Initialize database
    print("\n🗄️ Initializing database...")
    if not initialize_database():
        print("\n❌ Database initialization failed")
        sys.exit(1)
    
    print("\n✅ All checks passed! The project is ready to run.")
    print("\nTo start the project:")
    print("1. Backend: cd backend && python app.py")
    print("2. Frontend: cd frontend && npm start")
    print("\nOr run both simultaneously in separate terminals.")

if __name__ == "__main__":
    main() 