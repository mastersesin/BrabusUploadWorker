import os
import subprocess
import time

chia_plot_string = 'tmux new-session -d -s "myTempSession1" -n -1'

while True:
    cm_check_status_code = os.system('pidof fastapi')
    print('return status code {}'.format(cm_check_status_code))
    if cm_check_status_code != 0:
        print('Start run fastapi')
        os.system("sudo rm -rf /mnt/ram/*")
        os.system("sudo rm -rf /tmp1/tmp/*")
        os.system(chia_plot_string + ' &')
    time.sleep(60)
