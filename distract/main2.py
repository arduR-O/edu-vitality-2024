import cv2
import numpy as np
import math
from gaze_tracking import GazeTracking
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

gaze = GazeTracking()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

analysis = []
analysis_timestamps = []

# saved facial landmark detection model's name as LBFmodel
LBFmodel = "lbfmodel.yaml"

# create an instance of the Facial landmark Detector with the model
landmark_detector = cv2.face.createFacemarkLBF()
landmark_detector.loadModel(LBFmodel)

# 3D model points
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip
    (0.0, -330.0, -65.0),        # Chin
    (-225.0, 170.0, -135.0),     # Left eye left corner
    (225.0, 170.0, -135.0),      # Right eye right corner
    (-150.0, -150.0, -125.0),    # Left Mouth corner
    (150.0, -150.0, -125.0)      # Right mouth corner
])

def pose_estimate(img, landmarks):
    ans = ""
    size = img.shape
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    shape = np.array(landmarks, dtype=np.float32).astype(np.uint)

    image_points = np.array([
        shape[0][0][30],  # Nose tip
        shape[0][0][8],  # Chin
        shape[0][0][36],  # Left eye left corner
        shape[0][0][45],  # Right eye right corner
        shape[0][0][48],  # Left Mouth corner
        shape[0][0][54]  # Right mouth corner
    ], dtype="double")
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                  dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                     translation_vector, camera_matrix, dist_coeffs)

    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

    try:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        ang = int(math.degrees(math.atan(m)))
    except:
        ang = 90

    if -45 < ang and ang < 45:
        ans = True
    else:
        ans = False
    print("Angle:", ang)
    print("ans:", ans)
    cv2.line(img, p1, p2, (0, 255, 255), 2)

    return ans

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=2,
        minSize=(20, 20)
    )
    return faces, gray

cap = cv2.VideoCapture(0)

cap.set(3, 1280)  # set Width
cap.set(4, 720)  # set Height

# For real-time plotting
fig, ax = plt.subplots()
focus_values = []
time_data = []
start_time = time.time()

def update_plot(i):
    ax.clear()
    ax.plot(time_data, focus_values, 'b-')
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Focus Level')
    ax.set_title('User Focus Level Over Time')
    ax.grid(True)

ani = animation.FuncAnimation(fig, update_plot, interval=1000)

while True:
    ret, img = cap.read()
    faces, gray = detect_faces(img)
    gaze.refresh(img)
    attention = False
    img = gaze.annotated_frame()

    if gaze.is_center():
        attention = True
    boolout = False
    try:
        _, landmarks = landmark_detector.fit(gray, faces)
        boolout = pose_estimate(img, landmarks) and attention
    except Exception as e:
        print(e)

    if boolout:
        text = "Definitely Focussed Listening"
        print(text)
        analysis.append(1)
    elif attention:
        text = "Somewhat Focussed"
        print(text)
        analysis.append(0.5)
    else:
        text = "Distracted"
        print(text)
        analysis.append(0)

    analysis_timestamps.append(time.time() - start_time)

    # Remove old data beyond 20 seconds
    while analysis_timestamps and (time.time() - start_time - analysis_timestamps[0] > 20):
        analysis_timestamps.pop(0)
        analysis.pop(0)

    time_data = analysis_timestamps
    focus_values = analysis

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x + w]
        roi_color = img[y:y + h, x + w]

    cv2.imshow('Webcam Feed', img)
    k = cv2.waitKey(30) & 0xff  # press 'ESC' to quit
    if k == 27:
        distraction_count = focus_values.count(0)
        somewhat_count = focus_values.count(0.5)
        focused_count = focus_values.count(1)
        print("Distracted for: ", 0.3 * distraction_count, "secs")
        print("Somewhat focused for: ", 0.3 * somewhat_count, "secs")
        print("Fully focused for: ", 0.3 * focused_count, "secs")
        break

plt.show()
cap.release()
cv2.destroyAllWindows()
plt.show()
