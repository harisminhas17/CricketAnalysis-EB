# Enhanced Cricket Ball Detection System

## Overview

This enhanced cricket ball detection system addresses the common challenges of detecting cricket balls in video footage, including:

- **Background noise** (red/white logos, dots, patterns)
- **Lighting variations** (glare, shadows, different lighting conditions)
- **Ball size variations** (distance from camera, zoom levels)
- **Motion blur** and **fast movement**

## Key Improvements

### 1. **Precise HSV Color Filtering**
- **Red ball detection**: Dual HSV ranges for red cricket balls (0-10° and 160-180°)
- **White ball detection**: Optimized HSV range for white cricket balls
- **Adaptive thresholds**: Parameters can be tuned for different lighting conditions

### 2. **Circularity Filtering**
- Uses contour analysis to identify ball-like circular shapes
- Eliminates rectangular patterns, logos, and irregular objects
- Configurable circularity thresholds (0.6-1.4)

### 3. **Size Filtering**
- Filters objects based on radius (3-20 pixels)
- Adapts to different camera distances and zoom levels
- Prevents detection of very small dots or large areas

### 4. **ROI (Region of Interest) Filtering**
- Focuses detection on the cricket field area
- Reduces false positives from spectators, equipment, or background
- Configurable ROI percentage (default: 60% of frame)

### 5. **Motion Filtering**
- Tracks ball position history across frames
- Ensures consistent motion patterns
- Rejects stationary objects or erratic movements

### 6. **Enhanced Preprocessing**
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)**: Improves contrast in varying lighting
- **Bilateral filtering**: Reduces noise while preserving edges
- **LAB color space processing**: Better color handling

## Files Overview

### Core Detection Files
- `track_ball.py` - Main ball detection implementation with enhanced algorithms
- `ball_detection_calibrator.py` - Real-time parameter tuning tool
- `test_ball_detection.py` - Testing and analysis tool
- `run_calibration.py` - Simple script to run the calibration tool

## Usage Instructions

### 1. **Calibrating Parameters (Recommended First Step)**

Run the calibration tool to tune parameters for your specific video:

```bash
cd backend
python run_calibration.py
```

**Calibration Tool Features:**
- Real-time HSV value adjustment
- Circularity threshold tuning
- Size range adjustment
- Motion distance parameter tuning
- ROI percentage adjustment
- Save/load parameter configurations

**Controls:**
- Use trackbars to adjust parameters
- Watch real-time detection in main window
- Press 's' to save parameters
- Press 'l' to load parameters
- Press 'q' to quit

### 2. **Testing Detection on Video Files**

Test the detection system on your video files:

```bash
# Test on video file
python test_ball_detection.py --video your_cricket_video.mp4 --output results.mp4

# Test on frame sequence
python test_ball_detection.py --frames ./frames/ --output ./analysis/
```

**Test Tool Features:**
- Detailed frame-by-frame analysis
- Detection confidence scoring
- Processing time measurement
- Comprehensive summary report
- JSON export of results

### 3. **Using in Your Code**

The enhanced detection is already integrated into your existing code:

```python
from track_ball import detect_ball

# Detect ball in a frame
ball_position = detect_ball(frame)

if ball_position:
    x, y = ball_position
    print(f"Ball detected at position: ({x}, {y})")
```

## Parameter Tuning Guide

### HSV Values for Different Conditions

**Red Cricket Balls:**
- **Bright lighting**: `[0, 100, 100]` to `[10, 255, 255]` and `[160, 100, 100]` to `[180, 255, 255]`
- **Low lighting**: `[0, 50, 50]` to `[10, 255, 255]` and `[160, 50, 50]` to `[180, 255, 255]`
- **Artificial lighting**: May need adjustment based on color temperature

**White Cricket Balls:**
- **Bright lighting**: `[0, 0, 200]` to `[180, 30, 255]`
- **Low lighting**: `[0, 0, 150]` to `[180, 50, 255]`

### Circularity Thresholds
- **Strict**: 0.7-1.3 (fewer false positives, may miss some balls)
- **Moderate**: 0.6-1.4 (balanced approach)
- **Loose**: 0.5-1.5 (more detections, may include false positives)

### Size Ranges
- **Close-up shots**: 8-20 pixels radius
- **Medium distance**: 5-15 pixels radius
- **Long shots**: 3-12 pixels radius

## Troubleshooting

### Common Issues and Solutions

**1. No balls detected:**
- Check if ROI is covering the field area
- Adjust HSV values for your lighting conditions
- Increase size range if balls appear small
- Lower circularity thresholds

**2. Too many false positives:**
- Increase circularity thresholds
- Adjust HSV ranges to be more specific
- Reduce ROI percentage
- Enable motion filtering

**3. Balls detected inconsistently:**
- Check for lighting variations in video
- Adjust preprocessing parameters
- Fine-tune motion distance threshold
- Consider using adaptive thresholds

**4. Performance issues:**
- Reduce ROI percentage
- Increase minimum contour area
- Use smaller kernel sizes for morphological operations

### Debug Information

The test tool provides detailed debug information:
- Total contours found
- Contours after circularity filtering
- Contours after size filtering
- Detection confidence scores
- Processing time per frame

## Advanced Features

### 1. **Motion Tracking**
The system maintains a history of ball positions to ensure consistent motion patterns. This helps eliminate stationary objects that might be detected as balls.

### 2. **Adaptive Scoring**
The detection uses a multi-factor scoring system:
- **Size score**: Prefers balls of expected size
- **Circularity score**: Prefers circular shapes
- **Position score**: Prefers positions near field center
- **Motion consistency**: Considers recent ball positions

### 3. **Fallback Mechanisms**
If the primary detection fails, the system can:
- Use the last known ball position
- Apply looser constraints
- Use alternative detection methods

## Integration with Existing Code

The enhanced detection system is backward compatible with your existing code. The main `detect_ball()` function signature remains the same, so no changes are needed to your existing applications.

## Performance Optimization

For real-time applications:
1. Reduce ROI percentage to focus on smaller areas
2. Increase minimum contour area to skip small objects
3. Use smaller morphological kernels
4. Consider frame skipping for very fast motion

## Future Enhancements

Potential improvements for even better detection:
1. **Machine Learning Integration**: Train a small CNN for ball verification
2. **Multi-camera Fusion**: Combine detections from multiple cameras
3. **Temporal Filtering**: Use Kalman filters for smoother tracking
4. **Adaptive Parameters**: Automatically adjust parameters based on scene analysis

## Support

If you encounter issues:
1. Use the calibration tool to tune parameters for your specific video
2. Run the test tool to get detailed analysis
3. Check the debug information for insights
4. Adjust parameters based on the troubleshooting guide

The enhanced system should significantly improve your cricket ball detection accuracy while maintaining good performance. 