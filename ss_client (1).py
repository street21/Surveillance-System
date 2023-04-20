#========================
# Names and Roll Number: Vaania Asif 221438858, Sheikh Abdul Wahab 231524911
# Section: A
# Date: 1/13/2023
#========================



import cv2
from socket import *
import struct
import pickle
import imutils

from ss_server import client_socket

serverName = 'localhost'  # 'servername'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Open the webcam
cam = cv2.VideoCapture(0)

# Counter to keep track of the number of frames sent
frame_counter = 0

# Compression parameters for the image
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    # Read a frame from the webcam
    ret, frame = cam.read()

    # Encode the frame in JPEG format
    result, image = cv2.imencode('.jpg', frame, encode_param)

    # Serialize the image
    data = pickle.dumps(image, 0)
    size = len(data)

    # Send the frame to the server every 10 frames
    if frame_counter % 10 == 0:
        try:
            # Send the size of the frame first
            clientSocket.sendall(struct.pack(">L", size))
            # Send the frame
            clientSocket.sendall(data)
            # Show the frame on the client side
            cv2.imshow("client", frame)
        except socket.error as e:
            print("Error sending the frame: ", e)
            break

    frame_counter += 1

    # Check if the user pressed 'q' to stop capturing video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cam.release()
cv2.destroyAllWindows()

# Close the socket
client_socket.close()
