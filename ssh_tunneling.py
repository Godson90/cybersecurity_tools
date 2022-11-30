import getpass
import socket
import select
import sys
import  paramiko

def handler(channel, host, port):
    print("Aquiring new socket")
    sock = socket.socket()
    try:
        sock.connect(host, port)
    except Exception as err:
        print(f'Forwarding request to {host}:{port} failed: {err}')
        return
    print("Connection success! Tunnel open %r -> %r -> %r" %(channel.origin_addr, channel.getpeername(), (host, port)))

    while True:
        r, w, x = select.select([sock, channel], [] ,[])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            channel.send(data)
        if channel in r:
            data = channel.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    channel.close()
    sock.close()
    print('Tunnel terminated from %r' %(channel.origin_addr,))


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        channel = transport.accept(1000)
        print("Opening new channel...")
        if channel is None:
            continue
        handler(channel, remote_host, remote_port)

def main():

    local_ip = input(str("Please enter SSH Server IP address:"))

    local_port = input('Please enter SSH Server port or <CR>:') or 22
    #local_port -int(local_port)

    user = input(str('Please enter SSH Server Username:'))
    password = getpass.getpass()

    forward_port = input('Please enter SSH Server Forwarding Port or <CR>:') or 5000

    remote_ip = input(str("Please enter Remote Server IP address:"))
    remote_port = input('Please enter Remote Server port:')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    try:
        client.connect(local_ip,
                       local_port,
                       user,
                       password)
        print(f'Connectiong to ssh host {local_ip}:{local_port} ....')
    except Exception as err:
        print(f'Connection failed to {local_ip}:{local_port}:{err}')
        sys.exit(1)
    print(f'Forwarding SSH Server port {forward_port} to {remote_ip}:{remote_port} ....')

    try:
        reverse_forward_tunnel(forward_port, remote_ip, remote_port,client.get_transport())

    except KeyboardInterrupt:
        print('Port forwarind stopped.')
        sys.exit(0)
if __name__ == "__main__":
    main()
