from app import app         # importing the app variable from app package

from flask import render_template

def processed_gen():
        cap = cv2.VideoCapture(0)

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

                return data
            
def mediapipe_videofeed():
    while True:
        data = VideoCamera.processed_gen()

        frame=data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/first')
def my_html():
    return render_template("first.html") 
