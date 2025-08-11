import cv2
import numpy as np
from typing import List, Tuple
from performance_flags import PerformanceFlag, FlagType

def draw_performance_flags(frame: np.ndarray, flags: List[PerformanceFlag]) -> np.ndarray:
    """Draw performance flags on the frame."""
    annotated_frame = frame.copy()
    
    # Define colors for different flag types
    colors = {
        FlagType.EDGE_RISK: (0, 0, 255),      # Red
        FlagType.BAT_LAG: (0, 255, 0),        # Green
        FlagType.FOOTWORK_ISSUE: (255, 0, 0),  # Blue
        FlagType.BALANCE_ISSUE: (255, 255, 0), # Yellow
        FlagType.TIMING_ISSUE: (255, 0, 255)   # Purple
    }
    
    for flag in flags:
        # Get color for flag type
        color = colors.get(flag.type, (255, 255, 255))
        
        # Draw flag indicator
        x, y = flag.position
        cv2.circle(annotated_frame, (x, y), 10, color, -1)
        
        # Draw severity indicator
        severity_radius = int(20 * flag.severity)
        cv2.circle(annotated_frame, (x, y), severity_radius, color, 2)
        
        # Draw confidence bar
        bar_length = int(50 * flag.confidence)
        cv2.rectangle(annotated_frame, (x + 15, y - 5), (x + 15 + bar_length, y + 5), color, -1)
        
        # Draw flag description
        cv2.putText(annotated_frame, flag.description, (x + 20, y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw metadata if available
        if flag.metadata:
            y_offset = y + 20
            for key, value in flag.metadata.items():
                text = f"{key}: {value:.2f}"
                cv2.putText(annotated_frame, text, (x + 20, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                y_offset += 15
    
    return annotated_frame

def create_performance_summary(flags: List[PerformanceFlag], output_path: str):
    """Create a summary visualization of performance flags."""
    # Count flags by type
    flag_counts = {}
    for flag in flags:
        flag_counts[flag.type] = flag_counts.get(flag.type, 0) + 1
    
    # Create summary image
    summary_height = 300
    summary_width = 400
    summary = np.ones((summary_height, summary_width, 3), dtype=np.uint8) * 255
    
    # Draw title
    cv2.putText(summary, "Performance Flags Summary", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Draw flag counts
    y_offset = 70
    for flag_type, count in flag_counts.items():
        text = f"{flag_type.value}: {count}"
        cv2.putText(summary, text, (20, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        y_offset += 30
    
    # Draw severity distribution
    severities = [flag.severity for flag in flags]
    if severities:
        avg_severity = sum(severities) / len(severities)
        severity_text = f"Average Severity: {avg_severity:.2f}"
        cv2.putText(summary, severity_text, (20, y_offset + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Save summary
    cv2.imwrite(output_path, summary)

def create_flag_timeline(flags: List[PerformanceFlag], output_path: str):
    """Create a timeline visualization of performance flags."""
    if not flags:
        return
    
    # Get frame range
    frame_indices = [flag.frame_index for flag in flags]
    min_frame = min(frame_indices)
    max_frame = max(frame_indices)
    
    # Create timeline image
    timeline_height = 200
    timeline_width = max(800, (max_frame - min_frame) * 2)
    timeline = np.ones((timeline_height, timeline_width, 3), dtype=np.uint8) * 255
    
    # Draw frame numbers
    for i in range(min_frame, max_frame + 1, 10):
        x = (i - min_frame) * 2
        cv2.putText(timeline, str(i), (x, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    # Draw flags
    colors = {
        FlagType.EDGE_RISK: (0, 0, 255),
        FlagType.BAT_LAG: (0, 255, 0),
        FlagType.FOOTWORK_ISSUE: (255, 0, 0),
        FlagType.BALANCE_ISSUE: (255, 255, 0),
        FlagType.TIMING_ISSUE: (255, 0, 255)
    }
    
    for flag in flags:
        x = (flag.frame_index - min_frame) * 2
        y = 50 + int(flag.severity * 100)
        color = colors.get(flag.type, (255, 255, 255))
        
        # Draw flag point
        cv2.circle(timeline, (x, y), 5, color, -1)
        
        # Draw flag label
        cv2.putText(timeline, flag.type.value, (x + 10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    
    # Save timeline
    cv2.imwrite(output_path, timeline) 