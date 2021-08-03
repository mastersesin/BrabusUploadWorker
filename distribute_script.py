"""Sua lai ten cua NVME"""
import os
import time
import threading

import paramiko

STARTUP_SCRIPT = """
rm -rf run.sh
sudo systemctl stop upload.service
sudo apt-get update
sudo mkfs -t xfs /dev/nvme1n1
sudo mkdir -p /tmp1
sudo mount /dev/nvme1n1 /tmp1
sudo chmod 777 /tmp1
sudo mkdir /mnt/ram
sudo rm -rf /mnt/ram/*
sudo mount -t tmpfs -o size=110G tmpfs /mnt/ram/
mkdir /tmp1/tmp
mv /tmp1/BrabusUploadWorker/tmp_upload/*.plot /tmp1/
rm -rf /tmp1/BrabusUploadWorker
cd /tmp1
git clone https://github.com/mastersesin/BrabusUploadWorker.git
cd BrabusUploadWorker
sudo apt-get install -y python3-pip rclone
sudo pip3 install virtualenv
virtualenv venv
venv/bin/pip install -r requirements.txt
sudo cp upload.service /etc/systemd/system/
sudo systemctl start upload.service
"""

chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./chia_plot -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -c xch1xsjaqskkkq6hvlvvall4042jeqd3jygarsrdnmrua7wjjtt0k5fqn9w8aa -f 95999787516a65e3afdd55a583001b56e7ec371f83ceb47f412779ef43460d9cd0d7583b9c3e99fd961c9591b4f95070'

PEM_PATH = 'pem'
run_file = open('pem/ip_map_pem', 'r')
list_thread = []


def worker(paramiko_ssh_key, paramiko_connect_ip, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(paramiko_connect_ip, username='ubuntu', key_filename=os.path.join(PEM_PATH, paramiko_ssh_key))
    except paramiko.ssh_exception.AuthenticationException as e:
        print(e, paramiko_connect_ip, paramiko_ssh_key)
        return
    if command == '1':
        ssh.exec_command("echo '{}' >> run.sh".format(STARTUP_SCRIPT))
        ssh.exec_command("chmod 777 run.sh")
        stdin, stdout, stderr = ssh.exec_command('./run.sh', get_pty=True)
        for content in iter(stdout.readline, ""):
            print(content, end="")
        print('done {}'.format(paramiko_connect_ip))
    elif command == '2':
        ssh.exec_command("sudo pkill chia_plot")
        ssh.exec_command("sudo rm -rf /mnt/ram/*")
        ssh.exec_command("cd /tmp1/BrabusUploadWorker &&" + chia_plot_string)


input_command = input('1 run upload 2 run plot_chia')

for line in run_file:
    print(line.rstrip().split())
    ip, pem_name = line.rstrip().split()
    new_thread = threading.Thread(target=worker, args=[pem_name, ip, input_command])
    new_thread.start()
    list_thread.append(new_thread)
    time.sleep(0.1)

for thread in list_thread:
    thread.join()

print('done 2')
