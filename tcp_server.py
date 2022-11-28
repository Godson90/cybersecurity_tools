import socket
import sys
import typer


app = typer.Typer()

@app.command()
def tcpserver():
    HOST  = "127.0.0.1"
    PORT = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f'[*] Listening on {HOST}:{PORT}', "Press Ctrl-C to Exit")

        while True:
            try:
                client_socket, address = server_socket.accept()

            except KeyboardInterrupt:
                print("\nClosing Server Socket...")
                server_socket.close()
                sys.exit(-1)
            with client_socket:
                print(f'[*] Accepted connection from {address[0]}:{address[1]}')
                request = client_socket.recv(1024)
                print (f'[*] Recieved: {request.decode("utf-8")}')
                client_socket.send(b'This is the server response!!!!')




if __name__ == "__main__":
    app()