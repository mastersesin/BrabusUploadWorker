import os
import subprocess
import time

# chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -n -1'
chia_plot_string = 'tmux new-session -d -s "myTempSession1" ./fastapi -t /tmp1/tmp/ -2 /mnt/ram/ -d /tmp1/ -r 32 -n -1 -c xch16p65jx63sv9gmwp5em263kdn847j2n3g8mxuk5mn2d0rcv4v62fsvzmdpy -f 841a65d12d40aeb595759e00ea68dde653d9c508a60c222ddb3915c1f67b04ffef7070c0bbe4349f1dd4b086e337a668'
while True:
    cm_check_status_code = os.system('pidof fastapi')
    print('return status code {}'.format(cm_check_status_code))
    if cm_check_status_code != 0:
        print('Start run fastapi')
        os.system("sudo rm -rf /mnt/ram/*")
        os.system("sudo rm -rf /tmp1/tmp/*")
        os.system(chia_plot_string + ' &')
    time.sleep(60)
