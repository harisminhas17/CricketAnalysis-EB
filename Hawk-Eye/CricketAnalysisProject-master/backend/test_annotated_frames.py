#!/usr/bin/env python3
"""
Test script to verify that annotated frames are being generated correctly.
"""

import os
import sys
import glob
from datetime import datetime

def check_annotated_frames():
    """Check if annotated frames are being generated in the expected locations."""
    
    # Check the annotated folder
    annotated_folder = "data/annotated"
    if os.path.exists(annotated_folder):
        print(f"✓ Annotated folder exists: {annotated_folder}")
        
        # List all subdirectories (each should be a video analysis)
        subdirs = [d for d in os.listdir(annotated_folder) if os.path.isdir(os.path.join(annotated_folder, d))]
        
        if subdirs:
            print(f"Found {len(subdirs)} analysis directories:")
            for subdir in subdirs:
                subdir_path = os.path.join(annotated_folder, subdir)
                files = os.listdir(subdir_path)
                image_files = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
                print(f"  - {subdir}: {len(image_files)} annotated images")
                
                # Show first few files
                if image_files:
                    print(f"    Sample files: {image_files[:3]}")
        else:
            print("  No analysis directories found")
    else:
        print(f"✗ Annotated folder not found: {annotated_folder}")
    
    # Check the frames folder
    frames_folder = "data/frames"
    if os.path.exists(frames_folder):
        print(f"✓ Frames folder exists: {frames_folder}")
        
        subdirs = [d for d in os.listdir(frames_folder) if os.path.isdir(os.path.join(frames_folder, d))]
        
        if subdirs:
            print(f"Found {len(subdirs)} frame directories:")
            for subdir in subdirs:
                subdir_path = os.path.join(frames_folder, subdir)
                files = os.listdir(subdir_path)
                image_files = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
                print(f"  - {subdir}: {len(image_files)} frame images")
        else:
            print("  No frame directories found")
    else:
        print(f"✗ Frames folder not found: {frames_folder}")
    
    # Check the analysis folder
    analysis_folder = "data/analysis"
    if os.path.exists(analysis_folder):
        print(f"✓ Analysis folder exists: {analysis_folder}")
        
        subdirs = [d for d in os.listdir(analysis_folder) if os.path.isdir(os.path.join(analysis_folder, d))]
        
        if subdirs:
            print(f"Found {len(subdirs)} analysis directories:")
            for subdir in subdirs:
                subdir_path = os.path.join(analysis_folder, subdir)
                files = os.listdir(subdir_path)
                print(f"  - {subdir}: {len(files)} files")
                
                # Show specific file types
                json_files = [f for f in files if f.endswith('.json')]
                video_files = [f for f in files if f.endswith(('.mp4', '.avi', '.mov'))]
                image_files = [f for f in files if f.endswith(('.jpg', '.png', '.jpeg'))]
                
                if json_files:
                    print(f"    JSON files: {json_files}")
                if video_files:
                    print(f"    Video files: {video_files}")
                if image_files:
                    print(f"    Image files: {image_files[:3]}")
        else:
            print("  No analysis directories found")
    else:
        print(f"✗ Analysis folder not found: {analysis_folder}")

def check_recent_analysis():
    """Check for recent analysis results."""
    
    print("\n" + "="*50)
    print("RECENT ANALYSIS CHECK")
    print("="*50)
    
    # Check for files created in the last hour
    current_time = datetime.now()
    one_hour_ago = current_time.timestamp() - 3600
    
    folders_to_check = [
        "data/annotated",
        "data/frames", 
        "data/analysis"
    ]
    
    for folder in folders_to_check:
        if os.path.exists(folder):
            print(f"\nChecking {folder} for recent files:")
            
            recent_files = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_time = os.path.getmtime(file_path)
                    
                    if file_time > one_hour_ago:
                        relative_path = os.path.relpath(file_path, folder)
                        recent_files.append((relative_path, file_time))
            
            if recent_files:
                print(f"  Found {len(recent_files)} recent files:")
                for file_path, file_time in sorted(recent_files, key=lambda x: x[1], reverse=True):
                    time_diff = current_time.timestamp() - file_time
                    print(f"    - {file_path} ({time_diff:.0f}s ago)")
            else:
                print("  No recent files found")

def main():
    """Main function to run the check."""
    
    print("ANNOTATED FRAMES VERIFICATION")
    print("="*50)
    
    check_annotated_frames()
    check_recent_analysis()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("This script checks if:")
    print("1. Annotated frames are being generated in data/annotated/")
    print("2. Original frames are being extracted to data/frames/")
    print("3. Analysis results are being saved to data/analysis/")
    print("4. Recent analysis files exist (last hour)")
    print("\nIf you're not seeing annotated frames, check:")
    print("- The video upload and analysis process")
    print("- The object detection step in app.py")
    print("- The file permissions and disk space")

if __name__ == "__main__":
    main() 