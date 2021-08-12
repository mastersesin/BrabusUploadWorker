import os
import subprocess
import time

chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./chia_plot -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -c xch1xsjaqskkkq6hvlvvall4042jeqd3jygarsrdnmrua7wjjtt0k5fqn9w8aa -f 95999787516a65e3afdd55a583001b56e7ec371f83ceb47f412779ef43460d9cd0d7583b9c3e99fd961c9591b4f95070'

while True:
    cm_check_status_code = os.system('pidof chia_plot')
    print('return status code {}'.format(cm_check_status_code))
    if cm_check_status_code != 0:
        print('Start run chia_plot')
        os.system("sudo rm -rf /mnt/ram/*")
        os.system("sudo rm -rf /tmp1/tmp/*")
        os.system(chia_plot_string + ' &')
    time.sleep(60)
