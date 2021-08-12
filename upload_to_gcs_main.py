from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'cloud4bucket1'
RUN_CONFIG = [
    {
        'email': 'jaleesajacques9260',
        'rclone_token': '{"access_token": "ya29.a0ARrdaM8xJ-2AXyuG0ylL_BlLtLpZR5JMzVrPIZ0LkBxvrG2zeFzXENBIhDS3j5OrmduVtKzxuMf-_HeNbHbiWyiytplmmvuOr4gKeL1Dz33RqN6OwMq6z_u07FKqajh7ZQpFty2uqvOXm_A93V6q7l4F3IDZ", "token_type": "Bearer", "refresh_token": "1//0eUBGe1xgJhKgCgYIARAAGA4SNwF-L9IrVWfdT1W21HjlHRqnPlzzsnt3quSwPuFCl8vinYqLqO5P2Rn9t-XW6bName2R0K0L3G4", "expiry": "2021-08-06T02:38:29.581661+07:00"}',
        'share_drive_id': '0AIhcAHFef3fpUk9PVA',
        'folder_name': '10_08_2021_05_51_14'
    },
    {
        'email': 'talialindy8465',
        'rclone_token': '{"access_token": "ya29.a0ARrdaM84Nx5gBgeDM-E3K6otyjTJHxl5z_bd5Xh04O9C_vNh9gGeH3E7wA9xh5CiAHSCe3YyuMF9rsXGMl0V6N9wZfRWBggDH49fvesPOH_tYRILBPdvpQe9vibxjdkcb-3-tOmlnS4I1OQ51C_LdYmjKhWQ", "token_type": "Bearer", "refresh_token": "1//0euarHcHqtMcHCgYIARAAGA4SNwF-L9IrCD1DnYRxZHQ5mmw4ZrnUyDsI1ia5ezKdwT6p5BzOIglAjO2sOhhu9znn364UHhNJNjU", "expiry": "2021-08-06T02:39:09.632909+07:00"}',
        'share_drive_id': '0AIhcAHFef3fpUk9PVA',
        'folder_name': '10_08_2021_05_52_59'
    },
    {
        'email': 'natoshaoscar9451',
        'rclone_token': '{"access_token": "ya29.a0ARrdaM-VrtTE0SbQWCYn7hVlHlGC_biPh1iT2qZPUu7ORVB_hzZAGYnA4VvmG4jff5dRWjv3l7L29KJce_dHmUd1lfQzSFi_8A5na3R4EfhmPBrp6qbMvBn8cEi4p9eOpKoalrh0HGltXqiSy2mo-rxKXqrS", "token_type": "Bearer", "refresh_token": "1//0eMy5H6r2Qo3nCgYIARAAGA4SNwF-L9Ir9QyUnSOkzsdvThiScHTbSXrPUDfn82kJtaSahvt7ups4ZJChguTpM3iqtAc9xgW30wg", "expiry": "2021-08-06T02:48:47.134532+07:00"}',
        'share_drive_id': '0AKUkmbvSaV-CUk9PVA',
        'folder_name': '10_08_2021_06_01_07'
    },
    {
        'email': 'jacklynjessica9808',
        'rclone_token': '{"access_token": "ya29.a0ARrdaM-LQNRPL3lO9ERs0RMhCAqZp2i9IqKz0eFKyw8OkqNWgbquPz0kqvpy5FPeqHqEV1GDVy4U4NpaTHf-fnNd3r1hrV2KA4FQ_ZNvTyApcOt6f3Y-KYQwZaP03S8mZTs1upVUSAhU1ag4ZxEpwxKd9vA1", "token_type": "Bearer", "refresh_token": "1//0e8ZwCpl_vtkaCgYIARAAGA4SNwF-L9IrMYBsf369PLKj7CuTWQ8BxoPjFt-C0qfVWF7zcDIGCMxUgwLQ6mbxTNo_MdbyBqfqigA", "expiry": "2021-08-06T02:42:54.304903+07:00"}',
        'share_drive_id': '0AKUkmbvSaV-CUk9PVA',
        'folder_name': '10_08_2021_06_03_17'
    },
]
PROCESS_COUNT = 16

RCLONE_TEMPLATE = """
[{mount_name}]
type = drive
scope = drive
token = {token} 
team_drive = {drive_id}
root_folder_id =
"""
RCLONE_CONFIG_ABS_PATH = subprocess.check_output('rclone config file'.split()).decode().split('\n')[1]


def process(abs_file_path):
    os.system('python3 upload_to_gcs.py {} {}'.format(abs_file_path, BUCKET_NAME))


def mount_drive_disk(rclone_mount_name, token, drive_id, folder):
    os.system("echo '{}' >> {}".format(RCLONE_TEMPLATE.format(
        mount_name=rclone_mount_name,
        token=token,
        drive_id=drive_id
    ), RCLONE_CONFIG_ABS_PATH))
    cm = os.system('mkdir {}'.format(rclone_mount_name))
    if cm != 0:
        os.system('fusermount -u {}'.format(rclone_mount_name))
    os.system(
        'rclone mount {}:{}/ {} --vfs-read-chunk-size 256M --transfers 16 &'.format(rclone_mount_name, folder,
                                                                                    rclone_mount_name, ))


if __name__ == "__main__":
    processes = []
    for config in RUN_CONFIG:
        mount_drive_disk(config.get('email'), config.get('rclone_token'), config.get('share_drive_id'),
                         config.get('folder_name'))
        current_process_path = os.path.join(CURRENT_EXEC_PATH, config.get('email'))
        while len(os.listdir(current_process_path)) == 0:
            print('List dir not updated yet wait 1 sec')
            time.sleep(1)
            continue
        if os.path.exists(current_process_path):
            for file in os.listdir(current_process_path):
                print(file)
                if file.endswith('.csv'):
                    print(file)
                    p = Process(target=process, args=(os.path.join(current_process_path, file),))
                    processes.append(p)
                    p.start()
                while len(processes) >= PROCESS_COUNT:
                    processes = [running_process for running_process in processes if running_process.is_alive()]
                    time.sleep(0.01)
            for p in processes:
                p.join()
        else:
            print('{} not existed'.format(current_process_path))

# for file in os.listdir():
#     if os.path.isdir(file):
#         print(file)
#         os.system('chia plots add -d /home/ty/cloud3bucket2/{}'.format(file))
