import cv2
import numpy as np
import os
import json
import argparse
from track_ball import detect_ball, preprocess_frame, create_ball_color_masks, filter_by_circularity, filter_by_size, create_roi_mask
from typing import List, Tuple, Optional

class BallDetectionTester:
    """
    Test script for cricket ball detection with detailed analysis and visualization.
    """
    
    def __init__(self):
        self.detection_results = []
        self.frame_analysis = []
        
    def analyze_frame(self, frame: np.ndarray, frame_number: int) -> dict:
        """Analyze a single frame for ball detection with detailed metrics."""
        
        analysis = {
            'frame_number': frame_number,
            'ball_detected': False,
            'ball_position': None,
            'detection_confidence': 0.0,
            'candidates_found': 0,
            'processing_time': 0.0,
            'debug_info': {}
        }
        
        try:
            import time
            start_time = time.time()
            
            # Step 1: Preprocessing
            processed_frame = preprocess_frame(frame)
            
            # Step 2: Create ROI mask
            roi_mask, (roi_left, roi_top, roi_right, roi_bottom) = create_roi_mask(frame.shape)
            
            # Step 3: HSV color filtering
            hsv = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2HSV)
            ball_mask, red_mask, white_mask = create_ball_color_masks(hsv)
            
            # Apply ROI mask
            ball_mask = cv2.bitwise_and(ball_mask, roi_mask)
            
            # Step 4: Morphological operations
            kernel = np.ones((3, 3), np.uint8)
            ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_CLOSE, kernel)
            ball_mask = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)
            
            # Step 5: Find contours
            contours, _ = cv2.findContours(ball_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            analysis['debug_info']['total_contours'] = len(contours)
            
            if contours:
                # Step 6: Circularity filtering
                circular_contours = filter_by_circularity(contours)
                analysis['debug_info']['circular_contours'] = len(circular_contours)
                
                if circular_contours:
                    # Step 7: Size filtering
                    size_filtered = filter_by_size(circular_contours)
                    analysis['debug_info']['size_filtered'] = len(size_filtered)
                    analysis['candidates_found'] = len(size_filtered)
                    
                    if size_filtered:
                        # Step 8: Select best candidate
                        best_candidate = None
                        best_score = -float('inf')
                        
                        for contour, (x, y), radius in size_filtered:
                            area = cv2.contourArea(contour)
                            perimeter = cv2.arcLength(contour, True)
                            circularity = 4 * np.pi * area / (perimeter * perimeter)
                            
                            center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
                            distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                            
                            size_score = 1.0 / (1.0 + abs(radius - 8))
                            circularity_score = circularity
                            position_score = 1.0 / (1.0 + distance_from_center / 100)
                            
                            total_score = size_score + circularity_score + position_score
                            
                            if total_score > best_score:
                                best_score = total_score
                                best_candidate = (x, y)
                        
                        if best_candidate:
                            analysis['ball_detected'] = True
                            analysis['ball_position'] = best_candidate
                            analysis['detection_confidence'] = best_score
                            analysis['debug_info']['best_score'] = best_score
            
            analysis['processing_time'] = time.time() - start_time
            
        except Exception as e:
            analysis['debug_info']['error'] = str(e)
        
        return analysis
    
    def create_visualization(self, frame: np.ndarray, analysis: dict) -> np.ndarray:
        """Create visualization of the detection process."""
        
        vis_frame = frame.copy()
        
        # Draw ROI
        roi_mask, (roi_left, roi_top, roi_right, roi_bottom) = create_roi_mask(frame.shape)
        cv2.rectangle(vis_frame, (roi_left, roi_top), (roi_right, roi_bottom), (0, 255, 0), 2)
        
        # Draw detected ball
        if analysis['ball_detected'] and analysis['ball_position']:
            x, y = analysis['ball_position']
            cv2.circle(vis_frame, (x, y), 15, (0, 0, 255), 3)
            cv2.putText(vis_frame, f'Ball: ({x}, {y})', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(vis_frame, f'Confidence: {analysis["detection_confidence"]:.2f}', (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Add debug information
        cv2.putText(vis_frame, f'Frame: {analysis["frame_number"]}', (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(vis_frame, f'Candidates: {analysis["candidates_found"]}', (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(vis_frame, f'Time: {analysis["processing_time"]:.3f}s', (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return vis_frame
    
    def test_video(self, video_path: str, output_path: str = None, max_frames: int = None):
        """Test ball detection on a video file."""
        
        if not os.path.exists(video_path):
            print(f"Error: Video file {video_path} not found")
            return
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"Testing ball detection on video: {video_path}")
        print(f"Total frames: {total_frames}, FPS: {fps}")
        
        if max_frames:
            total_frames = min(total_frames, max_frames)
        
        # Setup video writer for output
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        detections = 0
        
        while frame_count < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze frame
            analysis = self.analyze_frame(frame, frame_count)
            self.frame_analysis.append(analysis)
            
            if analysis['ball_detected']:
                detections += 1
            
            # Create visualization
            vis_frame = self.create_visualization(frame, analysis)
            
            # Write to output video
            if output_path:
                out.write(vis_frame)
            
            # Display progress
            if frame_count % 30 == 0:  # Every 30 frames
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% - Detections: {detections}/{frame_count + 1}")
            
            frame_count += 1
        
        cap.release()
        if output_path:
            out.release()
        
        # Generate summary
        self.generate_summary(video_path)
    
    def test_image_sequence(self, frames_dir: str, output_dir: str = None):
        """Test ball detection on a sequence of images."""
        
        if not os.path.exists(frames_dir):
            print(f"Error: Frames directory {frames_dir} not found")
            return
        
        frame_files = [f for f in os.listdir(frames_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        frame_files.sort()
        
        if not frame_files:
            print(f"Error: No image files found in {frames_dir}")
            return
        
        print(f"Testing ball detection on {len(frame_files)} frames from {frames_dir}")
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        detections = 0
        
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)
            
            if frame is None:
                continue
            
            # Analyze frame
            analysis = self.analyze_frame(frame, i)
            self.frame_analysis.append(analysis)
            
            if analysis['ball_detected']:
                detections += 1
            
            # Create visualization
            vis_frame = self.create_visualization(frame, analysis)
            
            # Save output image
            if output_dir:
                output_path = os.path.join(output_dir, f'analysis_{i:04d}.jpg')
                cv2.imwrite(output_path, vis_frame)
            
            # Display progress
            if i % 10 == 0:  # Every 10 frames
                progress = (i / len(frame_files)) * 100
                print(f"Progress: {progress:.1f}% - Detections: {detections}/{i + 1}")
        
        # Generate summary
        self.generate_summary(frames_dir)
    
    def generate_summary(self, source_path: str):
        """Generate a detailed summary of the detection results."""
        
        total_frames = len(self.frame_analysis)
        detected_frames = sum(1 for analysis in self.frame_analysis if analysis['ball_detected'])
        detection_rate = (detected_frames / total_frames) * 100 if total_frames > 0 else 0
        
        avg_confidence = np.mean([analysis['detection_confidence'] for analysis in self.frame_analysis if analysis['ball_detected']])
        avg_processing_time = np.mean([analysis['processing_time'] for analysis in self.frame_analysis])
        
        print("\n" + "="*50)
        print("BALL DETECTION TEST SUMMARY")
        print("="*50)
        print(f"Source: {source_path}")
        print(f"Total frames analyzed: {total_frames}")
        print(f"Frames with ball detected: {detected_frames}")
        print(f"Detection rate: {detection_rate:.1f}%")
        print(f"Average confidence: {avg_confidence:.3f}")
        print(f"Average processing time: {avg_processing_time:.3f}s per frame")
        
        # Save detailed results
        results = {
            'source': source_path,
            'total_frames': total_frames,
            'detected_frames': detected_frames,
            'detection_rate': detection_rate,
            'average_confidence': avg_confidence,
            'average_processing_time': avg_processing_time,
            'frame_analysis': self.frame_analysis
        }
        
        output_file = f"ball_detection_results_{os.path.basename(source_path)}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Detailed results saved to: {output_file}")
        print("="*50)

def main():
    """Main function to run the ball detection tester."""
    
    parser = argparse.ArgumentParser(description='Test cricket ball detection')
    parser.add_argument('--video', type=str, help='Path to video file')
    parser.add_argument('--frames', type=str, help='Path to frames directory')
    parser.add_argument('--output', type=str, help='Output path for results')
    parser.add_argument('--max-frames', type=int, help='Maximum frames to process')
    
    args = parser.parse_args()
    
    tester = BallDetectionTester()
    
    if args.video:
        tester.test_video(args.video, args.output, args.max_frames)
    elif args.frames:
        tester.test_image_sequence(args.frames, args.output)
    else:
        print("Please provide either --video or --frames argument")
        print("Example usage:")
        print("  python test_ball_detection.py --video cricket_match.mp4 --output results.mp4")
        print("  python test_ball_detection.py --frames ./frames/ --output ./analysis/")

if __name__ == "__main__":
    main() 