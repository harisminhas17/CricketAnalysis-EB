import cv2
import numpy as np
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrameAnalyzer:
    def __init__(self, output_dir: str = "frames"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.frame_data = {}
        self.annotations = {}

    def extract_frames(self, video_path: str, frame_rate: int = 1) -> Dict[str, Any]:
        """
        Extract frames from video at specified frame rate
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_interval = int(fps / frame_rate)

            frames_data = {
                "total_frames": total_frames,
                "fps": fps,
                "frame_interval": frame_interval,
                "frame_paths": [],
                "frame_timestamps": []
            }

            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    frame_path = os.path.join(self.output_dir, f"frame_{frame_count:04d}.jpg")
                    cv2.imwrite(frame_path, frame)
                    timestamp = frame_count / fps
                    frames_data["frame_paths"].append(frame_path)
                    frames_data["frame_timestamps"].append(timestamp)

                frame_count += 1

            cap.release()
            return frames_data

        except Exception as e:
            logger.error(f"Error extracting frames: {str(e)}")
            raise

    def save_annotation(self, frame_index: int, annotation_data: Dict[str, Any]) -> bool:
        """
        Save annotation data for a specific frame
        """
        try:
            if frame_index not in self.annotations:
                self.annotations[frame_index] = []

            self.annotations[frame_index].append({
                "id": len(self.annotations[frame_index]),
                "type": annotation_data["type"],
                "data": annotation_data["data"],
                "timestamp": datetime.now().isoformat()
            })

            # Save annotations to file
            self._save_annotations_to_file()
            return True

        except Exception as e:
            logger.error(f"Error saving annotation: {str(e)}")
            return False

    def get_annotations(self, frame_index: int) -> List[Dict[str, Any]]:
        """
        Get all annotations for a specific frame
        """
        return self.annotations.get(frame_index, [])

    def delete_annotation(self, frame_index: int, annotation_id: int) -> bool:
        """
        Delete a specific annotation
        """
        try:
            if frame_index in self.annotations:
                self.annotations[frame_index] = [
                    ann for ann in self.annotations[frame_index]
                    if ann["id"] != annotation_id
                ]
                self._save_annotations_to_file()
                return True
            return False

        except Exception as e:
            logger.error(f"Error deleting annotation: {str(e)}")
            return False

    def update_annotation(self, frame_index: int, annotation_id: int, 
                         new_data: Dict[str, Any]) -> bool:
        """
        Update an existing annotation
        """
        try:
            if frame_index in self.annotations:
                for ann in self.annotations[frame_index]:
                    if ann["id"] == annotation_id:
                        ann["data"] = new_data
                        ann["timestamp"] = datetime.now().isoformat()
                        self._save_annotations_to_file()
                        return True
            return False

        except Exception as e:
            logger.error(f"Error updating annotation: {str(e)}")
            return False

    def _save_annotations_to_file(self):
        """
        Save all annotations to a JSON file
        """
        try:
            annotations_file = os.path.join(self.output_dir, "annotations.json")
            with open(annotations_file, 'w') as f:
                json.dump(self.annotations, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving annotations to file: {str(e)}")
            raise

    def load_annotations_from_file(self):
        """
        Load annotations from JSON file
        """
        try:
            annotations_file = os.path.join(self.output_dir, "annotations.json")
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    self.annotations = json.load(f)
        except Exception as e:
            logger.error(f"Error loading annotations from file: {str(e)}")
            raise

    def get_frame_metadata(self, frame_index: int) -> Dict[str, Any]:
        """
        Get metadata for a specific frame
        """
        try:
            frame_path = os.path.join(self.output_dir, f"frame_{frame_index:04d}.jpg")
            if os.path.exists(frame_path):
                frame = cv2.imread(frame_path)
                height, width = frame.shape[:2]
                return {
                    "width": width,
                    "height": height,
                    "path": frame_path,
                    "annotations": self.get_annotations(frame_index)
                }
            return {}
        except Exception as e:
            logger.error(f"Error getting frame metadata: {str(e)}")
            return {}

    def export_annotated_frame(self, frame_index: int, output_path: str) -> bool:
        """
        Export a frame with its annotations
        """
        try:
            frame_path = os.path.join(self.output_dir, f"frame_{frame_index:04d}.jpg")
            if not os.path.exists(frame_path):
                return False

            frame = cv2.imread(frame_path)
            annotations = self.get_annotations(frame_index)

            # Draw annotations on frame
            for ann in annotations:
                if ann["type"] == "drawing":
                    points = ann["data"]["points"]
                    color = ann["data"]["color"]
                    thickness = ann["data"]["thickness"]
                    cv2.polylines(frame, [np.array(points)], False, color, thickness)
                elif ann["type"] == "text":
                    text = ann["data"]["text"]
                    position = ann["data"]["position"]
                    color = ann["data"]["color"]
                    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                              1, color, 2)

            cv2.imwrite(output_path, frame)
            return True

        except Exception as e:
            logger.error(f"Error exporting annotated frame: {str(e)}")
            return False 