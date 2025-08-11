#!/usr/bin/env python3
"""
Environment setup script for Cricket Analytics Project
"""

import os
from dotenv import load_dotenv

def setup_environment():
    """Set up environment variables"""
    
    # Check if .env file exists
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ .env file already exists")
        load_dotenv()
        return
    
    # Create .env file with default values
    env_content = """# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=cricket-analytics-secret-key-change-in-production

# Database Configuration
DATABASE_URI=sqlite:///video.db

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002

# Optional: AWS Configuration (for cloud features)
# AWS_ACCESS_KEY_ID=your-aws-access-key
# AWS_SECRET_ACCESS_KEY=your-aws-secret-key
# AWS_BUCKET_NAME=your-bucket-name

# Optional: Social Media API Keys (for sharing features)
# TWITTER_API_KEY=your-twitter-api-key
# TWITTER_API_SECRET=your-twitter-api-secret
# INSTAGRAM_CLIENT_ID=your-instagram-client-id
# INSTAGRAM_CLIENT_SECRET=your-instagram-client-secret
# YOUTUBE_CLIENT_ID=your-youtube-client-id
# YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env file with default configuration")
    print(f"📝 You can edit {env_file} to customize settings")

if __name__ == "__main__":
    setup_environment() 