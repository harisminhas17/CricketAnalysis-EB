import cv2
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EdgeDetection:
    def __init__(self, method: str = 'canny'):
        self.method = method

    def detect_edges(self, image: np.ndarray, low_threshold: int = 50, high_threshold: int = 150) -> Optional[np.ndarray]:
        """Detect edges in an image using the specified method."""
        try:
            if self.method == 'canny':
                edges = cv2.Canny(image, low_threshold, high_threshold)
                return edges
            elif self.method == 'sobel':
                grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
                grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
                edges = cv2.magnitude(grad_x, grad_y)
                edges = np.uint8(edges)
                return edges
            else:
                logger.error(f"Unknown edge detection method: {self.method}")
                return None
        except Exception as e:
            logger.error(f"Error in edge detection: {str(e)}")
            return None 