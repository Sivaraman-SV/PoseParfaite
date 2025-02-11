'''
0 - nose
1 - left eye (inner)
2 - left eye
3 - left eye (outer)
4 - right eye (inner)
5 - right eye
6 - right eye (outer)
7 - left ear
8 - right ear
9 - mouth (left)
10 - mouth (right)
11 - left shoulder
12 - right shoulder
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index

'''

import cv2
import numpy as np
import time
import PoseModule as pm

from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from PoseModule import poseDetector

from flask import Flask #you have installed flask already, you need to install flask-login, flask-sqlalchemy and other modules.

cap = cv2.VideoCapture(r"C:\Users\svsiv\OneDrive\Desktop\Nexathon - Working Progress\ML model\PoseVideos\cur.mp4")  # r prefix is used to process the file address as a raw string, done because i was getting Syntax Error: unicode error
detector = pm.poseDetector()

pTime = 0
count = 0
dir = 0


while True:
    success, img = cap.read()

    #img = cv2.imread(r"C:\Users\svsiv\OneDrive\Desktop\Nexathon - Working Progress\ML model\PoseVideos\bicep3.jpg")
    img = cv2.resize(img, (1280,720))
    img = detector.findPose(img)

    lmList = detector.findPosition(img, False)
    print(lmList)


    if len(lmList) != 0:
          angle = detector.findAngle(img, 11, 13, 15)
          per = np.interp(angle, (210, 310), (0, 100))
          bar = np.interp(angle, (220, 310), (650, 100))
          print(angle)
          print(per)


          # Count logic
          if int(per) == 100:
               if dir == 0:
                    count += 0.5
                    dir = 1
          if int(per) == 0:
               if dir == 1:
                    count += 0.5
                    dir = 0
          print("Number of Reps: ", count)

    # Draw Bar
    cv2.rectangle(img, (1100, 100), (1175, 650), (255,0,255), 3)    
    cv2.rectangle(img, (1100, int(bar)), (1175, 650), (255,0,0), cv2.FILLED)
    cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0,0,0), 4)

        # Draw Curl Count
    cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)

    #cv2.putText(img, str(int(count)), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50,100), cv2.FONT_HERSHEY_PLAIN, 5, (255,0,0), 5)



    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'): #press 'q' to quit
        break


app = Flask(__name__)
detector = poseDetector()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    img_data = data['image'].split(',')[1]
    current_count = data['count']
    current_dir = data['direction']

    # Decode image
    nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
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
        
        # Exercise logic
        if per >= 95 and current_dir == 0:
            current_count += 0.5
            current_dir = 1
            feedback_message = "Peak contraction! Lower slowly."
        elif per <= 5 and current_dir == 1:
            current_count += 0.5
            current_dir = 0
            feedback_message = "Full extension! Lift again."

    return jsonify({
        'count': current_count,
        'direction': current_dir,
        'message': feedback_message,
        'angle': int(angle)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

