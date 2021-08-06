import os
import uuid
import subprocess
import logging

gdrive_credential = ''
gstorage_credential = ''
gstorage_project_name = ''
gstorage_bucket_name = ''
root_gdrive_source_folder = ''
mount_endpoint_folder = ''
rclone_config_file = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]
rclone_gdrive_name = str(uuid.uuid4())
rclone_template = """
[{}]
type = drive
scope = drive
token = {} 
team_drive = 0AOZcGh-zmeBPUk9PVA
root_folder_id =
"""


def main():
    logging.basicConfig(level=logging.INFO, filename='app_upload_to_gcs.log', filemode='w',
                        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s ')
    logging.info('Program started')
    os.system("echo '{}' >> {}".format(rclone_template.format(
        rclone_gdrive_name,
        gdrive_credential
    ), rclone_config_file))
    os.system('rclone mount {}:{}/ {} --vfs-read-chunk-size 256M --transfers 16'.format(
        rclone_gdrive_name,
        root_gdrive_source_folder,
        mount_endpoint_folder
    ))
    for file in os.listdir(mount_endpoint_folder):
        if os.path.isdir(file):
            current_upload_folder_abs_path = os.path.abspath(file)
            command_return_obj = subprocess.run('gsutil -m cp -n {}/* gs://{}'.format(
                current_upload_folder_abs_path,
                gstorage_bucket_name
            ).split(' '), capture_output=True)
            if command_return_obj.stderr or command_return_obj.returncode != 0:
                print(command_return_obj)
            else:
                print(command_return_obj)


if __name__ == '__main__':
    main()
