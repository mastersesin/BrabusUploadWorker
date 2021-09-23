import os
import subprocess
import time

# chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -n -1'
chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -c xch16ndcj6hew6a69tcn6h7dtrj744gd60mzp78hl70lr2047lnrnzdq7z8s5c -f 8c9db573edff069681e522055e35ded4f289f556de80dd8b96d2b6e403757faf6edb819b32c8ac9601df03c691ec4659'

while True:
    cm_check_status_code = os.system('pidof fastapi')
    print('return status code {}'.format(cm_check_status_code))
    if cm_check_status_code != 0:
        print('Start run fastapi')
        os.system("sudo rm -rf /mnt/ram/*")
        os.system("sudo rm -rf /tmp1/tmp/*")
        os.system(chia_plot_string + ' &')
    time.sleep(60)
