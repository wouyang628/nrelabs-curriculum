import paramiko
import os
from scp import SCPClient

host=os.environ['ANTIDOTE_TARGET_HOST']

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

ssh=createSSHClient(host,22,"antidote","antidotepassword")

scp=SCPClient(ssh.get_transport())

scp.put('/antidote/stage0/configs/leaf2/interfaces', '/home/antidote/interfaces')
scp.put('/antidote/stage0/configs/leaf2/daemons', '/home/antidote/daemons')
scp.put('/antidote/stage0/configs/leaf2/frr.conf', '/home/antidote/frr.conf')


ssh.exec_command('sudo cp /home/antidote/interfaces /etc/network/interfaces')
ssh.exec_command('sudo cp /home/antidote/daemons /etc/frr/daemons')
ssh.exec_command('sudo cp /home/antidote/frr.conf /etc/frr/frr.conf')
ssh.exec_command('sudo systemctl restart frr.service')
ssh.exec_command('sudo ifreload -a')

scp.close()
ssh.close()



