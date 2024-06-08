import cv2
import time
from gaze_tracking import GazeTracking  # Assuming you have the GazeTracking module

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Initialize timing variables
start_blink_time = None
start_not_in_frame_time = None

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        if start_blink_time is None:
            start_blink_time = time.time()
            text = "Closed"
        elif time.time() - start_blink_time > 5:
            text = "User is sleeping"
    else:
        start_blink_time = None

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is None and right_pupil is None:
        if start_not_in_frame_time is None:
            start_not_in_frame_time = time.time()
        elif time.time() - start_not_in_frame_time > 5:
            text = "User not in frame"
    else:
        start_not_in_frame_time = None

    # If no special condition is met, reset the text to indicate eye direction
    if text == "" and gaze.is_right():
        text = "Right"
    elif text == "" and gaze.is_left():
        text = "Left"
    elif text == "" and gaze.is_center():
        text = "Center"

    # Display text
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # Show the frame
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
cv2.destroyAllWindows()

