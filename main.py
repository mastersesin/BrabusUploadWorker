import os
import threading
import time
import subprocess
import uuid
import logging
import requests
import json

abs_plot_path = '/tmp1'
abs_tmp_upload_path = 'tmp_upload'
rclone_api_endpoint = ''
CREDENTIAL_URL = 'http://207.244.240.238:5000/credential'
rclone_template = """
[{}]
type = drive
scope = drive
token = {} 
team_drive = 0AOZcGh-zmeBPUk9PVA
root_folder_id =
"""
rclone_config_file = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]


def get_unused_credential():
    json_response_obj = requests.get(CREDENTIAL_URL)
    if json_response_obj.status_code == 200:
        json_credential = json_response_obj.json().get('message').get('json_credential')
        return json.dumps(json_credential)
    else:
        return False


def upload_worker(file_name):
    logging.info('Upload worker started')
    rclone_mount_name = str(uuid.uuid4())
    os.system('mv {} {}'.format(
        os.path.join(abs_plot_path, file_name),
        os.path.join(abs_tmp_upload_path, file_name)
    ))
    os.system("echo '{}' >> {}".format(rclone_template.format(
        rclone_mount_name,
        get_unused_credential()
    ), rclone_config_file))
    os.system('mkdir {}'.format(rclone_mount_name))
    os.system('rclone mount {}:backup/ {}/ &'.format(rclone_mount_name, rclone_mount_name))
    time.sleep(1)
    os.system('cp {} {}/'.format(
        os.path.join(abs_tmp_upload_path, file_name),
        rclone_mount_name
    ))
    list_file = subprocess.check_output(['ls', rclone_mount_name]).decode()
    if list_file:
        list_file = list_file.split('\n')
        if file_name in list_file:
            os.system('rm -rf {}'.format(os.path.join(abs_tmp_upload_path, file_name)))
            logging.info('Upload worker ended')
        else:
            os.system('mv {} {}/'.format(
                os.path.join(abs_tmp_upload_path, file_name),
                abs_plot_path
            ))
            logging.info('File not in final destination')
    else:
        os.system('mv {} {}/'.format(
            os.path.join(abs_tmp_upload_path, file_name),
            abs_plot_path
        ))
        logging.info('Can not retrieve file in folder')
    os.system('sudo fusermount -u {}'.format(rclone_mount_name))
    os.system('rm -rf {}'.format(rclone_mount_name))


def main():
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s ')
    logging.info('Program started')
    count = 0
    while True:
        count += 1
        if count >= 30:
            logging.info('Checking folder {}'.format(abs_plot_path))
            count = 0
        for file in os.listdir(abs_plot_path):
            if file.endswith('.plot'):
                logging.info('Found file {} - Starting new thread for uploading...'.format(file))
                threading.Thread(target=upload_worker, args=[file]).start()
        time.sleep(2)


if __name__ == '__main__':
    main()
