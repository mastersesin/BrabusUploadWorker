import os
import threading
import time
import subprocess
import urllib
import uuid
import logging
import requests
import json

abs_plot_path = '/tmp1'
abs_tmp_upload_path = 'tmp_upload'
rclone_api_endpoint = ''
DRIVE_ID = '0ANV7vBguMi57Uk9PVA'
CREDENTIAL_URL = f'http://34.123.34.239:5000/credential?drive={DRIVE_ID}'
LOG_URL = 'http://34.123.34.239:5000/log'
rclone_template = """
[{}]
type = drive
scope = drive
token = {} 
team_drive = {}
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


def post_log(file_name):
    requests.post(LOG_URL, json={'file_name': file_name})


def upload_worker(file_name):
    logging.info('Upload worker started')
    credential = get_unused_credential()
    if not credential:
        logging.info('Can not get credential')
        return
    rclone_mount_name = str(uuid.uuid4())
    file_name_uuid = rclone_mount_name
    os.system('mv {} {}.csv'.format(
        os.path.join(abs_plot_path, file_name),
        os.path.join(abs_tmp_upload_path, file_name_uuid)
    ))
    os.system("echo '{}' >> {}".format(rclone_template.format(
        rclone_mount_name,
        credential,
        DRIVE_ID
    ), rclone_config_file))

    # Test drive
    logging.info('Start test upload session')
    command_return_obj_test = subprocess.run('rclone copyto {} {}:testdrive/{}.csv'.format(
        'upload.service',
        rclone_mount_name,
        str(uuid.uuid4())
    ).split(' '), capture_output=True)
    logging.info('Debug info: {}'.format(command_return_obj_test))
    if command_return_obj_test.stderr or command_return_obj_test.returncode != 0:
        logging.info('Test copy failed, reason {}'.format(command_return_obj_test.stderr.decode()))
        os.system('mv {} {}/'.format(
            os.path.join(abs_tmp_upload_path, file_name_uuid),
            abs_plot_path
        ))
        return

    # Main run
    logging.info('Start copy file {} and will be renamed to {}'.format(file_name, file_name_uuid))
    command_return_obj = subprocess.run('rclone --drive-chunk-size=256M copy {}.csv {}:backup/'.format(
        os.path.join(abs_tmp_upload_path, file_name_uuid),
        rclone_mount_name
    ).split(' '), capture_output=True)
    if command_return_obj.stderr or command_return_obj.returncode != 0:
        logging.info('Start copy file failed, reason {}'.format(command_return_obj.stderr.decode()))
        os.system('mv {} {}/'.format(
            os.path.join(abs_tmp_upload_path, file_name_uuid),
            abs_plot_path
        ))
    else:
        os.system('rclone config delete {}'.format(rclone_mount_name))
        os.system('rm -rf {}'.format(os.path.join(abs_tmp_upload_path, file_name_uuid)))
        post_log(file_name_uuid)


def main():
    logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s ')
    logging.info('Program started')
    count = 0
    while True:
        count += 1
        if count >= 300:
            logging.info('Checking folder {}'.format(abs_plot_path))
            count = 0
        for file in os.listdir(abs_plot_path):
            if file.endswith('.plot') or file.endswith('.csv'):
                logging.info('Found file {} - Starting new thread for uploading...')
                threading.Thread(target=upload_worker, args=[file]).start()
        time.sleep(2)


if __name__ == '__main__':
    main()
