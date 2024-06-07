import cv2
import requests
import numpy as np

def consume_stream(url):
    stream = requests.get(url, stream=True)
    if stream.status_code != 200:
        print("Failed to connect to the stream")
        return

    bytes_data = b''
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')
        b = bytes_data.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes_data[a:b+2]
            bytes_data = bytes_data[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('MJPEG Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_url = 'http://localhost:8001/video_feed'
    consume_stream(stream_url)
