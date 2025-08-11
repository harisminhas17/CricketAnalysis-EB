import os

# Get the absolute path of the backend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_URI = 'sqlite:///video.db'

# Upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
FRAMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'frames')
ANNOTATED_FOLDER = os.path.join(UPLOAD_FOLDER, 'annotated')
ANALYSIS_FOLDER = os.path.join(UPLOAD_FOLDER, 'analysis')

# Create required directories
for folder in [UPLOAD_FOLDER, FRAMES_FOLDER, ANNOTATED_FOLDER, ANALYSIS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# API configuration
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'png', 'jpg', 'jpeg', 'gif'}

# CORS configuration
CORS_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]
