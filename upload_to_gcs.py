import os
import time
import uuid
import subprocess
import logging
import json

gdrive_credential_list = [
    {
        'email': 'shalatuttle3233@gmail.com',
        'json_credential': {
            "access_token": "ya29.a0ARrdaM_9qDOt-h1ZsuZrjuEIRmRVYqfmozN04CVigRnwASPSFvjwpjxhsfliiFFSLBQ6zZAFwFnxd7oJSgZ3vKXNWaWsos3Sl60otbKmCWXKNmmCAnNsmnC29RPLWRr7UoKgkvkGQ6dMs5pizSUZiHdIOIzv",
            "token_type": "Bearer",
            "refresh_token": "1//0gSYDap7LN2QxCgYIARAAGBASNwF-L9IrWfGOqGulOuzpuWTtYm3G15I5_VUwKg4bzYxWDwlFbIex7R6TXozbiBR-iZur8QVRJEU",
            "expiry": "2021-08-07T19:29:16.382589+07:00"}
    }
]
gdrive_credential = {
    "access_token": "ya29.a0ARrdaM_9qDOt-h1ZsuZrjuEIRmRVYqfmozN04CVigRnwASPSFvjwpjxhsfliiFFSLBQ6zZAFwFnxd7oJSgZ3vKXNWaWsos3Sl60otbKmCWXKNmmCAnNsmnC29RPLWRr7UoKgkvkGQ6dMs5pizSUZiHdIOIzv",
    "token_type": "Bearer",
    "refresh_token": "1//0gSYDap7LN2QxCgYIARAAGBASNwF-L9IrWfGOqGulOuzpuWTtYm3G15I5_VUwKg4bzYxWDwlFbIex7R6TXozbiBR-iZur8QVRJEU",
    "expiry": "2021-08-07T19:29:16.382589+07:00"}
root_gdrive_source_folder = 'acc_3'
mount_endpoint_folder = root_gdrive_source_folder  # Usually the same as root_gdrive_source_folder
gstorage_bucket_name = 'cloud3bucket2'
rclone_config_file = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]
rclone_gdrive_name = str(uuid.uuid4())
rclone_template = """
[{}]
type = drive
scope = drive
token = {} 
team_drive = 0AKUkmbvSaV-CUk9PVA
root_folder_id =
"""


def main():
    logging.basicConfig(level=logging.INFO, filename='app_upload_to_gcs.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s ')
    print('Program started')
    os.system('mkdir {}'.format(mount_endpoint_folder))
    print('mkdir done')
    os.system("echo '{}' >> {}".format(rclone_template.format(
        rclone_gdrive_name,
        json.dumps(gdrive_credential)
    ), rclone_config_file))
    print('add rclone config done')
    os.system('rclone mount {}:{}/ {} --vfs-read-chunk-size 256M --transfers 16 &'.format(
        rclone_gdrive_name,
        root_gdrive_source_folder,
        mount_endpoint_folder
    ))
    print('mount done')
    input('press any key to continue')
    print('start search in {}'.format(mount_endpoint_folder))
    # for file in os.listdir(mount_endpoint_folder):
    #     print(file)
    #     if os.path.isdir(os.path.join(mount_endpoint_folder, file)):
    #         print('processing folder {}'.format(file))
    #         current_upload_folder_abs_path = os.path.abspath(os.path.join(mount_endpoint_folder, file))
    command_return_obj = os.system('gsutil -m cp -n {}/* gs://{}'.format(
        mount_endpoint_folder,
        gstorage_bucket_name
    ))
    # while True:
    #     line = command_return_obj.stdout.readline().rstrip().decode()
    #     print(line)
    #     if not line:
    #         break
    #     time.sleep(0.1)
    # for content in iter(command_return_obj.stdout.readline, b''):
    #     output = content.rstrip().decode()
    #     print(output)
    # command_return_obj = subprocess.run('gsutil -m cp -n {}/* gs://{}'.format(
    #     current_upload_folder_abs_path,
    #     gstorage_bucket_name
    # ).split(' '), capture_output=True)
    print(command_return_obj, 'Return code')
    # if command_return_obj.stderr or command_return_obj.returncode != 0:
    #     print(command_return_obj)
    # else:
    #     print(command_return_obj)


if __name__ == '__main__':
    main()
