import os
import subprocess
import time
import uuid
import threading
import ast

import requests
import json
from uuid import UUID
import sqlalchemy
from bs4 import BeautifulSoup
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary, ForeignKey, REAL, Numeric, DateTime, DECIMAL, \
    BIGINT
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

gcs_credential = [
    {
        'email': 'riversweaver334569@gmail.com',
        'bucket': ['riversweaver334569', 'riversweaver334569_bucket2'],
        'json_credential': 'riversweaver334569.json'
    },
    {
        'email': 'cloud5@hoangyencuisine.com',
        'bucket': ['cloud5bucket1'],
        'json_credential': 'cloud5.json'
    },
    {
        'email': 'ty@nolivo.edu.vn',
        'bucket': ['nolivobucket'],
        'json_credential': 'tynolivo.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-1', 'ty-bucket-farm-2'],
        'json_credential': 'ty-bucket-farm.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-3', 'ty-bucket-farm-4'],
        'json_credential': 'ty-bucket-farm-acc2.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-5', 'ty-bucket-farm-6'],
        'json_credential': 'ty-bucket-farm-acc3.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-7', 'ty-bucket-farm-8'],
        'json_credential': 'ty-bucket-farm-acc4.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-9', 'ty-bucket-farm-10'],
        'json_credential': 'ty-bucket-farm-acc5.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-11', 'ty-bucket-farm-12'],
        'json_credential': 'ty-bucket-farm-acc6.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-13', 'ty-bucket-farm-14'],
        'json_credential': 'ty-bucket-farm-acc7.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-15', 'ty-bucket-farm-16'],
        'json_credential': 'ty-bucket-farm-acc8.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-17', 'ty-bucket-farm-18'],
        'json_credential': 'ty-bucket-farm-acc9.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-19', 'ty-bucket-farm-20'],
        'json_credential': 'ty-bucket-farm-acc10.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-21', 'ty-bucket-farm-22'],
        'json_credential': 'ty-bucket-farm-acc11.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-23', 'ty-bucket-farm-24'],
        'json_credential': 'ty-bucket-farm-acc12.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-25', 'ty-bucket-farm-26'],
        'json_credential': 'ty-bucket-farm-acc13.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-27', 'ty-bucket-farm-28'],
        'json_credential': 'ty-bucket-farm-acc14.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-29', 'ty-bucket-farm-30'],
        'json_credential': 'ty-bucket-farm-acc15.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-31', 'ty-bucket-farm-32'],
        'json_credential': 'ty-bucket-farm-acc16.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-farm-33', 'ty-bucket-farm-34'],
        'json_credential': 'ty-bucket-farm-acc17.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['bucket-new-1'],
        'json_credential': 'bucket-new-1.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-new-2'],
        'json_credential': 'bucket-new-2.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-new-3'],
        'json_credential': 'bucket-new-3.json'
    },
    {
        'email': 'ty@autonomous.nyc',
        'bucket': ['ty-bucket-new-4'],
        'json_credential': 'bucket-new-4.json'
    }
]

# iubackup_100@tnus.edu.vn
refresh_token = '1//0gZm80b5iTW6zCgYIARAAGBASNwF-L9IrOMN18s5teBDarxXD7WC5wfjUXvU_JhptJHHMd8HXLrFkvtjS17jYAcoiphv8QA0I5fE'
client_id = '560996391824-3es4jijjnqognc14l5c7t11cpqn3ib6n.apps.googleusercontent.com'
client_secret = 'AL5uJhH-4I5SDN36lwmsApY-'
gcs_credential_path = 'gcs_credential'
engine = create_engine('sqlite:///token.sqlite', echo=False)
Base = declarative_base()
# gcloud_exec = 'C:\\Users\\maste\\AppData\\Local\\Google\\Cloud_SDK\\google-cloud-sdk\\bin\\gcloud.cmd'
gcloud_exec = 'gcloud'


class Credential(Base):
    __tablename__ = 'credential'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    json_credential = Column(String, nullable=False, unique=True)
    last_used_time = Column(Integer, default=0)

    def __repr__(self):
        return '<Id: {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'json_credential': json.loads(self.json_credential),
            'last_used_time': self.last_used_time,
        }


Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.commit()


