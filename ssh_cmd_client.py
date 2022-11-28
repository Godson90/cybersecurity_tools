import paramiko
import getpass
import sys

def ssh_command(ip, user, passwd, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.set_missing_host_key_policy(paramiko.WarningPolicy()) 

    try:    
        client.connect(ip, port, user, passwd)
    except Exception as err:
        print("Exception: ",err)
        sys.exit(-1)

    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        stdout.channel.recv_exit_status() #EOF?
        output = stdout.read().decode()
        print ("output:")
        print (output)
    except Exception as err:
        print("Exception: ",err)
        client.close()
        sys.exit(-1)

    
    client.close()


if __name__ == '__main__':

       
    ip = input('Enter server IP: ') 
    port = input('Enter port : ') or 22

    user = input('Username: ')
    password = getpass.getpass()

    while True:

        cmd = input('Enter command : ') or 'id'
        ssh_command(ip, user, password, cmd, port)
