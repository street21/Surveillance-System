#========================
# Names and Roll Number: Vaania Asif 221438858, Sheikh Abdul Wahab 231524911
# Section: A
# Date: 1/13/2023
#========================


from socket import *
import struct
import cv2
import pickle

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

# List to store connected clients
clients = []

# Counter to keep track of the number of frames received
frame_counter = 0

while True:
    # Accept a new connection
    client_socket, address = serverSocket.accept()

    # Add the new client to the list of connected clients
    clients.append(client_socket)

    # Receive data from the client
    while True:
        try:
            # Receive the size of the frame first
            size = struct.unpack(">L", client_socket.recv(struct.calcsize(">L")))[0]
            # Receive the frame
            data = b""
            while len(data) < size:
                data += client_socket.recv(4096)
            # Deserialize the image
            image = pickle.loads(data, fix_imports=True, encoding="bytes")
            # Decode the image
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            # Show the frame on the server side
            cv2.imshow("server", image)
            cv2.waitKey(1)
        except socket.error as e:
            print("Error receiving the frame: ", e)
            # Remove the client from the list of connected clients
            clients.remove(client_socket)
            client_socket.close()
            break
    cv2.destroyAllWindows()
# Close the server socket
server_socket.close()