def list_bucket(bucket_name, _access_token, marker=None):
    return_list = []
    endpoint = f'https://storage.googleapis.com/?marker={marker if marker else ""}'
    headers = {
        'Host': f'{bucket_name}.storage.googleapis.com',
        'Authorization': f'Bearer {_access_token}',
    }
    try:
        xml_response = requests.get(endpoint, headers=headers).text
    except (requests.exceptions.ReadTimeout, TimeoutError, requests.exceptions.SSLError):
        return list_bucket(bucket_name, _access_token, marker)
    bs_content = BeautifulSoup(xml_response, 'lxml')
    marker_next_time = bs_content.find('nextmarker')
    return_list.extend([csv.text for csv in bs_content.find_all('key')])
    if marker_next_time:
        return_list.extend(list_bucket(bucket_name, _access_token, marker_next_time.text))
    return return_list


def get_file_warehouse_list(_access_token, _drive_id, _folder_id=None, _next_page_token=None):
    print('Start')
    final_list_csv_file = []
    endpoint = f'https://www.googleapis.com/drive/v3/files?corpora=drive&driveId={_drive_id}&includeItemsFromAllDrives=true&q=parents%20in%20%22{_folder_id if _folder_id else _drive_id}%22and%20trashed=false&supportsAllDrives=true&pageSize=1000&pageToken={_next_page_token if _next_page_token else ""}'
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    try:
        response = requests.get(url=endpoint, headers=headers, timeout=10)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        final_list_csv_file.extend(
            get_file_warehouse_list(_access_token, _drive_id=_drive_id, _folder_id=_folder_id,
                                    _next_page_token=_next_page_token))
        return final_list_csv_file
    if not response.status_code == 200:
        print(response.text)
        print('Cannot get file warehouse list')
        os.abort()
    list_file_with_full_info = response.json().get('files')
    print(len(list_file_with_full_info))
    next_page_token = response.json().get('nextPageToken')
    final_list_csv_file.extend(list_file_with_full_info)
    if next_page_token:
        next_list = get_file_warehouse_list(_access_token, _drive_id=_drive_id, _folder_id=_folder_id,
                                            _next_page_token=next_page_token)
        final_list_csv_file.extend(next_list)
        return final_list_csv_file
    return final_list_csv_file


def get_current_running_list(_gcs_credential, _json_path):
    final_list_csv_file = []
    for cre in _gcs_credential:
        if not cre:
            continue
        json_file_name = cre.get('json_credential')
        bucket_name_list = cre.get('bucket')
        return_code = 1
        while return_code != 0:
            return_code = os.system(
                f'{gcloud_exec} auth activate-service-account --key-file {os.path.join(os.path.abspath(os.getcwd()), _json_path, json_file_name)}'
            )
            print(return_code, 'Return code ne')
        for bucket_name in bucket_name_list:
            if not json_file_name:
                print(f'Something went wrong with obj {cre}')
                os.abort()
            while True:
                command_return_obj = subprocess.run(f'{gcloud_exec} auth print-access-token'.split(' '),
                                                    capture_output=True)
                if not command_return_obj.returncode == 0:
                    print(f'Something went wrong with get access token: {command_return_obj}')
                    continue
                _access_token_for_gcs = command_return_obj.stdout.decode().strip()
                final_list_csv_file.extend(list_bucket(bucket_name, _access_token_for_gcs))
                break
    return final_list_csv_file


def get_access_token_from_refresh_token(_refresh_token):
    endpoint_url = f'https://oauth2.googleapis.com/token?' \
                   f'client_id={client_id}&' \
                   f'client_secret={client_secret}&' \
                   f'refresh_token={_refresh_token}&' \
                   f'grant_type=refresh_token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        resp = requests.post(endpoint_url, headers=headers, timeout=1)
        _access_token = resp.json().get('access_token')
    except requests.exceptions.ReadTimeout:
        return get_access_token_from_refresh_token(_refresh_token)
    if not _access_token:
        return None
    return _access_token


def get_current_utc_timestamp():
    return int(time.time())


def insert_token_to_db(file_path):
    if not os.path.exists(file_path):
        print('Invalid path')
    for line in open(file_path, 'r'):
        if not line:
            continue
        json_credential, email = line.split()
        if '@' not in email:
            print(email, ' -> Incorrect format for email')
            os.abort()
        new_token = Credential(email=email, json_credential=json_credential)
        session.add(new_token)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError as err:
            session.rollback()
            print(err)


