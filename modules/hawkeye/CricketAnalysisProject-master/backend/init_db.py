#!/usr/bin/env python3
"""
Database initialization script for Cricket Analytics Project
"""

import os
import sys
from app import app, db
from models import User, Video, GalleryItem, Post, Comment, Like, Share, Follow, Notification

def init_database():
    """Initialize the database with all tables"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create upload directories if they don't exist
            upload_dirs = [
                'uploads',
                'uploads/frames', 
                'uploads/annotated',
                'uploads/analysis',
                'uploads/social',
                'static/output',
                'static/profile_pics'
            ]
            
            for dir_path in upload_dirs:
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ Created directory: {dir_path}")
            
            print("✅ Database initialization completed successfully")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database() 