from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import cv2
import uvicorn
import time

app = FastAPI()

def generate_video():
    # Open the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not start camera.")

    # Set the width and height of the video capture
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            continue

        # Encode the frame in JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Convert the encoded frame to bytes
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Sleep for 1 second
        time.sleep(0.042)

    # Release the camera
    cap.release()

@app.get("/")
def read_root():
    return {"message": "MJPEG Streaming Server"}

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
