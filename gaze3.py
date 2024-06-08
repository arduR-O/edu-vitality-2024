import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gaze_tracking import GazeTracking

# Initialize GazeTracking and webcam
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Initialize plot
fig, (ax1, ax2) = plt.subplots(2, 1)

left_x_data, left_y_data = [], []
right_x_data, right_y_data = [], []

# Set up plot parameters
ax1.set_xlim(0, 640)  # Assuming width of the webcam feed is 640 pixels
ax1.set_ylim(0, 480)  # Assuming height of the webcam feed is 480 pixels
ax1.set_title('Left Pupil Position')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')

ax2.set_xlim(0, 640)
ax2.set_ylim(0, 480)
ax2.set_title('Right Pupil Position')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')

# Initialize empty lines for left and right pupil
left_line, = ax1.plot([], [], 'ro')
right_line, = ax2.plot([], [], 'bo')

def update_plot(frame):
    # Get a new frame from the webcam
    _, frame = webcam.read()

    # Send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Update data lists for plotting
    if left_pupil is not None:
        left_x_data.append(left_pupil[0])
        left_y_data.append(left_pupil[1])
    if right_pupil is not None:
        right_x_data.append(right_pupil[0])
        right_y_data.append(right_pupil[1])

    # Update lines with new data
    left_line.set_data(left_x_data, left_y_data)
    right_line.set_data(right_x_data, right_y_data)

    # Display text on frame
    text = ""
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # Display the frame
    cv2.imshow("Demo", frame)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        webcam.release()
        cv2.destroyAllWindows()
        plt.close()

    return left_line, right_line

# Create animation
ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=50)

# Show plot
plt.show()
