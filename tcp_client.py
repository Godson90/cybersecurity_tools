import socket
import sys


host = '127.0.0.1'
port = 5555
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        message = (b'This is a test message from the client!')
        print('sending:', message.decode('utf-8'))
        client_socket.send(message)
        response = client_socket.recv(1204)
        print('recieved:', response.decode('utf-8'))
except ConnectionRefusedError:
    print('\nConnection was refused by server')
    sys.exit(-1)



