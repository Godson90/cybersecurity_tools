import socket
import select
import sys

#Directly from Black Hat Python Book
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

#Directly from Black Hat Python Book
def hexdump(src, length=16): #Nice little function to print out wordsharkish output.
    results = list()
    try:
        if isinstance(src, bytes): #Converts Bytes into a string
            src = src.decode()
        for i in range(0, len(src), length): #process 16 bit chunks at a time (by default)
            word = str(src[i:i+length]) #converts the chunk a string
            printable = word.translate(HEX_FILTER) #translate it via HEX_FILTER
            hexa = ' '.join([f'{ord(c):02X}' for c in word]) #Format HEX to two digits (instead of 0x) and in a 16 digit format
            hexwidth = length*3
            results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}') #Formats list items
    except Exception as err:
        print(repr(err))

    if results:
        for line in results:
            print(line)

# Tweaked from Network basics with Python by (Sean Wilkins)
def proxy_handler(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        x, _, _ = select.select([client_socket, remote_socket], [], [])

        if client_socket in x:
            data = client_socket.recv(1024)
            if len(data) == 0:
                break
            print(f"[<==] Received {len(data)} bytes from local.")
            hexdump(data)
            remote_socket.send(data)

        if remote_socket in x:
            data = remote_socket.recv(1024)
            if len(data) == 0:
                break
            print(f"[<==] Received {len(data)} bytes from remote.")
            hexdump(data)
            client_socket.send(data)

    print("Sockets closing...")
    client_socket.close()
    remote_socket.close()


def server_loop(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"[!!] Failed to listen on {local_host}:{local_port} ....." )
        print(repr(e))
        sys.exit()

    print(f"[*] Listening on {local_host}:{local_port} .....")
    server.listen()
    while True:
        try:
            client_socket, addr = server.accept()
            print(f"> Received incoming connection {addr[0]} {addr[1]}")
            proxy_handler (client_socket, remote_host, remote_port)
        except KeyboardInterrupt:
            print("Exiting...")
            server.close()
            sys.exit(-1)


def main():

    local_host = input("Please enter Local IP: ")

    local_port = input('Please enterLocal TCP Port: ')
    local_port = int(local_port)

    remote_host = input("Please enter Remote IP: ")

    remote_port = input('Please enterRemote TCP Port: ')
    remote_port = int(remote_port)

    server_loop(local_host, local_port, remote_host, remote_port)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as err:
        print(repr(err))