"""Sua lai ten cua NVME"""
import os
import time
import threading

import paramiko

STARTUP_SCRIPT = """
rm -rf run.sh
sudo systemctl stop upload.service
sudo apt update && sudo apt install mdadm --no-install-recommends
yes | sudo mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/nvme0n1 /dev/nvme0n2
sudo mkfs.ext4 -F /dev/md0
sudo mkdir -p /tmp1
sudo mount /dev/md0 /tmp1
sudo chmod 777 /tmp1
sudo mkdir /mnt/ram
sudo rm -rf /mnt/ram/*
sudo mount -t tmpfs -o size=110G tmpfs /mnt/ram/
mkdir /tmp1/tmp
sudo chmod 777 /tmp1/tmp
mv /tmp1/BrabusUploadWorker/tmp_upload/*.plot /tmp1/
rm -rf /tmp1/BrabusUploadWorker
cd /tmp1
git clone https://github.com/mastersesin/BrabusUploadWorker.git
cd BrabusUploadWorker
git checkout 150tr2
sudo chmod 777 /tmp1/BrabusUploadWorker
sudo chmod 777 /tmp1/BrabusUploadWorker/tmp_upload
sudo chmod 777 /tmp1/BrabusUploadWorker/fastapi
sudo apt-get install -y python3-pip rclone
sudo pip3 install virtualenv
virtualenv venv
venv/bin/pip install -r requirements.txt
sudo cp upload.service /etc/systemd/system/
sudo systemctl start upload.service
sudo cp checkplot.service /etc/systemd/system/
sudo systemctl start checkplot.service
"""

STARTUP_SCRIPT_2 = """
sudo systemctl stop upload.service
cd /tmp1/BrabusUploadWorker
git checkout .
git fetch
git checkout 150tr
git pull
sudo chmod 777 fastapi
sudo systemctl stop checkplot.service
sudo systemctl start checkplot.service
sudo systemctl start upload.service
"""

# chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -c xch1xsjaqskkkq6hvlvvall4042jeqd3jygarsrdnmrua7wjjtt0k5fqn9w8aa -f 95999787516a65e3afdd55a583001b56e7ec371f83ceb47f412779ef43460d9cd0d7583b9c3e99fd961c9591b4f95070'
# chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -p a94a9f827a062a24d8f8c2201f9113fd8428da53deded15d501d8c94ed59e7d700b44bdc7e0e42a1501426fccca005b6 -f ac99a1d74615b16d12189e2b82a51e0640ca1aa38c55a5841f78c58ac448972555585c8295c181a0eaf6a6d9bf5f5d2d'
chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -n -1'

PEM_PATH = 'pem_credential'
# run_file = open('{}/pem_map_ip.txt'.format(PEM_PATH), 'r')
list_thread = []


def worker(paramiko_connect_ip, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(paramiko_connect_ip, username='ty', key_filename='/Users/macbook_autonomous/.ssh/id_rsa',
                    passphrase='ckiuzk4ever')
    except paramiko.ssh_exception.AuthenticationException as e:
        print(e, paramiko_connect_ip)
        return
    if command == '1':
        ssh.exec_command("echo '{}' >> run.sh".format(STARTUP_SCRIPT))
        ssh.exec_command("chmod 777 run.sh")
        stdin, stdout, stderr = ssh.exec_command('./run.sh', get_pty=True)
        for content in iter(stdout.readline, ""):
            print(content, end="")
        print('done {}'.format(paramiko_connect_ip))
    elif command == '2':
        ssh.exec_command("sudo pkill fastapi")
        ssh.exec_command("sudo rm -rf /mnt/ram/*")
        ssh.exec_command("sudo rm -rf /tmp1/tmp/*")
        ssh.exec_command("cd /tmp1/BrabusUploadWorker &&" + chia_plot_string)
    elif command == '3':
        stdin, stdout, stderr = ssh.exec_command('sudo systemctl is-active upload.service', get_pty=True)
        for content in iter(stdout.readline, ""):
            print(content, end="")
        stdin, stdout, stderr = ssh.exec_command('sudo pidof fastapi', get_pty=True)
        for content in iter(stdout.readline, ""):
            print(content, end="")
    elif command == '4':
        ssh.exec_command("mv /tmp1/BrabusUploadWorker/tmp_upload/*.plot /tmp1")
        ssh.exec_command("cd /tmp1/BrabusUploadWorker && git pull")
        ssh.exec_command("sudo systemctl restart upload.service")
        # ssh.exec_command("cd /tmp1/BrabusUploadWorker &&" + chia_plot_string)
    elif command == '5':
        # ssh.exec_command("sudo systemctl stop upload.service")
        # ssh.exec_command("sudo systemctl stop checkplot.service")
        # ssh.exec_command("mv /tmp1/BrabusUploadWorker/tmp_upload/*.plot /tmp1")
        # ssh.exec_command("cd /tmp1/BrabusUploadWorker && git checkout . && git pull && sudo chmod 777 fastapi")
        ssh.exec_command("cd /tmp1/BrabusUploadWorker && sudo chmod 777 fastapi")
        # ssh.exec_command("sudo systemctl start upload.service")
        # ssh.exec_command("sudo systemctl start checkplot.service")
    elif command == '6':
        ssh.exec_command("echo '{}' >> run.sh".format(STARTUP_SCRIPT_2))
        ssh.exec_command("chmod 777 run.sh")
        stdin, stdout, stderr = ssh.exec_command('./run.sh', get_pty=True)
        for content in iter(stdout.readline, ""):
            print(content, end="")
        print('done {}'.format(paramiko_connect_ip))


# input_command = input('1 run upload 2 run plot_chia 3 check upload / fastapi 4 restart upload 5 special')
#
# for line in run_file:
#     try:
#         if line.startswith('#'):
#             continue
#         print(line.rstrip().split())
#         ip, pem_name = line.rstrip().split()
#         new_thread = threading.Thread(target=worker, args=[pem_name, ip, input_command])
#         new_thread.start()
#         # list_thread.append(new_thread)
#         time.sleep(0.1)
#         if input_command == '1' or input_command == '3':
#             new_thread.join()
#     except ValueError:
#         continue
#
# # for thread in list_thread:
# #     thread.join()
#
# print('done 2')
# worker('34.136.116.157', '1')
# worker('34.132.15.59', '1')
a = '''34.133.244.8
35.225.253.138
34.66.59.92
23.251.153.221
34.67.90.112
34.122.151.186
104.197.107.65
34.68.132.115
34.69.84.40
104.155.165.65
35.194.42.151
35.226.229.188
35.192.191.7
34.134.20.248
34.68.30.247
34.123.79.10
35.238.86.96
34.68.32.127
34.71.56.116
34.68.177.172
34.72.149.30
34.135.54.211
35.188.130.13
34.135.129.153
34.68.7.167
34.132.67.156
34.69.168.97
35.232.126.60
104.154.180.198
35.238.129.116
35.193.218.210
34.133.193.64
34.67.248.31
35.192.157.20
35.188.69.2
35.224.11.41
35.226.69.109
35.238.217.141
34.134.248.113
34.71.34.37
34.66.26.49
34.132.239.65
34.66.70.19
35.224.44.100
34.134.24.100'''
a = a.split('\n')
for ip in a:
    worker(ip, '1')
