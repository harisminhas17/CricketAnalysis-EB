import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class AnnotationType(Enum):
    BALL = "ball"
    PLAYER = "player"
    BAT = "bat"
    PITCH = "pitch"
    SHOT_ZONE = "shot_zone"
    TRAJECTORY = "trajectory"
    TEXT = "text"
    ARROW = "arrow"
    CIRCLE = "circle"
    RECTANGLE = "rectangle"

@dataclass
class Annotation:
    type: AnnotationType
    points: List[Tuple[int, int]]
    color: Tuple[int, int, int]
    thickness: int
    label: str = ""
    confidence: float = 1.0

class FrameAnnotator:
    def __init__(self):
        self.annotations: List[Annotation] = []
        self.colors = {
            AnnotationType.BALL: (0, 255, 0),      # Green
            AnnotationType.PLAYER: (255, 0, 0),    # Blue
            AnnotationType.BAT: (0, 0, 255),       # Red
            AnnotationType.PITCH: (128, 128, 128), # Gray
            AnnotationType.SHOT_ZONE: (255, 255, 0), # Yellow
            AnnotationType.TRAJECTORY: (255, 0, 255), # Purple
            AnnotationType.TEXT: (255, 255, 255),  # White
            AnnotationType.ARROW: (0, 255, 255),   # Cyan
            AnnotationType.CIRCLE: (255, 128, 0),  # Orange
            AnnotationType.RECTANGLE: (128, 0, 128) # Purple
        }
    
    def add_annotation(self, annotation: Annotation):
        """Add a new annotation."""
        self.annotations.append(annotation)
    
    def clear_annotations(self):
        """Clear all annotations."""
        self.annotations = []
    
    def draw_annotation(self, frame: np.ndarray, annotation: Annotation) -> np.ndarray:
        """Draw a single annotation on the frame."""
        if annotation.type == AnnotationType.BALL:
            for point in annotation.points:
                cv2.circle(frame, point, 5, annotation.color, -1)
                if annotation.label:
                    cv2.putText(frame, annotation.label, 
                              (point[0] + 10, point[1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.PLAYER:
            if len(annotation.points) >= 2:
                cv2.rectangle(frame, annotation.points[0], annotation.points[1],
                            annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.BAT:
            if len(annotation.points) >= 2:
                cv2.line(frame, annotation.points[0], annotation.points[1],
                        annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.PITCH:
            if len(annotation.points) >= 2:
                cv2.rectangle(frame, annotation.points[0], annotation.points[1],
                            annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.SHOT_ZONE:
            if len(annotation.points) >= 3:
                points = np.array(annotation.points, np.int32)
                cv2.polylines(frame, [points], True, annotation.color, annotation.thickness)
                if annotation.label:
                    center = np.mean(points, axis=0, dtype=np.int32)
                    cv2.putText(frame, annotation.label,
                              (center[0], center[1]),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.TRAJECTORY:
            if len(annotation.points) >= 2:
                for i in range(len(annotation.points) - 1):
                    cv2.line(frame, annotation.points[i], annotation.points[i + 1],
                            annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.TEXT:
            if len(annotation.points) >= 1:
                cv2.putText(frame, annotation.label,
                          annotation.points[0],
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.ARROW:
            if len(annotation.points) >= 2:
                cv2.arrowedLine(frame, annotation.points[0], annotation.points[1],
                              annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.CIRCLE:
            if len(annotation.points) >= 2:
                center = annotation.points[0]
                radius = int(np.linalg.norm(np.array(annotation.points[1]) - np.array(center)))
                cv2.circle(frame, center, radius, annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (center[0] - radius, center[1] - radius - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        elif annotation.type == AnnotationType.RECTANGLE:
            if len(annotation.points) >= 2:
                cv2.rectangle(frame, annotation.points[0], annotation.points[1],
                            annotation.color, annotation.thickness)
                if annotation.label:
                    cv2.putText(frame, annotation.label,
                              (annotation.points[0][0], annotation.points[0][1] - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, annotation.color, 2)
        
        return frame
    
    def annotate_frame(self, frame: np.ndarray) -> np.ndarray:
        """Annotate a frame with all current annotations."""
        annotated_frame = frame.copy()
        for annotation in self.annotations:
            annotated_frame = self.draw_annotation(annotated_frame, annotation)
        return annotated_frame
    
    def save_annotations(self, file_path: str):
        """Save annotations to a JSON file."""
        annotations_data = []
        for annotation in self.annotations:
            annotations_data.append({
                'type': annotation.type.value,
                'points': annotation.points,
                'color': annotation.color,
                'thickness': annotation.thickness,
                'label': annotation.label,
                'confidence': annotation.confidence
            })
        
        with open(file_path, 'w') as f:
            json.dump(annotations_data, f, indent=2)
    
    def load_annotations(self, file_path: str):
        """Load annotations from a JSON file."""
        with open(file_path, 'r') as f:
            annotations_data = json.load(f)
        
        self.annotations = []
        for data in annotations_data:
            annotation = Annotation(
                type=AnnotationType(data['type']),
                points=data['points'],
                color=tuple(data['color']),
                thickness=data['thickness'],
                label=data['label'],
                confidence=data['confidence']
            )
            self.annotations.append(annotation) 