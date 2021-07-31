import os
import threading
import time
import subprocess

abs_plot_path = 'tmp1'
abs_tmp_upload_path = 'tmp_upload'
rclone_api_endpoint = ''
rclone_template = """
[{}]
type = drive
scope = drive
token = {} 
team_drive = 0AOZcGh-zmeBPUk9PVA
root_folder_id =
"""
rclone_config_file = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]
_test_token = '{"access_token":"ya29.a0ARrdaM94I6iStenAgGOP8rQBAjGMCuh-y4bW3Iw5TWIjh6h45zcIkMmO4njNix6yj9ataN39YhS2iPFVcUaaOV133Mq5ZzzuqpEIBGyNVXfYdHB82DoZPb1p4bGFQ7mm8VkIRPuTk8Sv-lwWEUsTO32T0Ato","token_type":"Bearer","refresh_token":"1//0eMvj9NJFoWwDCgYIARAAGA4SNwF-L9IrAi8dWgNYy1QgnBgs-_W1euhrnwA4sV5rDTDC29qu5S8X0PnnQuGFpNLGKE1dhaohb9s","expiry":"2021-07-31T01:36:11.633096+07:00"}'


def upload_worker(file_name):
    print('Upload worker started')
    os.system('mv {} {}'.format(
        os.path.join(abs_plot_path, file_name),
        os.path.join(abs_tmp_upload_path, file_name)
    ))
    os.system("echo '{}' >> {}".format(rclone_template.format(
        'gdrive',
        _test_token
    ), rclone_config_file))
    os.system('mkdir gdrive')
    os.system('rclone mount gdrive:backup/ gdrive/ &')
    time.sleep(1)
    os.system('mv {} {}'.format(
        os.path.join(abs_tmp_upload_path, file_name),
        'gdrive/'
    ))
    print('Upload worker ended')


def main():
    print('Program started')
    while True:
        print('Checking folder {}'.format(abs_plot_path))
        for file in os.listdir(abs_plot_path):
            if file.endswith('.plot'):
                print('Found file {} - Starting new thread for uploading...'.format(file))
                threading.Thread(target=upload_worker, args=[file]).start()
        time.sleep(2)


if __name__ == '__main__':
    main()
