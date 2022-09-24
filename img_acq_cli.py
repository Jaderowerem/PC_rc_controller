import io
import socket
import struct
import time
import picamera


# raspberry pi side
client_socket = socket.socket()
client_socket.connect(('192.168.0.215', 8000))
connection = client_socket.makefile('wb')
cam = picamera.PiCamera()

try:
    cam.resolution = (1640, 922)
    cam.framerate = 30
    cam.sensor_mode = 5
    cam.awb_mode = "auto"

    cam.start_preview()
    time.sleep(3)
    print("sensor_mode:", cam.sensor_mode)
    print("resolution:", cam.resolution)
    print("framerate:", cam.framerate)
    print("auto white balance", cam.awb_mode)

    start = time.time()
    frame = io.BytesIO()   # binary file

    for f in cam.capture_continuous(frame, 'jpeg', use_video_port=True):
        size = frame.tell()     # returns current position of the file pointer (size of file expressed in bytes)
        connection.write(struct.pack('<L', size))   # send size of frame
        print("size of image frame:", struct.pack('<L', size))
        connection.flush()  # clears write buffer of the stream
        frame.seek(0)   # sets file pointer to the beginning
        connection.write(frame.read())  # send image frame

        if time.time() - start > 10:
            break

        # deallocate memory
        frame.seek(0)
        frame.truncate()
        print("frame sent")

    connection.write(struct.pack('<L', 0))
    print("end of frame transmission:", struct.pack('<L', 0))

finally:
    connection.close()
    client_socket.close()
    cam.close()
