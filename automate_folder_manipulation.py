import os
import subprocess
import time
import uuid
import threading

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


def get_list_drive(_access_token):
    endpoint = f'https://www.googleapis.com/drive/v3/drives?pageSize=100'
    headers = {
        'Authorization': f'Bearer {_access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url=endpoint, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json().get('drives')
        else:
            print(response.text)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        return get_list_drive(_access_token)


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
# list_file_warehouse = get_file_warehouse_list(
#     _access_token=access_token,
#     _drive_id=root_drive_id,
#     _folder_id=root_folder_id,
# )
# list_file_hashed = {}
# for file in list_file_warehouse:
#     list_file_hashed[file['name']] = file
# list_file_warehouse_name_only = list_file_hashed.keys()
# list_current_running = get_current_running_list(_gcs_credential=gcs_credential, _json_path=gcs_credential_path)
# intersection_list = list(set(list_file_warehouse_name_only).intersection(list_current_running))
# print(len(list_current_running), 'Current running')
# print(len(list_file_warehouse_name_only), 'File warehouse')
# print(len(list(set(list_file_warehouse_name_only) - set(intersection_list))), 'Remain list len')
# input('Is number corrent ? press any key...')
# next_step_info = []
# for i in range(40):
#     intersection_list = list(set(list_file_warehouse_name_only).intersection(list_current_running))
#     list_file_name_will_be_upload = list(set(list_file_warehouse_name_only) - set(intersection_list))[:50]
#     list_current_running.extend(list_file_name_will_be_upload)
#     new_drive_id = create_new_drive(access_token)
#     new_folder_id_but_still_in_root_drive = create_new_foler(_access_token=access_token, _new_drive_id=root_drive_id)
#     time.sleep(5)
#     total_moved_file = 0
#     status = False
#     list_thread = []
#     # while total_moved_file != 50:
#     for file in list_file_name_will_be_upload:
#         file_id = list_file_hashed[file].get('id')
#         print(file_id)
#         new_thread = threading.Thread(target=move_file_from_root_to_share_drive, kwargs={
#             '_access_token': access_token,
#             '_file_id': file_id,
#             '_new_drive_id': new_folder_id_but_still_in_root_drive,
#             '_old_drive_id': root_folder_id
#         })
#         new_thread.start()
#         list_thread.append(new_thread)
#     for thread in list_thread:
#         thread.join()
#     move_file_from_root_to_share_drive(
#         _access_token=access_token,
#         _file_id=new_folder_id_but_still_in_root_drive,
#         _old_drive_id=root_drive_id,
#         _new_drive_id=new_drive_id
#     )
#     while True:
#         credential_obj: Credential = get_usable_token()
#         add_email_to_drive(credential_obj.email, new_drive_id, access_token)
#         if test_rclone(token=credential_obj.json_credential, drive_id=new_drive_id):
#             break
#         print('Token cannot use will try again')
#     next_step_info.append({
#         'id': str(uuid.uuid4()),
#         'share_drive_id': new_drive_id,
#         'rclone_token': credential_obj.json_credential
#     })
#     print('ok')
# print(next_step_info)

'''SAU KHI UPLOAD THI CHUYEN FILE VE'''
list_thread = []
# list_drive = get_list_drive(_access_token=access_token)
# list_drive_id = [drive.get('id') for drive in list_drive if is_valid_uuid(drive.get('name'))]
upload_config = [{'id': '374f26e2-2181-44f2-9a62-920f9ef1a261', 'share_drive_id': '0ACoHxbA2vM9GUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM83rGBsfthd_tHwDybhSkuVTgVLtbbh-rWks1xVXLbQHtc_6twos_kPZvauz7i6kXLlWTBVqaZnMnrEwsfQWQ0BE9gChsLIp7A1dSfv47zfQBEuUP_NY-UMibVLzERkBMHyeRaQHZ3fYU58YxnBDJOB","token_type":"Bearer","refresh_token":"1//0eXc9O-5LGRYSCgYIARAAGA4SNwF-L9Irzv63eyKpFIvnxmPMsQmJrDbOxIQKkCGIu0gITLS4dbmFu9V4nxNSpvJvOzrpxjPetGg","expiry":"2021-08-18T17:09:01.060212+07:00"}'}, {'id': '1f757f20-aefe-4fda-9ad1-df3eecc614ca', 'share_drive_id': '0AE8Kxt__87u5Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9zrF50bcGhdeuWAvRRJEO5ZM61lzehi8AWC4OjB0_u5MoGUYJ7YSU7oRAvYUXrR-4PSDYBf2NstwFLuCex2Hg7DjNjQ8tJcH5Sxvu5mr9vb5HG-iDEiNmSRMBo-Zs8m-JV_yQiryciYOJBWeJNcoiI","token_type":"Bearer","refresh_token":"1//0ezerN70_pVwmCgYIARAAGA4SNwF-L9IrBfzmGJ5ASniP4USz_cv2mNqBtTIxPYszPABQbBPaXRzZqW5QlTBvIDvtY32LP1MQEGM","expiry":"2021-08-18T17:09:22.7154214+07:00"}'}, {'id': '66fe8dd9-4b11-4d91-a70c-b29654e6f4fc', 'share_drive_id': '0AKbVQU2bgDzJUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--zeLJT4-kBrOBfMa9iaTBnbinp3aSJUP4m5uWDjfa3bE7JpD95q_T_a8DwCcIJ9b44A1h_9kf65sqDLjbyJxwSaNk9lYzEi8SuDKdpzSYwXTuD9LnPVkv37p4ItTd5GiT9DyQrMrP6_krXl-lWAbT","token_type":"Bearer","refresh_token":"1//0eQ2o_SSVeJkXCgYIARAAGA4SNwF-L9IrCV6Ru0ieKqPjNxWXn_2DdqDw7x_JgTpE6FJ_BvbhUoURduuZhMzwsNHTf0_jXhxejcA","expiry":"2021-08-18T17:10:40.9805559+07:00"}'}, {'id': '158be2e1-af15-4ffd-a3a6-e7237e48114c', 'share_drive_id': '0AHhwDK9TQic0Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM__nI-NMeb-bsjWBYzwre2I3lES1DVy0zTlmt0atyQEtFTSXEeU56UsnIPBn1p8uy5rFfvwq4an8pRtkGN9_7CRLJv1Mx7levaF-EikgXDnpJZqEkwpOdldBEGsn8KTJTLyegZ-pPKvS9GpsGzALNiB","token_type":"Bearer","refresh_token":"1//0eeJQKm_8z0nbCgYIARAAGA4SNwF-L9IrXiR4O9d3au2XbPFLVZNT2idnCkJaE7H_RhG_Wma8fGSCCqeLs7hYciF77hy-KlMzFsc","expiry":"2021-08-18T17:11:42.9804571+07:00"}'}, {'id': 'e733b5b2-b58b-4e78-ac0d-d8945b628112', 'share_drive_id': '0AN99C1QIbJY-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM81-ZmL8fin4EewUn6G5Xc93UkxEZD9QYAyKRN-6nLUjRdfRhyQWOvWXvCLtYhXDDsEQqWSLYhqalOgBNlbuO7BgygaUMOQDk0quWghqo-RDm5NVPtCdrN3Y9TWtfKkxALyAlowqRuhG4BXve1LnNR8","token_type":"Bearer","refresh_token":"1//0eS092QphmL_KCgYIARAAGA4SNwF-L9IrLH9xyDbpZS_IukstadyMx-zjz0iQ8u4nzSrq09M5lnXkgeJUupZi-0YseAcbtYZ4mfw","expiry":"2021-08-18T17:13:08.9709639+07:00"}'}, {'id': '4c78a44d-5f66-4438-9671-c0c6db815d66', 'share_drive_id': '0AJmdsB6n_EPVUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_mCNeZWg_zLjclJCAiJIfLgZ4TuopH0E0mobELAFFGWFXco1YMOZkw9kSrJtqXVYrxG6nmQGlXZynhZti7UbAhkle-mt8j8IbPkyvcnttVkjXm_GAYcAZV3AlopoJt5swenqNraOBWQiKbrHpDRT-m","token_type":"Bearer","refresh_token":"1//0e0bjqZQY27OvCgYIARAAGA4SNwF-L9IrlRjrWZmxbOI3Km-Y63JjnFDrokvgeaPE0iLo8bfA3LqSnsNo336ZaFMWWB2yMBfQHis","expiry":"2021-08-18T17:13:27.8124851+07:00"}'}, {'id': '4b47135c-80be-48cd-847c-b49814f06905', 'share_drive_id': '0AG-LajvFdLJxUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jfJnUGQF4CJTurPdVGly_daDvhBYpM2sSA_hCOsoESJC1nV1dG8OLyR9UsV2KrZNuS_RvjJNEPBWfmQFQNdXEK0dvG8iZrP6KpVYeDqpN5bvmBjiuWkEqXatn2K7OLpi9XzCK4cxJNKjxa7BXGdwE","token_type":"Bearer","refresh_token":"1//0eq7uwybdJC3ICgYIARAAGA4SNwF-L9IryNB90qcxPAP31qSm1qb7qhkqLnFRMN0IbRuIS9MPe_ETN1Sfkqa8R5loK86eX0VlhEo","expiry":"2021-08-18T17:13:48.4306399+07:00"}'}, {'id': 'b021fe25-23e7-45b1-a92e-9e9914fa8a25', 'share_drive_id': '0APb_vZaF9uZgUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9_nTBHKgwDsuD5Uf1tU2XT4RVJgl69XY2mFnBacMlQNqgspNF7AST-U9kHpX6jA31pQpZtA4X8exnCcfpW42zzycOeBd9j1ikKq_jDRCQFBII2j2eiVGocOw2bics_2qDgI-icGorCKs8qJXBubgZX","token_type":"Bearer","refresh_token":"1//0eWvN9_rEfR5ZCgYIARAAGA4SNwF-L9IrjvIawyopz6gZiBJOr_WPXbT4M2EF0xBtC0rgSsxEsjIW4nHxS_vvED8Ne_GaKflplNI","expiry":"2021-08-18T17:14:19.4152946+07:00"}'}, {'id': '508ed835-9c88-428f-90d9-dfa08075b225', 'share_drive_id': '0ADsafunP4Gh_Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_zarkw7Bt9pENn8MM7lNE3nIIuENgplHkSbahghGrMt8XL-eo6ZLVEJoVB1i981MwUZ8WFCFQj_jtLOvPfLmCqgRoa25mObVO6QhzXwsGDMR1sMen7l4tkFR8tiN06YsXPxxUK3cj-xFw_mjc6Yv5G","token_type":"Bearer","refresh_token":"1//0eUfjmKVps1DkCgYIARAAGA4SNwF-L9IrGgrvhzjc83rxnej3ZRNmE-7UzITH_uW3dhQ0EvYAAvIr7NFW0xp5qGAb81y_X2LV7eg","expiry":"2021-08-18T17:14:41.0008994+07:00"}'}, {'id': 'a240ce8d-bd2a-4813-b6e2-d0b241f47464', 'share_drive_id': '0ACm8DaZdXJWIUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8YVGPTsdIMIEo3mjc2og5yrVf-eV7xwDBi3mPbbMLg7W9MT_fe2nyv6x5Q1H65B4rUqw5FzNewHHV5dx4ebHP4QLxJhaqIc_-9D6dzqXYv3lvJf-qjXVnQkQeHyvwVTT7YJImX1derffjyimy368qo","token_type":"Bearer","refresh_token":"1//0e6ICRrJyIB_SCgYIARAAGA4SNwF-L9IrGps_H2ZWMJXq_FBLBgbnaRZGFxyoS3HKYV6qeiYQtr9UOO9DksUbC3N5Kv0pPdwFHTI","expiry":"2021-08-18T17:15:10.7685593+07:00"}'}, {'id': '45c35de6-c3d5-4eeb-b472-6f11e8e30c42', 'share_drive_id': '0AOx94rft0l7YUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9oT7tu99iQnxk46v4xmtSVwPrc_9DesPa3zbOaDhwLqVWRMTPoYOa4DoLm96sagtpIkza8VAYmGINBRb-QUiRKn4OBRyLp0DH5u1QZPynyTk3mq4z51MRE_qUEaw_6X9Y7Tao6LqFv7CR56eIbSoBV","token_type":"Bearer","refresh_token":"1//0eUS3_lRcDZueCgYIARAAGA4SNwF-L9Ir1POcGYoBI2cohQwQ_mEa7aBR_v2WWjz7YJ-i11QdaHPPf7G2CGdMtcfYlwGDyVsV9BM","expiry":"2021-08-18T17:15:29.7602277+07:00"}'}, {'id': '71327269-60a4-4811-a60b-0a69cc1a6a30', 'share_drive_id': '0AOFtWO9LtTpKUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_ptUfbPqsLyZaR8csGx2DO_Sjkb0c6t9hYa2ni0pIc9JBk_p46zpImIUOqGVZjkOZVgqKfdCMuMJRIHLWXivOlzaYbkeM2EL57JCyI9qkgFO_CdG9JWElBrni2ffovq8TVCWHeMPdcoU_fUD8__gp3","token_type":"Bearer","refresh_token":"1//0exGpvFIhqvKTCgYIARAAGA4SNwF-L9IrA57tMM4U6X9NnKk62bobojXJD9gs-2yNSqrW5Iuoz1DauWdRUBiYmf3MA5uSfCmPQcQ","expiry":"2021-08-18T17:16:04.4758921+07:00"}'}, {'id': '78e91713-84a4-4674-ac80-69436768779e', 'share_drive_id': '0AA87GSHUhzSMUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-W1Qp9UIcWMOdBkljIAmyxEI6_LGR8BO2GQFoZrA9faWnWH9qCHJoY0Ga1V9od3Kd6Hr7YO5j9Pg2Yv66_kBCRAB3PRylr7rOzNboC6d1llSesxyiC5lrQvIbcAkp45VWRFX_7sH1UzFpsj1iOs19W","token_type":"Bearer","refresh_token":"1//0eLb2iwfBjsfXCgYIARAAGA4SNwF-L9Ir24pvRSggyw7qPpsKSENu6LZ-eOUHDvnBCxXPwOatoIy1byclOzHvu4TgJzSg3jxdCRA","expiry":"2021-08-18T17:16:24.6688511+07:00"}'}, {'id': 'ff24468c-d28e-48c3-9608-9fd35370812b', 'share_drive_id': '0AKUA0ry1fM5oUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-ADv8GPeMpqTdHSvag_c_3sC1dSuLddmEegEppk91_ThiHr-GyKjDF3Hx87JyZqp_9dF6IJQxqJXMaH1zXYXDgRl4it-YZARyzA2LSEsfLKXX_dYyZu2i5xU8aD8I-zkC3Jsp_HJyW0VAIGXlyS_BL","token_type":"Bearer","refresh_token":"1//0eO_o6DAYdU1rCgYIARAAGA4SNwF-L9IrN3cF7TBbTpmM4nvVSIeIn0Dc0PYMxaJ2Zucc39RpN4kBfpyHy6DVHYZ-nDCeSueRoao","expiry":"2021-08-18T17:17:27.2714651+07:00"}'}, {'id': '75f3509c-f178-4b21-b30d-796544fd3551', 'share_drive_id': '0AL3x-9ghVmFTUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM92xlsnrDTUxO3--ai9OPODdK0rfsgWMZhCLNvQ6FhsL-2cSird4aDgDlnYesrTc_E6cn6NAyIVwxLcKpmuZkGXHJtprsA3q2M0j_NpW07LbRYLyOvIk0srm4_QoPnL3OM0PnkQMu7P05WPpYirHz4l","token_type":"Bearer","refresh_token":"1//0eXHipw8yPfRBCgYIARAAGA4SNwF-L9Irnp7l0xl44yAsoJNkgXa6voKsiCmke6pU7vmD759eaQCm8umTzFcmPCFc8ef5sBqgPIQ","expiry":"2021-08-18T17:18:19.1370732+07:00"}'}, {'id': '58772bba-4c67-4173-899b-33d1fcdb32b2', 'share_drive_id': '0ADzIoW_M9pwOUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_iI0HSzWKmpYpi34J4rtiQGNJQ_MV9WXXXVrUd4HARiP7OJGAFF54kP3xg4rT9fDXX9Hh83vj159WhlU3ihSZVe7BqIXEJSnZOlAs8PdXkw64dhaWTiti3v8KSEKZG9rEb10S5vT4vLmNG-KNjoZmH","token_type":"Bearer","refresh_token":"1//0eMBiwcAx3oe4CgYIARAAGA4SNwF-L9IrutpwPzzUrRuN3OGwaUopoImGNeEE_dg1lH2gH6r1vdlFJdpADlz5ioveAW0Hejy4Llo","expiry":"2021-08-18T17:18:38.2274354+07:00"}'}, {'id': '777ee8e1-d097-4c72-a9b1-9d701c122bf8', 'share_drive_id': '0ANSKWOKHgOZQUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_k4AqH7sspkEbcBfUx1K0-wrOP1YsYcyGKFi1rsLvA7uTDnWvfU62Yqx9R3zxQiWmqB0E9-scwTS-WmRBsbRd8FHmqR69d50wwxPhu9ydUaM88QyOahFfK6fcPUmWyRR1yEnSsmiHuKPVYz7TLpD8T","token_type":"Bearer","refresh_token":"1//0e1G7Pr9B4GHSCgYIARAAGA4SNwF-L9Ir_sgxioAmhefj5RWya_k1gGhVot7NXNjZ46D2nMgMRQNfccLfTmbfGJKMBefZ8gkuVlI","expiry":"2021-08-18T17:19:00.8618839+07:00"}'}, {'id': 'f9b55721-2172-49c2-9ccf-a94f0f938f2b', 'share_drive_id': '0AFwUDtQYzoS-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_DmGVkI0nUbikL7PLRirvH_jG6WZXVBTUtP6yX1GNqR3KPhtBd-zrWpIZ6EeNU6u-8EVeYUplLm7F6nzmdUyDYdKzxl1w_6E2T8Wy69UIqrRsqktqmrO336sMiaWJB25g8xjXBI9a5qs6dRBLkyphk","token_type":"Bearer","refresh_token":"1//0ec95Hg2dmDK3CgYIARAAGA4SNwF-L9IrzeE4kdMaTNTt_fKXC5Ebp7vSnuqLgNbQN4T8h87URhN3cW9hqKsb3oqzp-cL0eUIafM","expiry":"2021-08-18T17:19:21.2346434+07:00"}'}, {'id': 'c5c4ca34-bb26-4e2d-bb2a-dc998c52a559', 'share_drive_id': '0AHy7E9N5CVLTUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--bGIhKgYpzcZ7wmprY_G-BCq9JpNQ6t7sS71nK65EF5KpDWbXwvXEO02Tdx3ZA-Vdm9xBv2o3MdoHY6NM-Q95AvHMc2ztzrdzo7UGyweglqobeFgTTmsp9oypGP0ciXHZZKyyLT29Aw548BlZhEir","token_type":"Bearer","refresh_token":"1//0eQqpvCkgyTbeCgYIARAAGA4SNwF-L9Ir9k7VWWVsyukJIzmoQiY7tLHfxYQN5O-J4IEzyfcoKuh6bEiv1h6gJgcV-BDZ-K3O3ks","expiry":"2021-08-18T17:20:03.7286143+07:00"}'}, {'id': 'f1e9aa02-4661-4dbe-be42-75373cf2937c', 'share_drive_id': '0AOg9myvjuSz7Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-lsPOC8n4PYxYm7zk84n-EMtnXCPK80e6vpgrxM6czX-kDy42-e5SG6BPSBJCg9RXVSGAOEMHcy_HklONnsA2VAJ0niwoxVNkS6ZcNBlVl5WRxpuDys1HaNdSOeewM4fqqR8Dh0KVsRc3ElzwGeQei","token_type":"Bearer","refresh_token":"1//0ebH6CGURI_swCgYIARAAGA4SNwF-L9IrFAvjtDaW9s6cm1Q34ShoGhZvpbBm8XAlwDG8sUAIphZVy5zuAv4XYYiob_OyEDBZAko","expiry":"2021-08-18T17:20:25.5556227+07:00"}'}, {'id': '025f8514-fa0e-4162-8a61-4d0ac5248d1c', 'share_drive_id': '0AMTeToi8M4xSUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_AE2Mcx59esDDa9bdfRVFBg9_36c3uepAqsP9ru_cJI0eLVA8XDY7_xhiUK35mnd2FFRRFA-EIs-76QUx-LKV6ct1UAwIDzC5Pqy6uTr-8JH0fuT0O4CR2vIB0nqv4c-57XaucatgrTOjKsRAgIf_b","token_type":"Bearer","refresh_token":"1//0eOdyQEE0lTMjCgYIARAAGA4SNwF-L9Ir9ors4-GDwKE0HF7hKyqZ4qym3PqJshoySXXbKAMw82OEZf1buXBGr8clIjngkr3dUdQ","expiry":"2021-08-18T17:20:55.122884+07:00"}'}, {'id': '11deeaf3-b4c7-4b00-9c54-daa6eac2c1da', 'share_drive_id': '0AKpNQiG7RV0KUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8aqIIMZ7rKjIlDvuZZJCkCLpoUPl4f9Tk6s00UT9KKzPjvvlLcg_nQ3IQfjJ088wL_tFYyp3hgJP71MSBIwdm0gASa3PcWQ6bi7fGx00Jj84uUVHdDCr4hYD-DQttFw2US08ZTz3vPBUQmGkN7RqYg","token_type":"Bearer","refresh_token":"1//0ejRWbAxohOl1CgYIARAAGA4SNwF-L9IrZ9VzQEDlU0VuJpfGWcQsecY8aKoEW5cOZ6Tv5Eq2qNDd5OKGHD3MUp9D5-tYAr5v1wQ","expiry":"2021-08-18T17:21:13.4333271+07:00"}'}, {'id': '77bb5f7d-9248-4b99-8653-7d2fd6aef9dc', 'share_drive_id': '0AEjK2Q2kk8WmUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_7j2Ck193G3nDHccxAc1j6BtyWd3ncOwyWsiJUIu08NIxv_5Yyl58VHDiICoUeATggG6BJVuH3YtaG7mmVpupZ30pfewdT6dog0N3ERCw8i-qj-HdJKBLgGkJpF2JS5r-cM4BoqdlECeJEdtgK5sDV","token_type":"Bearer","refresh_token":"1//0erabMG6qvP3uCgYIARAAGA4SNwF-L9Ir4AZTAuEDE72oi0C3nZF9xYR0ZnI_wiYcBVIQYYUwUpjuHuJ1h6-_rPP3TUoqye_zyXk","expiry":"2021-08-18T17:21:36.3898538+07:00"}'}, {'id': '51bbf739-08a4-4921-92a0-3ed83dd38d4b', 'share_drive_id': '0AOYILWsJ3xHaUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM99fvNwep80mjSq7E1dsmQ0WLSLOAhvC51LgyMcLlWDl12wV2QemdxQtfA-qqRs0sbq-UjA08bQlQzx_LYVtAL3LXh515h6JzdXfhlCuqFkxYADUxl7Ekp3nD6Om223vxhDKuwWaetI2O6sxlAYbK9D","token_type":"Bearer","refresh_token":"1//0eu-qdyZRbHtLCgYIARAAGA4SNwF-L9IrcaindKOUnc33p0YDLNi_dOrgSbgXkkTPj0sCAGYJD3ZJrPqJFq3apg7UbDWxo4cSeHk","expiry":"2021-08-18T17:22:08.0501874+07:00"}'}, {'id': '0bf56be3-bd5b-4c4f-8fe9-d50c44c83e3a', 'share_drive_id': '0AKQoJMa-J8kSUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM84PAotvR0Q0NF82pZ6H7tvP6RUlwkwNEP2qFsmrsgAvKTc0hURkxOqKQ2UqdqOgI-YsA3gBmi5VOihAJDtT8yxsVyDfLNqtNFZJ0Jn7pCcoWXyaxnTitHuq-795lE-mFoM4ojP_FS_WdgUNsfjXH68","token_type":"Bearer","refresh_token":"1//0esh32Mjf2HHiCgYIARAAGA4SNwF-L9IrHjG9nItmqN0kmi7gFukPOGlMYkyiXfN_caiEAAjCICHOTvpMQ8VTM4LnPPVjkdJgu-M","expiry":"2021-08-18T17:22:26.3790485+07:00"}'}, {'id': '7c17475b-81d4-4b18-b748-7b2f99b0c817', 'share_drive_id': '0AKelepGXpI7MUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8keoBPBzeTP60FV5z7kZps8lTFpV1JSfqwjVxc4Cj-5I-gbIlZbatI2V9ClYkogqdTjabT6PxJ7aD0fok3AP8wgO1AOjx8HqLh5Xwh62qYuT4I5mG5T7iKTtqTpnIotSkc-rO5rbQgj-63GQ-xaaH2","token_type":"Bearer","refresh_token":"1//0eUfKpsEOlXtACgYIARAAGA4SNwF-L9IrCRygqxeR5jL3KZy2BGw7Clv9ngrWlrxEtq3MiUArw80OcInziIAYAgv5Vujv1JL5S8A","expiry":"2021-08-18T17:23:07.7111659+07:00"}'}, {'id': 'b4cb13ab-d238-407e-a643-71846d8c3907', 'share_drive_id': '0APU0jojEyRgbUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8WGJHRCaYyZkc1-pFW1-xs7WIDhd2NZaoIN81CzMjKFiZ-4UcIAwbJEH1OqDnhtLOJX_R7GoCr5RO4IibmSwQV84Z5ps3qv_Apda0685tfYkcT6rdRnQ91xRmfGDUpA0CZDWkVFJfKPHjMU2hMxqtC","token_type":"Bearer","refresh_token":"1//0eeJQGX2PlpH3CgYIARAAGA4SNwF-L9IrRxfDgWIMR4dyl49IIHH2jU0c0Y5_TT5_jK4Qzv9DZCxAX_NLd0jvyVOcvVrTgbvJ6bs","expiry":"2021-08-18T17:23:26.2277692+07:00"}'}, {'id': 'a5d84a3f-a7df-49b0-ba05-3b72a833cdda', 'share_drive_id': '0AFg5hzErB9O-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8aGEpNCeZfHogjP6vAHYD-OOOZvpNmSSWKH6u-c5j1nuYVCQ6kGVVhBPlVMaKQ4ku_e321Oj1LZAN4WkLMMwN7FWVnUDnLG9xx7bwhmj4ixAY6d0g8jLN4k2K6KHqWxbDbZ5jEI6ipnYhvvwy3idbT","token_type":"Bearer","refresh_token":"1//0e2FatRlAznF-CgYIARAAGA4SNwF-L9Ir4XdPoyZPPWRHi3uLGsBulI655XVVbhEtnPZfpqCbgra204wMUV6kbB3vcQAZE-SI1-E","expiry":"2021-08-18T17:56:56.8318587+07:00"}'}, {'id': '600705fd-aeeb-4bd7-ae22-0343cbc857a3', 'share_drive_id': '0AHELjUkICADiUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-2kd09_0533BTxgDDIriNd4fVQ2vO1uGs35GjF3azNx4KOZiD9AutrIQ_uNL8ZLhgSZsz025w5KPfrkc7SdiF_ELM9PJ1VARb7K4-kNH0OvKG6wAn0k9b5xoC1g8ZTyLT3Q1UH-lYPS9vVYPfb0_Zq","token_type":"Bearer","refresh_token":"1//0edsTopwc4QTACgYIARAAGA4SNwF-L9Ir5vJVKbMBZEXGjCUrPiHXi1_Yj1PJ23NibqgwVp4OSu8NaVrR18U1TfqtKWPnoO1K_so","expiry":"2021-08-18T17:57:15.2236298+07:00"}'}, {'id': 'b998a702-63a8-4089-8f4b-230a45ae516f', 'share_drive_id': '0AIbLldLhF4uIUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8N3MY4gNFF7e5ZArwitg001n9PDGskpsQ_mPz5FTx32U1wpSQs_J3Q9qEQGIFsq0ZsBxCIC1IfTU51B2ELC0036hdxiitrNmSMX0C1uuKKX4TMTWRKrFNZOjAh4MeAEsPazndfkA8IWtZ17CcNE1qy","token_type":"Bearer","refresh_token":"1//0eXrq1QFoSd-WCgYIARAAGA4SNwF-L9IrMsJTIvSkg3cLGXnWKLVj463sryfZ68Vynjisp9HoSqFthZhEoAqXjasgdl8PQaDPugw","expiry":"2021-08-18T17:57:34.3791653+07:00"}'}, {'id': '931779ca-3d85-41d6-a5e9-a44a189c276b', 'share_drive_id': '0AGmhrnElUmvcUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_qNyN6KfOfRh21pzdOWSgaICYXewuugiNUt0P_xYxx-ETXBOjpb99H2OAAsn6TQMEEBaslgyHI3LFl5V_QoG1fVsEe3gHGiPehknO3MXBhmpXGpWGTctZHV3eLQRw-GzJBvqIMlvUwNW4VYhbd6c77","token_type":"Bearer","refresh_token":"1//0em5ScwfPRXdxCgYIARAAGA4SNwF-L9Ir5FfPiURD6eec1hs9rsEfA5xPhNYM10y0yEvQSvziGM6jb2XFDva0yHl6U0PtyCUsi3E","expiry":"2021-08-18T17:57:52.9130138+07:00"}'}, {'id': '2e8d5d7b-d67e-440c-9724-c5f63a337663', 'share_drive_id': '0ABiULzKgfxnPUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_UcyUK79hZrzzxaEx3lQSx8vTlxIXOiiTYlXhcb9b138b-I_naUxP9aeTHTtgzaM1_HkQILNlwIyKHrkjJO0SLtHz5Oa4hJp-KUm7dfteKXNk1cxHFTWw_xGxC2g3_iJ7q9bPmUlNviJ3Kvthp1DrI","token_type":"Bearer","refresh_token":"1//0eK-OaoKoMk8HCgYIARAAGA4SNwF-L9IrYg1jREs2A0svmWtDnrkLYtac_IhY-VV7x8RVeSUvR_jRw22riYYymlyyNE-CRBNzFKs","expiry":"2021-08-18T17:58:12.325797+07:00"}'}, {'id': '25c2fe0e-f255-49dd-8e7d-5a085906f2e0', 'share_drive_id': '0AAvlHna7PmzJUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-1iC4f01NIQoZDHJeKiRL3fU486au-XTeD2v9TTvMOPb4b75JaZyO2s4GNdZdQy2OfQmxOu2Q1vYBDXlBGBSS0BZIu1x8BwqQcIM7DUIfdh40gmymQAjeHOUyAzwDtMCujWdGJ6ljYQGLWNxD8RNeG","token_type":"Bearer","refresh_token":"1//0eqB-OEuq2KkxCgYIARAAGA4SNwF-L9IroJov-avKSLou-A4hOfrwIbFt05HaOFBJxorIr7pGRYA209EoWYR9LKLfleg1exctMUo","expiry":"2021-08-18T17:58:51.1117722+07:00"}'}, {'id': '8903d772-d591-47c2-8f15-4a1aad6374b6', 'share_drive_id': '0AL4L7lfDbFCMUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM87tYyrsbxelZ94XD8nhm0xiDqQZN8xftJJ3f0OsffzODiMdR9ZJsuts6UgowFhh1mldLwQ3RF0TMVeIuhZIMGaef3D-k6oxwoZWWPmmyLJlrhxwdxh_kLaYpGVgaG3wxWODmpYuXdc3fAf9iLObI-h","token_type":"Bearer","refresh_token":"1//0ejyaJWyzJS5XCgYIARAAGA4SNwF-L9IrRt5sh3glYPkEwgRu6e_iUJXEXh2Gp1NJtgwvfR_AP0Ids0A0e5SkLvo8OtxRgd36GwM","expiry":"2021-08-18T17:59:10.1335999+07:00"}'}, {'id': 'fcce7a3d-460e-45b6-91cd-4beef80a64a7', 'share_drive_id': '0ANNL2hQyVjRRUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM85TGhx5MdhmHTaiySWB5rwgohNJeuLkpdq3YTBE97h_ga6AijJzbBi66AntYC8UeNCOQarWbLOJJLcZMffbSzdl10-EbUazC3t_vWtu6boIK1LZmXyqjm4exnnJF6bCSRYs7uzSEityJyz3nBbdsrY","token_type":"Bearer","refresh_token":"1//0eCRrGrMf-8nPCgYIARAAGA4SNwF-L9Irvj6DEnJUI0zQhhF4LMNEb0AeX_FAt-xnDJjHiM1waW3YdluIBc11gHpj6emEmQ1ibn8","expiry":"2021-08-18T17:59:28.9706329+07:00"}'}, {'id': '70d79fe0-846a-4ffe-9e16-317720d5b7cd', 'share_drive_id': '0AB3tTHFtG9vnUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM87XxrJrz7_ojW34LR6aW8aXWhklnwALz-Y1cZEboUKvWOrPtxKJW6uh5IPHW5EXSd_JVxcJEqLV744Qi-VFsnmURHoXor8m_0lKNu1XkIj-UE11-QkxD_VNnG4NxXRznna-QXweQbfCu_1TMu5QsfQ","token_type":"Bearer","refresh_token":"1//0erxTF2vWEm5uCgYIARAAGA4SNwF-L9IrGzPFGRq1PwtzpIa5Pdrgb390oPMpufgCKmqbneHBPJR5OAzAa3a1DxNR9NL6ndUw28g","expiry":"2021-08-18T17:59:54.3118044+07:00"}'}, {'id': 'e08c299b-210a-4083-8b58-bca430588f8c', 'share_drive_id': '0APAQcwkUnZLXUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_vJqgIhh0USGARXKL-82nuMTxn8Y50iq-KxrzbsTdBGnGoGOhwyT97YXXUWXGFt6wyiXOVc0hlk20VwRngrbKCwmjuEZsledIUfLPU_eI96PnVcZ-shjxcj-CYCGM4zAp-KCza_3-6c5ecfWIWKw1l","token_type":"Bearer","refresh_token":"1//0es-blbjS1cUjCgYIARAAGA4SNwF-L9IrF8z5T3YmbhnB91QQljCRmU7jEgaX4xYMZ8Tp2lwYb44IW7dsYFucDXF3S7t8jo8ST_0","expiry":"2021-08-18T18:00:13.3013895+07:00"}'}, {'id': 'e70027f8-3c4b-431b-be06-a6e4f1e38025', 'share_drive_id': '0AFgTgFqYZQ1nUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9bo7CfFWEKwor2amK-SJLb7S5n5TpNbAC_w56x-xpBaxr19f9r8fyka3Ae0_aKlCgakh0S7-VhM2Jufz5NtHQc4s0ok61kbVACLblGdc1TzzMO01DSRhAHDaZlLenWQa-0HfoVmXkxdHKMdMU6je9O","token_type":"Bearer","refresh_token":"1//0eF68Vfsh-UkfCgYIARAAGA4SNwF-L9Iru_M2torazBh13a49Gbcta4vlV3wE0pvJHtGURt31aM7_dZEMjWF9MYjFy1WD6IUN9HI","expiry":"2021-08-18T18:00:32.1397908+07:00"}'}, {'id': 'ad9fc518-e01c-4785-a6ca-0f25675ee554', 'share_drive_id': '0AFrRTvoccauUUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_22OprNPEAbsxe2cGBQtzWqNwdrvveoNGTRQQMsT3TlxPJ-MKZMRMwBKjSiXQxfx1sTcr4sbPW5GtOtxT0BbUUoETXyG3-_bqWvciRaYFIWPeHHnhP8AY_281G3SMIVJiTTmi6M55r78Gz-r-dTMAO","token_type":"Bearer","refresh_token":"1//0e0P5bJGtrvnwCgYIARAAGA4SNwF-L9IrCuYyZaKKeMTnXNLvSO-rrFRVAoamThEKZ796rZGpvUjU8qifmL8POAg4SJHQgSBTXnM","expiry":"2021-08-18T18:00:51.8799223+07:00"}'}, {'id': '7219a2ec-df47-4cca-861a-499ddba2c936', 'share_drive_id': '0AGbBjoDOim8qUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_XfcpNNkpkemjwN4BxsUYx0QN5BLOq3OYZD6hzmngVvWEkU113_gMFyAyERbtI84z4PL-Tky0qFbkgOyoGa8UffIbmg3toqUkcuSKHCKSzbdAB6ILYCy_ZiVe15VKabJTsYwLBf6RGuU2oWHb_cRv8","token_type":"Bearer","refresh_token":"1//0eUvHcqM39IQMCgYIARAAGA4SNwF-L9Ir9zMxSp7mMPnfRNr_DP01nE9j9hxdGIR33Cw9RO5lSNR3674On2CiEHyqOBEqiZ5BmSk","expiry":"2021-08-18T18:01:19.271579+07:00"}'}]

list_drive_id = [x['share_drive_id'] for x in upload_config]
for drive_id in list_drive_id:
    print(drive_id)
    list_folder_current_in_temp_drive = get_file_warehouse_list(access_token, drive_id)
    folder_id = [x.get('id') for x in list_folder_current_in_temp_drive]
    if len(folder_id) == 1:
        folder_id = folder_id[0]
        list_file_of_temp_folder_in_temp_drive = get_file_warehouse_list(access_token, drive_id, folder_id)
        for file in list_file_of_temp_folder_in_temp_drive:
            file_id = file.get('id')
            new_thread = threading.Thread(target=move_file_from_root_to_share_drive, kwargs={
                '_access_token': access_token,
                '_file_id': file_id,
                '_new_drive_id': root_folder_id,
                '_old_drive_id': folder_id
            })
            new_thread.start()
            time.sleep(0.01)
            list_thread.append(new_thread)
        for thread in list_thread:
            thread.join()
        delete_temp_folder_in_temp_drive(access_token, folder_id)
    delete_share_drive(access_token, drive_id)
    print('move ok')


# ''' CHUYEN FILE VE ROOT FOLDER '''
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
