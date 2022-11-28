import socket
import sys
import subprocess
import paramiko
import time
import os.path

#Use if displaying key as text
#import io

try:
    if os.path.exists ("private_key.key"):
        host_key = paramiko.RSAKey.from_private_key_file("private_key.key")
    else:
        host_key = paramiko.RSAKey.generate(4096)
        host_key.write_private_key_file ("private_key.key")
except Exception as e:
   print("Exception: ",e)
   sys.exit()


#Display Key as Text
#privateString = io.StringIO()
#host_key.write_private_key(privateString)
#print(privateString.getvalue())

class Server(paramiko.ServerInterface):

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        if (username == "") and (password == ""):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_pty_request (self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_exec_request(self, channel, command):
        print ("Grabbing subprocess information...")
        cmd_output = subprocess.check_output(command, shell=True)
        cmd_output = cmd_output.strip()        
        channel.send(cmd_output)
        return True


def listener():

    #New Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 22)) #listening Port
    
    print ("Listening...")
    sock.listen(1)
    
    client, addr = sock.accept() #Waiting for remote connection

        
    #New Transport
    print("Opening new Paramiko Transport...")
    t = paramiko.Transport(client)
    t.load_server_moduli()
    t.add_server_key(host_key)
    server = Server()
    print ("Starting Server...")
    t.start_server(server=server)


    #New Channel

    chan = t.accept(10) #Accepts new channel from exec_command
    print("Opening new Paramiko Channel...")
    if chan is None:
        print("No Channel...") #Wrong credentials?
    else:        
        print("Channel is Authenticated...")
        time.sleep(.1) #Gives time for subprocess to finish.

        chan.close() #Closing Channel
        t.close() #Closing Transport
        sock.close() #Closing Socket
        print ("Exiting...")

while True:

    try:
        listener()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)