def create_new_drive(_access_token):
    endpoint_new_drive = f'https://www.googleapis.com/drive/v3/drives?requestId={str(uuid.uuid4())}'
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    drive_name = str(uuid.uuid4())
    try:
        response = requests.post(url=endpoint_new_drive, json={'name': drive_name}, headers=headers)
    except (requests.exceptions.ReadTimeout, TimeoutError, requests.exceptions.SSLError):
        return create_new_drive(_access_token)
    if not response.status_code == 200:
        print('Cannot create new drive')
        os.abort()
    print(f'Created drive id: {response.json()["id"]} with name: {drive_name} successfully')
    return response.json()['id']


def delete_temp_folder_in_temp_drive(_access_token, _folder_id):
    endpoint_delete_file = f'https://www.googleapis.com/drive/v3/files/{_folder_id}?supportsAllDrives=true'
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    try:
        response = requests.delete(url=endpoint_delete_file, headers=headers)
    except (requests.exceptions.ReadTimeout, TimeoutError, requests.exceptions.SSLError):
        return delete_temp_folder_in_temp_drive(_access_token, _folder_id)
    if response.status_code == 204:
        print(f'Delete temp folder {_folder_id} successfully')
        return True
    else:
        if response.status_code == 403:
            time.sleep(1)
            return delete_temp_folder_in_temp_drive(_access_token, _folder_id)
        print(response.text, response.status_code)


def delete_share_drive(_access_token, _drive_id):
    endpoint_delete_drive = f'https://www.googleapis.com/drive/v3/drives/{_drive_id}'
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    try:
        response = requests.delete(url=endpoint_delete_drive, headers=headers)
    except (requests.exceptions.ReadTimeout, TimeoutError, requests.exceptions.SSLError):
        return delete_share_drive(_access_token, _drive_id)
    if response.status_code == 204:
        print(f'Delete drive {_drive_id} successfully')
        return True
    else:
        if response.status_code == 403:
            time.sleep(1)
            return delete_share_drive(_access_token, _drive_id)
        print(response.text, response.status_code)


