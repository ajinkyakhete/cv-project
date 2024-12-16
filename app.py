from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import numpy as np
from object_detector import HomogeneousBgDetector
import os  # Add this line at the top of your file

app = Flask(__name__)

# Global variables
cap = None
detector = HomogeneousBgDetector()
video_streaming = False

def generate_frames():
    """Generate video frames for streaming."""
    global cap
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            # ArUco marker detection for size measurement
            parameters = cv2.aruco.DetectorParameters()
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
            corners, _, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
            
            if corners:
                int_corners = np.int0(corners)
                cv2.polylines(frame, int_corners, True, (0, 255, 0), 5)

                # Calculate pixel-to-cm ratio using marker
                aruco_perimeter = cv2.arcLength(corners[0], True)
                pixel_cm_ratio = aruco_perimeter / 20  # Assuming the marker is 20 cm

                # Object detection and size calculation
                contours = detector.detect_objects(frame)
                for cnt in contours:
                    rect = cv2.minAreaRect(cnt)
                    (x, y), (w, h), angle = rect
                    object_width = w / pixel_cm_ratio
                    object_height = h / pixel_cm_ratio

                    # Draw bounding box and size text
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.polylines(frame, [box], True, (255, 0, 0), 2)
                    cv2.putText(frame, f"W: {round(object_width, 1)} cm", (int(x - 50), int(y - 20)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(frame, f"H: {round(object_height, 1)} cm", (int(x - 50), int(y + 20)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Encode the frame
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the homepage with Start and Stop buttons."""
    global video_streaming, cap
    if request.method == 'POST':
        action = request.form['action']
        if action == 'start':
            ip_address = request.form['ip_address']
            video_url = f"http://{ip_address}/video"
            cap = cv2.VideoCapture(video_url)  # Start video capture
            if cap.isOpened():
                video_streaming = True
                return redirect(url_for('video_feed'))
        elif action == 'stop':
            if cap and cap.isOpened():
                cap.release()
            video_streaming = False
            return redirect(url_for('index'))
    return render_template('index.html', video_streaming=video_streaming)

@app.route('/video_feed')
def video_feed():
    """Stream video to the webpage."""
    global cap, video_streaming
    if not video_streaming or not cap.isOpened():
        return "Failed to open the video stream. Please check the IP address and try again.", 400
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
