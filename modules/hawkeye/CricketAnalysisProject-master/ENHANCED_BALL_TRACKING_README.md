# Enhanced Ball Tracking System

This system provides advanced ball detection and tracking capabilities specifically designed for white circular cricket balls that are constantly changing position across multiple frames.

## Features

### 🎯 **Enhanced White Ball Detection**
- **Specialized for white circular objects**: Optimized HSV color filtering for white balls
- **Multiple detection strategies**: Combines color, shape, and motion analysis
- **Robust preprocessing**: Enhanced contrast and noise reduction for better detection

### 📈 **Multi-Frame Tracking**
- **Motion prediction**: Predicts ball position when detection fails
- **Trajectory smoothing**: Maintains smooth ball trajectory across frames
- **Velocity analysis**: Tracks ball velocity for motion analysis
- **Missing frame handling**: Continues tracking even when ball is temporarily occluded

### 🔄 **Motion Consistency**
- **Historical position tracking**: Uses previous positions to validate new detections
- **Velocity-based filtering**: Filters out false positives based on motion patterns
- **Adaptive thresholds**: Adjusts detection parameters based on ball movement

## Quick Start

### Basic Usage

```python
from enhanced_ball_tracker import EnhancedBallTracker

# Initialize tracker
tracker = EnhancedBallTracker()

# Process a single frame
ball_position = tracker.detect_white_ball(frame)

# Get trajectory
trajectory = tracker.get_trajectory()

# Visualize tracking
annotated_frame = tracker.visualize_tracking(frame, ball_position)
```

### Video Processing

```python
import cv2

# Open video
cap = cv2.VideoCapture('your_video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect ball
    ball_pos = tracker.detect_white_ball(frame)
    
    # Visualize
    annotated_frame = tracker.visualize_tracking(frame, ball_pos)
    
    # Display or save
    cv2.imshow('Ball Tracking', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Key Components

### 1. EnhancedBallTracker Class

The main class that handles white ball detection and tracking:

```python
tracker = EnhancedBallTracker(
    max_history_frames=10,  # Number of previous positions to remember
    prediction_frames=3      # Number of frames to predict ahead
)
```

**Key Methods:**
- `detect_white_ball(frame)`: Detect ball in a single frame
- `track_ball_across_frames(frames)`: Process multiple frames
- `get_trajectory()`: Get current ball trajectory
- `get_velocity_history()`: Get velocity history
- `visualize_tracking(frame, ball_pos)`: Create annotated frame
- `reset_tracking()`: Reset tracking state

### 2. Detection Pipeline

The system uses a multi-stage detection pipeline:

1. **Preprocessing**: Enhance contrast and reduce noise
2. **Color Filtering**: Detect white objects using HSV color space
3. **Shape Analysis**: Filter for circular objects
4. **Size Filtering**: Match cricket ball dimensions
5. **Motion Consistency**: Validate against previous positions
6. **Candidate Selection**: Choose best candidate based on multiple criteria

### 3. Motion Prediction

When ball detection fails, the system predicts position based on:
- Previous ball positions
- Velocity history
- Motion patterns

## Advanced Usage

### Customizing Detection Parameters

```python
tracker = EnhancedBallTracker()

# Adjust detection parameters
tracker.min_ball_radius = 5      # Minimum ball radius
tracker.max_ball_radius = 30     # Maximum ball radius
tracker.min_circularity = 0.5    # Minimum circularity
tracker.max_circularity = 1.5    # Maximum circularity
```

### Processing Multiple Frames

```python
# Process a list of frames
frames = [frame1, frame2, frame3, ...]
ball_positions = tracker.track_ball_across_frames(frames)

for i, pos in enumerate(ball_positions):
    if pos:
        print(f"Frame {i}: Ball at {pos}")
```

### Integrated System

For comprehensive analysis, use the integrated system:

```python
from integrated_ball_tracking import IntegratedBallTrackingSystem

system = IntegratedBallTrackingSystem()
results = system.process_video_frame_by_frame('video.mp4', 'output.mp4')
system.save_results('results.json')
```

## Command Line Usage

### Test Enhanced Tracker

```bash
python demo_enhanced_tracker.py
```

### Process Video with Integrated System

```bash
python integrated_ball_tracking.py --video input.mp4 --output output.mp4 --results results.json
```

### Test with Frame Directory

```bash
python test_enhanced_ball_tracker.py --frames-dir /path/to/frames --output-dir /path/to/output
```

## Performance Features

### Detection Accuracy
- **Enhanced white ball detection**: Specialized for cricket ball characteristics
- **Motion consistency filtering**: Reduces false positives
- **Multi-criteria scoring**: Combines shape, size, position, and motion

### Robustness
- **Missing frame handling**: Continues tracking when ball is occluded
- **Motion prediction**: Predicts position based on velocity
- **Adaptive thresholds**: Adjusts to different lighting conditions

### Real-time Capability
- **Optimized processing**: Efficient algorithms for real-time use
- **Frame-by-frame analysis**: Processes each frame independently
- **Minimal memory usage**: Efficient data structures

## Output and Analysis

### Trajectory Data
```python
trajectory = tracker.get_trajectory()
# Returns: [(x1, y1), (x2, y2), ...]

velocities = tracker.get_velocity_history()
# Returns: [(vx1, vy1), (vx2, vy2), ...]
```

### Visualization
- **Real-time annotation**: Shows ball position and trajectory
- **Detection status**: Indicates tracking state
- **Trajectory lines**: Visualizes ball path
- **Multiple detection methods**: Shows enhanced vs traditional detection

### Analysis Results
```json
{
  "total_frames": 1000,
  "detected_frames": 850,
  "detection_rate": 0.85,
  "trajectory_analysis": {
    "trajectory_length": 850,
    "start_position": [100, 200],
    "end_position": [500, 300],
    "average_velocity": [2.5, 1.0]
  }
}
```

## Troubleshooting

### Common Issues

1. **Low detection rate**
   - Adjust `white_ball_lower` and `white_ball_upper` parameters
   - Check lighting conditions in video
   - Verify ball size is within `min_ball_radius` and `max_ball_radius`

2. **False positives**
   - Increase `min_circularity` threshold
   - Adjust motion consistency parameters
   - Use ROI masking to focus on cricket field area

3. **Tracking instability**
   - Increase `max_history_frames` for better motion consistency
   - Adjust `velocity_smoothing_factor` for smoother tracking
   - Check for video quality issues

### Performance Optimization

1. **For real-time processing**
   - Reduce `max_history_frames`
   - Use smaller ROI area
   - Process every nth frame

2. **For accuracy**
   - Increase `max_history_frames`
   - Use larger ROI area
   - Process all frames

## Integration with Existing System

The enhanced ball tracker can be integrated with the existing ball detection infrastructure:

```python
# Use enhanced tracker for white balls
enhanced_pos = enhanced_tracker.detect_white_ball(frame)

# Use traditional tracker for other balls
traditional_pos = detect_ball(frame)

# Combine results
combined_pos = combine_detections(enhanced_pos, traditional_pos)
```

This provides the best of both worlds: specialized white ball detection with the robustness of the traditional system.

## Examples

See the following files for complete examples:
- `example_usage.py`: Basic usage demonstration
- `demo_enhanced_tracker.py`: Comprehensive demonstration
- `test_enhanced_ball_tracker.py`: Testing and analysis tools
- `integrated_ball_tracking.py`: Full integration example 