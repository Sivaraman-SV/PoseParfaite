from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from PoseModule import poseDetector

app = Flask(__name__)
detector = poseDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_photo', methods=['POST'])
def analyze_photo():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (1280, 720))
    
    # Process image
    img = detector.findPose(img)
    lmList = detector.findPosition(img, False)
    feedback_message = "Good form!"
    angle = 0
    
    if len(lmList) >= 16:
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (210, 310), (0, 100))
        
        if per >= 95:
            feedback_message = "Peak contraction! Lower slowly."
        elif per <= 5:
            feedback_message = "Full extension! Lift again."
    
    return jsonify({
        'message': feedback_message,
        'angle': int(angle)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)