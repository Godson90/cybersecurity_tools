import socket
#import sys

HOST = '127.0.0.1'
PORT = 7000
FILE = "sent.txt"

class netcatclone:
    def __init__(self, HOST, PORT, FILE):
        self.HOST = HOST
        self.PORT = PORT
        self.FILE = FILE
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def SendUpload(self):
        print('Connecting')
        self.client_socket.connect((self.HOST, self.PORT))

        try:

            with open(FILE, "rb") as f:
                while True:
                    read_data = f.read(4096)
                    if not read_data:
                        #Transmit complete
                        break
                    self.client_socket.sendall(read_data)
            
            self.client_socket.close()

        except Exception as e: 
            print(repr(e))

if __name__ == '__main__':

    cc = netcatclone(HOST, PORT, FILE)
    cc.SendUpload()
