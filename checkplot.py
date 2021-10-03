import os
import subprocess
import time

# chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -n -1'
chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -p a94a9f827a062a24d8f8c2201f9113fd8428da53deded15d501d8c94ed59e7d700b44bdc7e0e42a1501426fccca005b6 -f ac99a1d74615b16d12189e2b82a51e0640ca1aa38c55a5841f78c58ac448972555585c8295c181a0eaf6a6d9bf5f5d2d'
while True:
    cm_check_status_code = os.system('pidof fastapi')
    print('return status code {}'.format(cm_check_status_code))
    if cm_check_status_code != 0:
        print('Start run fastapi')
        os.system("sudo rm -rf /mnt/ram/*")
        os.system("sudo rm -rf /tmp1/tmp/*")
        os.system(chia_plot_string + ' &')
    time.sleep(60)
