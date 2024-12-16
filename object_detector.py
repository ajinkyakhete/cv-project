"""import cv2
import numpy as np

class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert Image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use Canny Edge Detection to find edges in the image
        edges = cv2.Canny(blurred, 100, 200)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:  # Only consider contours with a significant area
                # Get the bounding rectangle of the contour
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect
                aspect_ratio = w / float(h)

                # Filter based on aspect ratio (to avoid picking up non-object contours)
                if 0.5 < aspect_ratio < 2.0:  # Adjust the aspect ratio range as needed
                    objects_contours.append(cnt)

        return objects_contours
"""

import cv2
import numpy as np

class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Gray Image", gray)  # Debugging window for grayscale image

        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use Canny Edge Detection to find edges in the image
        edges = cv2.Canny(blurred, 50, 150)  # Adjust thresholds as needed
        cv2.imshow("Edge Detection", edges)  # Debugging window for edge detection

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f"Contours detected: {len(contours)}")  # Log the number of contours detected

        # Filter valid contours
        objects_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:  # Area threshold for significant objects
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect
                aspect_ratio = w / float(h)

                # Filter contours based on aspect ratio
                if 0.3 < aspect_ratio < 3.0:  # Broader range to capture more objects
                    objects_contours.append(cnt)

        print(f"Valid objects detected: {len(objects_contours)}")  # Log valid objects
        return objects_contours
