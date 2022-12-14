import io
import socket
import struct
import cv2 as cv
import numpy as np


# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

try:
    cnt = 0
    while True:
        try:
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

        except struct.error:
            print("some packets are lost :(")

        if not image_len:
            break

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)

        encoded_img = image_stream.getvalue()
        encoded_img = np.frombuffer(encoded_img, np.uint8)
        img = cv.imdecode(encoded_img, cv.IMREAD_COLOR)

        if img is None:
            pass

        else:
            print("frame received {}".format(cnt))
            cnt += 1
            img = cv.flip(img, 0)
            cv.imshow("img", img)
            cv.waitKey(1)

finally:
    connection.close()
    server_socket.close()