def move_file_from_root_to_share_drive(_access_token, _file_id, _old_drive_id, _new_drive_id):
    endpoint = f'https://www.googleapis.com/drive/v2/files/{_file_id}?addParents={_new_drive_id}&removeParents={_old_drive_id}&supportsAllDrives=true'
    headers = {
        'Authorization': f'Bearer {_access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.put(url=endpoint, headers=headers, data={}, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(response.text)
            print('Will retry')
            return move_file_from_root_to_share_drive(_access_token, _file_id, _old_drive_id, _new_drive_id)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        return move_file_from_root_to_share_drive(_access_token, _file_id, _old_drive_id, _new_drive_id)


def get_usable_token():
    cre_obj: Credential = session.query(Credential).filter(
        get_current_utc_timestamp() - Credential.last_used_time > 86400).first()
    if not cre_obj:
        return None
    cre_obj.last_used_time = get_current_utc_timestamp()
    session.commit()
    return cre_obj


def add_email_to_drive(_email, _drive_id, _access_token):
    endpoint = f'https://www.googleapis.com/drive/v3/files/{_drive_id}/permissions?supportsAllDrives=true'
    headers = {
        'Authorization': f'Bearer {_access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'role': 'organizer',
        'type': 'user',
        'emailAddress': _email
    }
    try:
        response = requests.post(url=endpoint, headers=headers, json=data, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(response.text, 'Will retry')
            return add_email_to_drive(_email, _drive_id, _access_token)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        return add_email_to_drive(_email, _drive_id, _access_token)


def get_list_drive(_access_token, _next_page_token=None):
    endpoint = f'https://www.googleapis.com/drive/v3/drives?pageSize=100&pageToken={_next_page_token if _next_page_token else ""}'
    list_of_all_drive = []
    headers = {
        'Authorization': f'Bearer {_access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url=endpoint, headers=headers, timeout=5)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        list_of_all_drive.extend(get_list_drive(_access_token, _next_page_token))
        return list_of_all_drive
    if not response.status_code == 200:
        print(response.text)
        print('Cannot get drives list')
        os.abort()
    list_max_100_drive = response.json().get('drives')
    next_page_token = response.json().get('nextPageToken')
    list_of_all_drive.extend(list_max_100_drive)
    if next_page_token:
        print(next_page_token)
        next_list = get_list_drive(_access_token, next_page_token)
        list_of_all_drive.extend(next_list)
        return list_of_all_drive
    return list_of_all_drive


def create_new_foler(_access_token, _new_drive_id):
    endpoint = f'https://www.googleapis.com/drive/v3/files?supportsAllDrives=true'
    headers = {
        'Authorization': f'Bearer {_access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [_new_drive_id],
        'name': 'upload'
    }
    try:
        response = requests.post(url=endpoint, headers=headers, json=data, timeout=5)
        if response.status_code == 200:
            return response.json().get('id')
        else:
            print(response.text, 'failed will retry')
            return create_new_foler(_access_token, _new_drive_id)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        return create_new_foler(_access_token, _new_drive_id)


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return True


def test_rclone(token, drive_id):
    rclone_abs_path = '/Users/macbook_autonomous/.config/rclone/rclone.conf'
    template = """
    [{mount_name}]
    type = drive
    scope = drive
    token = {token} 
    team_drive = {drive_id}
    root_folder_id =
    """
    os.system("echo '{}' >> {}".format(template.format(
        mount_name=drive_id,
        token=token,
        drive_id=drive_id
    ), rclone_abs_path))
    return_code = os.system(f'rclone ls {drive_id}:')
    if not return_code == 0:
        return False
    return True


access_token = get_access_token_from_refresh_token(refresh_token)
# '''test'''
# for i in range(500):
#     new_drive_id = create_new_drive(access_token)
#     add_email_to_drive('trantrongty160995@gmail.com', new_drive_id, access_token)
#     print('Done')
# '''test'''

# Our container INFO
root_folder_id = '15Zq3a-qVLR7pVGAA0y7KzBjV412O0FwQ'
root_drive_id = '0AEAzoWcdy4WDUk9PVA'

# IUBACKUP 1000
# root_folder_id = '1pIQUQ8PImM0N7zwyjlfDjJ9b0yzHAtuG'
# root_drive_id = '0ANV7vBguMi57Uk9PVA'
'''Main program'''
def cheat_worker(_access_token, _drive_id):
    global list_of_usable_drive
    global lock
    if len(get_file_warehouse_list(_access_token, _drive_id)) == 0:
        with lock:
            list_of_usable_drive.append(_drive_id)


list_drive = get_list_drive(_access_token=access_token)
list_of_usable_drive = []
lock = threading.RLock()
list_thread = []
for drive in list_drive:
    drive_id = drive.get('id')
    new_thread = threading.Thread(target=cheat_worker, args=(access_token, drive_id))
    new_thread.start()
    time.sleep(0.01)
    list_thread.append(new_thread)
    while len(list_thread) >= 10:
        list_thread = [running_process for running_process in list_thread if running_process.is_alive()]
        time.sleep(0.01)
    if len(list_of_usable_drive) >= 40:
        break
for thread in list_thread:
    thread.join()
list_of_usable_drive = list_of_usable_drive[:40]
list_file_warehouse = get_file_warehouse_list(
    _access_token=access_token,
    _drive_id=root_drive_id,
    _folder_id=root_folder_id,
)
list_file_hashed = {}
for file in list_file_warehouse:
    list_file_hashed[file['name']] = file
list_file_warehouse_name_only = list_file_hashed.keys()
list_current_running = get_current_running_list(_gcs_credential=gcs_credential, _json_path=gcs_credential_path)
intersection_list = list(set(list_file_warehouse_name_only).intersection(list_current_running))
print(len(list_current_running), 'Current running')
print(len(list_file_warehouse_name_only), 'File warehouse')
print(len(list(set(list_file_warehouse_name_only) - set(intersection_list))), 'Remain list len')
print(len(list_of_usable_drive),  'List usable drive must be 40')
input('Is number corrent ? press any key...')
next_step_info = []
for new_drive_id in list_of_usable_drive:
    intersection_list = list(set(list_file_warehouse_name_only).intersection(list_current_running))
    list_file_name_will_be_upload = list(set(list_file_warehouse_name_only) - set(intersection_list))[:50]
    list_current_running.extend(list_file_name_will_be_upload)
    new_folder_id_but_still_in_root_drive = create_new_foler(_access_token=access_token, _new_drive_id=root_drive_id)
    time.sleep(5)
    total_moved_file = 0
    status = False
    list_thread = []
    # while total_moved_file != 50:
    for file in list_file_name_will_be_upload:
        file_id = list_file_hashed[file].get('id')
        print(file_id)
        new_thread = threading.Thread(target=move_file_from_root_to_share_drive, kwargs={
            '_access_token': access_token,
            '_file_id': file_id,
            '_new_drive_id': new_folder_id_but_still_in_root_drive,
            '_old_drive_id': root_folder_id
        })
        new_thread.start()
        list_thread.append(new_thread)
    for thread in list_thread:
        thread.join()
    move_file_from_root_to_share_drive(
        _access_token=access_token,
        _file_id=new_folder_id_but_still_in_root_drive,
        _old_drive_id=root_drive_id,
        _new_drive_id=new_drive_id
    )
    while True:
        credential_obj: Credential = get_usable_token()
        add_email_to_drive(credential_obj.email, new_drive_id, access_token)
        if test_rclone(token=credential_obj.json_credential, drive_id=new_drive_id):
            break
        print('Token cannot use will try again')
    next_step_info.append({
        'id': str(uuid.uuid4()),
        'share_drive_id': new_drive_id,
        'rclone_token': credential_obj.json_credential
    })
    print('ok')
print(next_step_info)
write_upload_config = open('upload_config_new.txt', 'a')
write_upload_config.write('%s\n' % datetime.now())
write_upload_config.write(str(next_step_info[:20]) + '\n')
write_upload_config.write(str(next_step_info[20:]) + '\n')
write_upload_config.close()

'''SAU KHI UPLOAD THI CHUYEN FILE VE'''
# list_thread = []
# # list_drive = get_list_drive(_access_token=access_token)
# # list_drive_id = [drive.get('id') for drive in list_drive if is_valid_uuid(drive.get('name'))]
# upload_config = []
#
# list_drive_id = [x['share_drive_id'] for x in upload_config]
# for drive_id in list_drive_id:
#     print(drive_id)
#     list_folder_current_in_temp_drive = get_file_warehouse_list(access_token, drive_id)
#     folder_id = [x.get('id') for x in list_folder_current_in_temp_drive]
#     if len(folder_id) == 1:
#         folder_id = folder_id[0]
#         list_file_of_temp_folder_in_temp_drive = get_file_warehouse_list(access_token, drive_id, folder_id)
#         for file in list_file_of_temp_folder_in_temp_drive:
#             file_id = file.get('id')
#             new_thread = threading.Thread(target=move_file_from_root_to_share_drive, kwargs={
#                 '_access_token': access_token,
#                 '_file_id': file_id,
#                 '_new_drive_id': root_folder_id,
#                 '_old_drive_id': folder_id
#             })
#             new_thread.start()
#             time.sleep(0.01)
#             list_thread.append(new_thread)
#         for thread in list_thread:
#             thread.join()
#         delete_temp_folder_in_temp_drive(access_token, folder_id)
#     # delete_share_drive(access_token, drive_id)
#     print('move ok')

''' CHUYEN FILE VE ROOT FOLDER '''
# list_thread = []
# list_file_of_temp_folder_in_temp_drive = get_file_warehouse_list(access_token, '0ANV7vBguMi57Uk9PVA',
#                                                                  '1pIQUQ8PImM0N7zwyjlfDjJ9b0yzHAtuG')
# for file in list_file_of_temp_folder_in_temp_drive:
#     file_id = file.get('id')
#     new_thread = threading.Thread(target=move_file_from_root_to_share_drive, kwargs={
#         '_access_token': access_token,
#         '_file_id': file_id,
#         '_new_drive_id': root_folder_id,
#         '_old_drive_id': '1pIQUQ8PImM0N7zwyjlfDjJ9b0yzHAtuG'
#     })
#     new_thread.start()
#     time.sleep(0.01)
#     list_thread.append(new_thread)
#     while len(list_thread) >= 50:
#         list_thread = [running_process for running_process in list_thread if running_process.is_alive()]
#         time.sleep(0.01)
# for thread in list_thread:
#     thread.join()

'''NEU NHIEU QUA THI PHAI XAI CODE SAU DE CONVERT VE 1 LIST CHO LE'''
# return_list = []
# count = 0
# config_file = open('upload_config', 'r')
# for line in config_file:
#     if line.startswith('#Stop'):
#         break
#     if line.startswith('up xong'):
#         count += 1
#         line = line.replace('up xong ', '')
#         return_list.extend(ast.literal_eval(line.strip()))
# print(return_list)
# print('Total process line: {}'.format(count))
# config_file.close()
