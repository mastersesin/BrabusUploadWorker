from multiprocessing import Process, Queue
import os
import time
import subprocess

CURRENT_EXEC_PATH = os.getcwd()
BUCKET_NAME = 'nolivobucket'
RUN_CONFIG = [
    {
        'email': 'id1',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM81b6k61sUGsTrO_aMZcow9yCTbqfoSBg3jFCIpYbidV-I4UiVr0hADhEraFNyoW05JWxBq2rlyeDd8FeRp0UXGIwW41vlgotgXfCBCGRbotwOQp5kHRzI7SdvKqGUVbVr0k6Xv9Ao0_bkp8xOim3yp","token_type":"Bearer","refresh_token":"1//0e1hMO-vPoNuoCgYIARAAGA4SNwF-L9IrEO6TpW0pABAUhQdc8Hh5INBIqL0xCOBNBm1YgpS2WWRbESD2XIiF77_jcs1tf6whyr4","expiry":"2021-08-18T11:59:13.3059316+07:00"}',
        'share_drive_id': '0AJlOCO3IjHM_Uk9PVA'
    },
    {
        'email': 'id2',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM_IQGIZf97-IME-4lqYvoXTyUtOZUPDR3Llui0_CAPyfzEjStLQlE-ESEwXKNG_ZtBrNrxrpObshMH31ziYK2sMZXDDyt_V2rfxnVwiwJ1YgJvm2MiLXWew1yo5KanFzEOcFe98409VtaQdi7oMm_Fv","token_type":"Bearer","refresh_token":"1//0e3BBrH3T-VDzCgYIARAAGA4SNwF-L9IrmIIh0AbVo7pZ4ISjVUAMOtAG9Fh4vS53Yr3dJ-t7YsqjHZ19MNBZhQV3A--OmVF-218","expiry":"2021-08-18T11:59:53.242003+07:00"}',
        'share_drive_id': '0AN_TOTL83hyDUk9PVA'
    },
    {
        'email': 'id3',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM9aVE7GF4F7IuXsMGnTddcXhtE7_wvULR1TFcDx-5bMAE0iQcUgZ2LA0RrFeNU-HZ_4Jxmmpqv5q01W2CaInxaP6pcw_9Q7qw1ZOJvAClTF09btSo_gJHIBHX0on6cd6H5FO6Q-qzHC8efb0CcNcMCg","token_type":"Bearer","refresh_token":"1//0eloNuycLMcl1CgYIARAAGA4SNwF-L9Ir_AmxD4YSy5TZHdJQEjb2tEKyptaHdZFkhA3MuJJFD-2PEVS8KeyuqXmx43czoI7bmQ0","expiry":"2021-08-18T13:54:31.3438449+07:00"}',
        'share_drive_id': '0AK0q1Uag3cwRUk9PVA'
    },
    {
        'email': 'id4',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM-eG5S7Wc1sBocyzXUHqPG_FV95nWGRz_aBdaaK0sgpDyMAFtrmXYnmi3NrQiwIwjeBPn7BV8IvostcnHauGwCzq1Jg-6_7wfXhrYdZ_sHCv0eeBUh5UHv7aNHP3ek4JM_VhCT0NnOjez0HBmVvSQw4","token_type":"Bearer","refresh_token":"1//0ewO_r_LmLiZ3CgYIARAAGA4SNwF-L9Ir0rdf1gA2b-9M_uaOGyf0mSzWoX2VQ4Uto0cUX_kA7x_PYXiZ7m945amWrZDbIDGsEtY","expiry":"2021-08-18T13:55:01.5199214+07:00"}',
        'share_drive_id': '0AJDtaOmOdPQTUk9PVA'
    },
    {
        'email': 'id5',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM-Uhf0Dj0tQXiF_ZNb91wQ13PrdyEeOcYOSotGNOtiLRowDGI2EpC_AVJ4986PGo-Kx8tJUyFIJc7an2X20B0YtxBO82frumIkGSQsNlfGE6kMPGfk1WV89VSI1lNK2FtClWSDYREDBI_cNQkFAZe2a","token_type":"Bearer","refresh_token":"1//0ejDBVRHZAebMCgYIARAAGA4SNwF-L9Iri7zHmFMcAn8WwvYeD6ngWU5efdlK8Xswh4zwzTx_a_R6q3_44V5FT200x1EtRnTcJ-8","expiry":"2021-08-18T13:55:40.3651032+07:00"}',
        'share_drive_id': '0AEHdnWLtSRFBUk9PVA'
    },
    {
        'email': 'id6',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM_f06giFgOEWG3yZCzLvID8Wwfbxj7GpDTE5HSscQPLWrR7ekodV2YP2p9BCW-1s0XwFGKZMlPwTgL8RBRHdv2iHisoO1Xd3NaT4UrHjnd-XjNrTnhwwea61WUFHPClBtidWPD-2wOcj0AdLk1-urv_","token_type":"Bearer","refresh_token":"1//0ecLQZ2gDlptDCgYIARAAGA4SNwF-L9IrRr8NYnrsr9Vd1f-EbVxCkrOVg49663miK86_g5x_PJjZSqzuAQanxqPNy9ciY9o5nC8","expiry":"2021-08-18T13:56:08.2776252+07:00"}',
        'share_drive_id': '0AAS-uinMbL61Uk9PVA'
    },
    {
        'email': 'id7',
        'rclone_token': '{"access_token":"ya29.a0ARrdaM_d6sNLBPuYN48YpRMq5c1fHWiC3HPcv6PUnOMT2XB-qqPxBXRMWmD4hhxGFELWUTbvwJB8ArY39GmKIkqBRUAKvK8M9nsZBGQSo1-Rs8cmTV3y-Mr3jN9G_eN7X5zqE7cUR3Cxi12SDSgYgNyNA6tA","token_type":"Bearer","refresh_token":"1//0ebpvkqAY4PpACgYIARAAGA4SNgF-L9IrllrFxGmlyfnlNuGLmT9RWVIT1Jq6IupFrs3fruF6O4QPosWTbLrV9AEuc4mih8QowQ","expiry":"2021-08-18T13:57:34.9289244+07:00"}',
        'share_drive_id': '0ALVnDA8bSdc_Uk9PVA'
    }
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


def mount_drive_disk(rclone_mount_name, token, drive_id):
    os.system("echo '{}' >> {}".format(RCLONE_TEMPLATE.format(
        mount_name=rclone_mount_name,
        token=token,
        drive_id=drive_id
    ), RCLONE_CONFIG_ABS_PATH))
    cm = os.system('mkdir {}'.format(rclone_mount_name))
    if cm != 0:
        os.system('fusermount -u {}'.format(rclone_mount_name))
    os.system(
        'rclone mount {}: {} --vfs-read-chunk-size 256M --transfers 16 &'.format(rclone_mount_name,
                                                                                 rclone_mount_name, ))


if __name__ == "__main__":
    processes = []
    for config in RUN_CONFIG:
        mount_drive_disk(config.get('email'), config.get('rclone_token'), config.get('share_drive_id'))
        current_process_path = os.path.join(CURRENT_EXEC_PATH, config.get('email'))
        while len(os.listdir(current_process_path)) == 0:
            print('List dir not updated yet wait 1 sec')
            time.sleep(1)
            continue
        if os.path.exists(current_process_path):
            for folder in os.listdir(current_process_path):
                print(folder)
                for file in os.listdir(os.path.join(current_process_path, folder)):
                    if file.endswith('.csv'):
                        print(file)
                        p = Process(target=process, args=(os.path.join(current_process_path, folder, file),))
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
