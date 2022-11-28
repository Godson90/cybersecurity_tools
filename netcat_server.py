import socket

HOST = '127.0.0.1'
PORT = 7000
FILE = "beta.txt"


class netcatClone:
    def __init__(self, HOST, PORT, FILE):
        self.HOST = HOST
        self.PORT = PORT
        self.FILE = FILE
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def WaitForUpload(self):
        print('Listening....')
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        client_socket, _ = self.server_socket.accept()

        file_buffer = b''
        while True:
            received_data = client_socket.recv(4096)
            if received_data:
                file_buffer += received_data
                print(len(file_buffer))
            else:
                break

        with open(self.FILE, 'wb') as f:
            f.write(file_buffer)

        client_socket.close()
        self.server_socket.close()


if __name__ == '__main__':

    cc = netcatClone(HOST, PORT, FILE)
    cc.WaitForUpload()
