import time
import subprocess
import select
import os
import re
import telegram

filename = '/home/ty/.chia/mainnet/log/debug.log'
telegram_api_token = '1989791535:AAFFS4efdml_WehN6LwBXSnxRqtPbRG5X7Y'
telegram_channel_id = -584319866
bot = telegram.Bot(token=telegram_api_token)
os.system('/home/ty/start_chia.sh')
f = subprocess.Popen(['tail', '-F', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)
last_event_time = int(time.time())
while True:
    if int(time.time()) - last_event_time >= 10 * 60:
        os.system('/home/ty/stop_chia.sh')
        os.system('sudo reboot')
        last_event_time = int(time.time())
    if p.poll(1):
        data = f.stdout.readline().decode()
        if 'harvester chia.harvester.harvester: ERROR' in data:
            bot.send_message(
                chat_id=telegram_channel_id,
                text=f'{data}'
            )
        if 'harvester chia.harvester.harvester: INFO' in data or 'harvester chia.plotting.plot_tools: INFO' in data:
            last_event_time = int(time.time())
    time.sleep(0.01)