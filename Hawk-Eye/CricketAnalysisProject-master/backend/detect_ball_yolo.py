from ultralytics import YOLO
import cv2
import numpy as np
import os

def is_red_or_white(image_crop):
    """Check if the cropped object has red or white pixels."""
    hsv = cv2.cvtColor(image_crop, cv2.COLOR_BGR2HSV)

    # Define color ranges for red and white
    red_lower1 = np.array([0, 70, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 70, 50])
    red_upper2 = np.array([180, 255, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 40, 255])

    # Create masks
    mask_red = cv2.inRange(hsv, red_lower1, red_upper1) | cv2.inRange(hsv, red_lower2, red_upper2)
    mask_white = cv2.inRange(hsv, white_lower, white_upper)

    red_pixels = cv2.countNonZero(mask_red)
    white_pixels = cv2.countNonZero(mask_white)

    total_pixels = image_crop.shape[0] * image_crop.shape[1]
    if (red_pixels / total_pixels > 0.05) or (white_pixels / total_pixels > 0.05):
        return True
    return False

def is_circular(image_crop):
    """Check if the object is approximately circular."""
    gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=10,
                               param1=50, param2=20, minRadius=3, maxRadius=30)
    return circles is not None

def detect_cricket_ball(video_path, conf=0.10, min_area=100, max_area=3000):
    model = YOLO('yolo11n.pt')
    results = model.predict(source=video_path, conf=conf, save=True)
    save_dir = results[0].save_dir
    print(f"Initial YOLO results saved in: {save_dir}")

    output_video_path = os.path.join(save_dir, "output_ball_detected.mp4")
    frame_width = int(results[0].orig_img.shape[1])
    frame_height = int(results[0].orig_img.shape[0])
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))

    for i, r in enumerate(results):
        img = r.orig_img.copy()
        ball_detected = False

        for box in r.boxes:
            if int(box.cls) == 32:  # sports ball
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)

                if min_area <= area <= max_area:
                    crop = img[y1:y2, x1:x2]
                    if is_red_or_white(crop) and is_circular(crop):
                        ball_detected = True
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        out.write(img)
        if ball_detected:
            print(f"Ball detected in frame {i}")

    out.release()
    print(f"Final video saved at: {output_video_path}")

if __name__ == "__main__":
    detect_cricket_ball('sample_video.mp4')
