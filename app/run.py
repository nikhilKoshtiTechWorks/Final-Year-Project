from app import app
from flask import Response
from camera import VideoCamera      # mporting VideoCamera class from camera package
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils    
mp_pose = mp.solutions.pose


def gen(camera):                    # creating function to get the frame in data variable using get_frame() from camera package
    while True:
        data = camera.get_frame()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def calculate_angle(a,b,c):
    a = np.array(a)   # first i.e. shoulder
    b = np.array(b)   # first i.e. elbow
    c = np.array(c)   # first i.e. wrist
    
    radian = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])  # calculating angke
    angle = np.abs(radian * 180.0 / np.pi)                                       # returning absolute degree value
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def processed_gen():
    cap = cv2.VideoCapture(0)       # VideoCapture() is a function of openCV used to capture the video from default web camera

    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    # in above line 'Pose' is a model and by using 'as pose' we can access the model with specified arguments by variable 'pose'
        while cap.isOpened():
            ret, frame = cap.read()
            
            ## Detect stuff and render
            
            # Recolor image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # we are just reaaranging the color arrays i.e. blue, green, red
            image.flags.writeable = False    # just saving the memory while processing the 'image' feed
            
            # Make detection
            results = pose.process(image)    # using the 'pose' variable created above
            
            # Recoloring image again
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Exract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                
                # Calculate angle
                angle1 = calculate_angle(shoulder, elbow, wrist)
                angle2 = calculate_angle(knee, hip, shoulder)
                
                # Visualizing the angle
                cv2.putText(
                    image, str(angle1),
                    tuple(np.multiply(elbow, [640, 480]).astype(int)),            # actual coordinates on display window; 640x480 are the dimensions of video display window
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                )
                
                cv2.putText(
                    image, str(angle2),
                    tuple(np.multiply(hip, [640, 480]).astype(int)),            # actual coordinates on display window; 640x480 are the dimensions of video display window
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                )
                
                # Logic for threshold values
                if 170 < angle2 < 180:
                    cv2.rectangle(image, (0,0), (270,40), (0,255,0), -1)
                    cv2.putText(image, 'Hip is Right', (10, 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    
                else:
                    cv2.rectangle(image, (0,0), (270,40), (0,0,255), -1)
                    cv2.putText(image, 'Hip is Wrong', (10, 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    
                if angle1 > 55:
                    cv2.rectangle(image, (0,40), (270,80), (0,255,0), -1)
                    cv2.putText(image, 'Elbow is Right', (10, 70),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    
                else:
                    isCorrect = False
                    cv2.rectangle(image, (0,40), (270,80), (0,0,255), -1)
                    cv2.putText(image, 'Elbow is Wrong', (10, 70),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                    
            except:
                pass

            mp_drawing.draw_landmarks(
            image,                       # = processed image
            results.pose_landmarks,      # = gives the co-ordinated of points that are on the joints
            mp_pose.POSE_CONNECTIONS,    # = gives the combination of landmark points between which we are creating the connections(line)
            mp_drawing.DrawingSpec(color=(255,0,66), thickness=2, circle_radius=2),     # specifications of our drawing
            mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
        )
            
            ret, jpeg = cv2.imencode('.jpg', image)
            data = []
            data.append(jpeg.tobytes())

            frames=data[0]
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frames + b'\r\n\r\n')

            
def mediapipe_videofeed():
    print("vosk")

@app.route('/video_feed')
def video_feed():
    return Response(processed_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
 