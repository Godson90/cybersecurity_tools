import paramiko
import getpass
import sys

def ssh_command(ip, user, passwd, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    client.set_missing_host_key_policy(paramiko.WarningPolicy()) #Without this the new key everytime will cause a problem.

    try:    
        client.connect(ip, port, user, passwd)
    except Exception as e:
        print("Exception: ",e)
        sys.exit()

    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        stdout.channel.recv_exit_status() #EOF?
        output = stdout.read().decode()
        print ("Returned output:")
        print (output)
    except Exception as e:
        print("Exception: ",e)
        client.close()
        sys.exit()

    
    client.close()


if __name__ == '__main__':

       
    ip = input('Enter server IP: ') or '192.168.1.203'
    port = input('Enter port or <CR>: ') or 22

    user = input('Username: ')
    password = getpass.getpass()

    while True:

        cmd = input('Enter command or <CR>: ') or 'id'
        ssh_command(ip, user, password, cmd, port)
