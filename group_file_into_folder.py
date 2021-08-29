import os
import threading
from datetime import datetime

BIG_FOLDER_PATH = '/home/ty/gdrive/backup/'
ROOT_FOLDER_PATH = '/home/ty/gdrive/'


def move_file(file_abs_path, destination_abs_path):
    print('Start copy <{}> to <{}>'.format(file_abs_path, destination_abs_path))
    os.system('mv {} {}'.format(file_abs_path, destination_abs_path))


list_file = []
list_thread = []
for file in os.listdir(BIG_FOLDER_PATH):
    if file.endswith('.csv'):
        list_file.append(file)
        if len(list_file) == 50:
            destination_folder_name = '{}'.format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
            print('Create folder {}'.format(destination_folder_name))
            os.system('mkdir {}'.format(os.path.join(ROOT_FOLDER_PATH, destination_folder_name)))
            for f in list_file:
                t = threading.Thread(target=move_file,
                                     args=[
                                         os.path.join(BIG_FOLDER_PATH, f),
                                         os.path.join(ROOT_FOLDER_PATH, destination_folder_name, f)
                                     ])
                t.start()
                list_thread.append(t)
            for t in list_thread:
                t.join()
            list_file = []
