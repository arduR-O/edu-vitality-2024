import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gaze_tracking import GazeTracking
import time

# Initialize GazeTracking and webcam
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Initialize plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Data lists for plotting
time_data = []
left_x_data, left_y_data = [], []
right_x_data, right_y_data = [], []

# Set up plot parameters
ax1.set_ylim(0, 640)  # Assuming width of the webcam feed is 640 pixels
ax1.set_title('Left Pupil Position Over Time')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Position (pixels)')

ax2.set_ylim(0, 640)
ax2.set_title('Right Pupil Position Over Time')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Position (pixels)')

# Initialize empty lines for left and right pupil
left_x_line, = ax1.plot([], [], 'r-', label='Left Pupil X')
left_y_line, = ax1.plot([], [], 'b-', label='Left Pupil Y')
right_x_line, = ax2.plot([], [], 'r-', label='Right Pupil X')
right_y_line, = ax2.plot([], [], 'b-', label='Right Pupil Y')

ax1.legend()
ax2.legend()

# Start time for plotting
start_time = time.time()

def update_plot(frame):
    # Get a new frame from the webcam
    _, frame = webcam.read()

    # Send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Current time for plotting
    current_time = time.time() - start_time
    time_data.append(current_time)

    # Update data lists for plotting
    if left_pupil is not None:
        left_x_data.append(left_pupil[0])
        left_y_data.append(left_pupil[1])
    else:
        left_x_data.append(None)
        left_y_data.append(None)

    if right_pupil is not None:
        right_x_data.append(right_pupil[0])
        right_y_data.append(right_pupil[1])
    else:
        right_x_data.append(None)
        right_y_data.append(None)

    # Update lines with new data
    left_x_line.set_data(time_data, left_x_data)
    left_y_line.set_data(time_data, left_y_data)
    right_x_line.set_data(time_data, right_x_data)
    right_y_line.set_data(time_data, right_y_data)

    # Set x-limits to follow the time
    ax1.set_xlim(0, current_time)
    ax2.set_xlim(0, current_time)

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

    # Show the frame
    cv2.imshow("Demo", frame)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        webcam.release()
        cv2.destroyAllWindows()
        plt.close()

    return left_x_line, left_y_line, right_x_line, right_y_line

# Create animation
ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=50)

# Show plot
plt.show()
