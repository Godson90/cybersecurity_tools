import socket

HOST = '127.0.0.1'

def main():

    socketProtocol = socket.IPPROTO_TCP
    #socketProtocol = socket.IPPROTO_ICMP
    #socketProtocol = socket.IPPROTO_UDP

    sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socketProtocol)
    #sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.ntohs(3)) #all types of protocol sniffer

    sniffer.bind(HOST, 0)
    #sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1) #Use when sniffing all types of protocols
    print(sniffer.recv(65565)) #max size of IP Packet

if __name__ == '__main__':
    main()