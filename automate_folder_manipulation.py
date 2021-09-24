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
input('Is number corrent ? press any key...')
next_step_info = []
for i in range(40):
    intersection_list = list(set(list_file_warehouse_name_only).intersection(list_current_running))
    list_file_name_will_be_upload = list(set(list_file_warehouse_name_only) - set(intersection_list))[:50]
    list_current_running.extend(list_file_name_will_be_upload)
    new_drive_id = create_new_drive(access_token)
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

'''SAU KHI UPLOAD THI CHUYEN FILE VE'''
# list_thread = []
# # list_drive = get_list_drive(_access_token=access_token)
# # list_drive_id = [drive.get('id') for drive in list_drive if is_valid_uuid(drive.get('name'))]
# upload_config = [{'id': 'f1f96dea-bd60-40e4-bb1c-fedd193a76cd', 'share_drive_id': '0AHvGOfyeKmYHUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM81b6k61sUGsTrO_aMZcow9yCTbqfoSBg3jFCIpYbidV-I4UiVr0hADhEraFNyoW05JWxBq2rlyeDd8FeRp0UXGIwW41vlgotgXfCBCGRbotwOQp5kHRzI7SdvKqGUVbVr0k6Xv9Ao0_bkp8xOim3yp","token_type":"Bearer","refresh_token":"1//0e1hMO-vPoNuoCgYIARAAGA4SNwF-L9IrEO6TpW0pABAUhQdc8Hh5INBIqL0xCOBNBm1YgpS2WWRbESD2XIiF77_jcs1tf6whyr4","expiry":"2021-08-18T11:59:13.3059316+07:00"}'}, {'id': '45114c2d-7073-4579-a513-b8616aa50e6c', 'share_drive_id': '0ALd7geg7yZ4fUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_IQGIZf97-IME-4lqYvoXTyUtOZUPDR3Llui0_CAPyfzEjStLQlE-ESEwXKNG_ZtBrNrxrpObshMH31ziYK2sMZXDDyt_V2rfxnVwiwJ1YgJvm2MiLXWew1yo5KanFzEOcFe98409VtaQdi7oMm_Fv","token_type":"Bearer","refresh_token":"1//0e3BBrH3T-VDzCgYIARAAGA4SNwF-L9IrmIIh0AbVo7pZ4ISjVUAMOtAG9Fh4vS53Yr3dJ-t7YsqjHZ19MNBZhQV3A--OmVF-218","expiry":"2021-08-18T11:59:53.242003+07:00"}'}, {'id': 'b64867b2-3c48-4bc3-b8c1-dd1c6dae2ef1', 'share_drive_id': '0AGiPc0NMR_-YUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9aVE7GF4F7IuXsMGnTddcXhtE7_wvULR1TFcDx-5bMAE0iQcUgZ2LA0RrFeNU-HZ_4Jxmmpqv5q01W2CaInxaP6pcw_9Q7qw1ZOJvAClTF09btSo_gJHIBHX0on6cd6H5FO6Q-qzHC8efb0CcNcMCg","token_type":"Bearer","refresh_token":"1//0eloNuycLMcl1CgYIARAAGA4SNwF-L9Ir_AmxD4YSy5TZHdJQEjb2tEKyptaHdZFkhA3MuJJFD-2PEVS8KeyuqXmx43czoI7bmQ0","expiry":"2021-08-18T13:54:31.3438449+07:00"}'}, {'id': '03861ba8-6c7a-48ce-a58d-90c3451fd538', 'share_drive_id': '0APjVuNot8E44Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-eG5S7Wc1sBocyzXUHqPG_FV95nWGRz_aBdaaK0sgpDyMAFtrmXYnmi3NrQiwIwjeBPn7BV8IvostcnHauGwCzq1Jg-6_7wfXhrYdZ_sHCv0eeBUh5UHv7aNHP3ek4JM_VhCT0NnOjez0HBmVvSQw4","token_type":"Bearer","refresh_token":"1//0ewO_r_LmLiZ3CgYIARAAGA4SNwF-L9Ir0rdf1gA2b-9M_uaOGyf0mSzWoX2VQ4Uto0cUX_kA7x_PYXiZ7m945amWrZDbIDGsEtY","expiry":"2021-08-18T13:55:01.5199214+07:00"}'}, {'id': '442dcfd9-225d-4322-88b7-ab9e7857dcf6', 'share_drive_id': '0AByG1AAZ2BJ6Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-Uhf0Dj0tQXiF_ZNb91wQ13PrdyEeOcYOSotGNOtiLRowDGI2EpC_AVJ4986PGo-Kx8tJUyFIJc7an2X20B0YtxBO82frumIkGSQsNlfGE6kMPGfk1WV89VSI1lNK2FtClWSDYREDBI_cNQkFAZe2a","token_type":"Bearer","refresh_token":"1//0ejDBVRHZAebMCgYIARAAGA4SNwF-L9Iri7zHmFMcAn8WwvYeD6ngWU5efdlK8Xswh4zwzTx_a_R6q3_44V5FT200x1EtRnTcJ-8","expiry":"2021-08-18T13:55:40.3651032+07:00"}'}, {'id': '1ed3c6b1-35a7-410e-ad39-d6f65309f624', 'share_drive_id': '0ANPd-4CiaS0-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_f06giFgOEWG3yZCzLvID8Wwfbxj7GpDTE5HSscQPLWrR7ekodV2YP2p9BCW-1s0XwFGKZMlPwTgL8RBRHdv2iHisoO1Xd3NaT4UrHjnd-XjNrTnhwwea61WUFHPClBtidWPD-2wOcj0AdLk1-urv_","token_type":"Bearer","refresh_token":"1//0ecLQZ2gDlptDCgYIARAAGA4SNwF-L9IrRr8NYnrsr9Vd1f-EbVxCkrOVg49663miK86_g5x_PJjZSqzuAQanxqPNy9ciY9o5nC8","expiry":"2021-08-18T13:56:08.2776252+07:00"}'}, {'id': '23afb148-4681-455e-9469-3d5ec4a48a11', 'share_drive_id': '0ALNXRy5WUkB_Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_d6sNLBPuYN48YpRMq5c1fHWiC3HPcv6PUnOMT2XB-qqPxBXRMWmD4hhxGFELWUTbvwJB8ArY39GmKIkqBRUAKvK8M9nsZBGQSo1-Rs8cmTV3y-Mr3jN9G_eN7X5zqE7cUR3Cxi12SDSgYgNyNA6tA","token_type":"Bearer","refresh_token":"1//0ebpvkqAY4PpACgYIARAAGA4SNgF-L9IrllrFxGmlyfnlNuGLmT9RWVIT1Jq6IupFrs3fruF6O4QPosWTbLrV9AEuc4mih8QowQ","expiry":"2021-08-18T13:57:34.9289244+07:00"}'}, {'id': '80caa258-d005-4f70-ac2e-4e262c64e256', 'share_drive_id': '0AE1Y0TcFe9dFUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_NkPfHoSd6ELHjvp-a8kNzoR2BbkTXOtmFEXSm3795xZjIsBJRRPDnEYDrrFLTzehS7Cd-F-KbEi1yh684KZHtx979_rTfd9n-7cajBrY89f6s3PfKDa3LrPa0HTP8EFBn2GU-kXKd_PSf9ypPG9Gg","token_type":"Bearer","refresh_token":"1//0elHPRFI3Hh61CgYIARAAGA4SNwF-L9Ir80t9plpMDgcKjK6FWOWq81ksXpDrrSneNdMv4Yb_oxqM39KMkkXbJ-32IyREy8l3V9U","expiry":"2021-08-18T13:58:01.8380733+07:00"}'}, {'id': '7820adb0-f78b-4093-a77e-74f243527f31', 'share_drive_id': '0ADCRbEIcGApqUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_MbgffIfmpgR05hbVzAKfQ-oD7CD8Ihy9KhN61tvpMNSDmHuU6DBpZKIJIQo556Vq9djpVbRSujsjHv71PZEsUvO8VFYbGK3CKIju-AJUi2zxZtOVxxJelYnjLTDKeZKqIO0nd_ZEQ55XKC1-NgeO-","token_type":"Bearer","refresh_token":"1//0e2tdXIBxMuOaCgYIARAAGA4SNwF-L9IrFbCE6f2TngWEqVc7yU8e3RLoDJmpbPQlDHw9ZVWz4yxzWUeWx9Wtq_x-N9bTR9JjMiI","expiry":"2021-08-18T13:58:36.2864059+07:00"}'}, {'id': '65746880-c226-4032-9447-87cbb3cfe9da', 'share_drive_id': '0AAUenCYg2vosUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9rDc9HvrP47DiZtmldx7QJhYSTJgiZh8jbdlC9FhyQovLD8klTd15o4LJ2a-BYQKtfaWELjy2YyL-IW7vVHl-bPaHu_A3hwKhukBRv7JRUcO3GG-q6lfJRfmWHUnjwnh0kId-kT-plT3mWwDt5fpLN","token_type":"Bearer","refresh_token":"1//0efWxsMfBLLWBCgYIARAAGA4SNwF-L9Irbl0JWdfCHvSGSv4eFyRfcfDCa-QjDO1jYcB_B4XJHgtEz8xV7mPwRUMAlGLaBOc6owA","expiry":"2021-08-18T13:59:13.1687607+07:00"}'}, {'id': '0186e150-37aa-410d-8d14-ad2440671ff2', 'share_drive_id': '0AKJbZp53IYklUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--aN0zJIBuzl8-Gik-67TPPNb86UkdC71BQsLJ1vOsG8nYCFvptra_qc_D6Hbthb7kmkgkQR_z8LqmFpJ42e4VRvrclViG3Cc7PWkSlU69YA5A_xZfwgXwQe-RdM-KBxfPNvOemCJ3zBGIJY6dr_Gm","token_type":"Bearer","refresh_token":"1//0eQNvp7PdthFBCgYIARAAGA4SNwF-L9Irb_3JKH1OTXHVPk-e2DPFmZZ40VS3htJEM7yPDnvW01BF-Phy1qLK7XDDeq_jM-gDiYE","expiry":"2021-08-18T13:59:43.0133264+07:00"}'}, {'id': '92eddafe-2059-47de-a001-f0de0ccfd2a0', 'share_drive_id': '0AB_bADbd7JLQUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_yTBl9Kb8JTvyBFa_JDsr5RUtrROTzR60Vuk2Wjk18ytaFi7jB8JMPR7PC3XUOIsSp5e1AQwNnP_PW5PS8SFMnQlbrxmhmAVjGtRb8vMqm9Ln_1HvDSxoDBLVVqZiaYIbSEO93wwnw_m3utSaG-IXC","token_type":"Bearer","refresh_token":"1//0e9_NpBjsr5kbCgYIARAAGA4SNwF-L9Ir0gS5X2T1IU-QguZeOmo6V9HGSjavIyiTKVMlI8FAD6ES77-AmNXqQ75pMFN670RgCk0","expiry":"2021-08-18T14:00:15.3026537+07:00"}'}, {'id': '8638c823-bdee-4465-94e2-479315118536', 'share_drive_id': '0AJKdoyrBZ-vbUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8q32zFARbimDWqIurKGUZctnhfp4t1ZIG7AL0Uad7Nor8sj06AQfYSpLKHIfxd4Yi0BqLCPxXEpOeRuOVfuD7AvggR5ZlVB-TCsjlBD176N3JS9YvhKJdHgGRlbR5XKbt6uBJIoOgebSoER-2nyFSH","token_type":"Bearer","refresh_token":"1//0esJHaUanoAPkCgYIARAAGA4SNwF-L9Ir2s8Mgh58sA3cas3h_oev__Ty53PvRA9gXZHs2wj5CBInElRfW8B5RCWXjLp8bRNXbGc","expiry":"2021-08-18T14:00:55.4510255+07:00"}'}, {'id': '432ce020-64ad-4057-8cc1-15cf91d8f6fe', 'share_drive_id': '0ANlDUHvvbtOpUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8tAZINOStdywe4mDAvJJur0AUzELjzJEaqStaHyedym3dvUGEEKnyENNWwQMOvM_H53MG4pD6ugTUrZ1tJ_mi09EMr1wESYuo7P_1TOKLP6coJmX0E16K4UTj9fITUWY2t6-q0quh_UmHr3tIiKphQ","token_type":"Bearer","refresh_token":"1//0e-lL8dKE4shACgYIARAAGA4SNwF-L9IroALaRr9s31P9R9zy4xwCoqWOy0ruSV-TaRZecoMIRSArxAhqy-QAtarYTHD-wefNMG8","expiry":"2021-08-18T14:01:21.5239468+07:00"}'}, {'id': 'd0856aac-b851-4f91-8489-a79215cbaf2f', 'share_drive_id': '0AGyhcZiP32NEUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-I4ufapp_1LUvRrnWhYO-LUREfYqnCyXfUxH3JthUMSMpvMaQuKRwOsW6hH_Rz0MS-_n-JLPbzJ1_TY6kj-CMCR48_RGHuVGXSCp9lUhNcxFR3kxGv2CrXrRizQJ7HB8lH4YU_8PeCSd4WM93sZ7jQ","token_type":"Bearer","refresh_token":"1//0ewTFwAasSkYkCgYIARAAGA4SNwF-L9Irmgm2fuKhstF56z0dZN3H8I9UkeD5goAbKy8URG_JSf40fjiyjJnRRzrf9w6Zm3N243E","expiry":"2021-08-18T14:01:56.9860301+07:00"}'}, {'id': '196f7e93-0596-449e-af35-5418c0a20fdb', 'share_drive_id': '0AFE9uk03bNF7Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_uo2vp32UaRE0XtnwJXU90omzIpkkYUxo5diMJJVVTj6vTqdeRB44GATWwAQ2SBdqUMRcEJKM_bgLhi3GWk4-76DMa4K9XZerdmhYAVIcKIPjci8itaBT4VKud4C3sRfNgMdTXKMfWzoTExkgtmSg4","token_type":"Bearer","refresh_token":"1//0e_NQf-4CfokrCgYIARAAGA4SNwF-L9IrirMu9hJ3YbN3EdLoSt-lU3z1QmMYSq_H9ecHufDrec9uec3fE7sZ_J4SbzvNDxgmEwA","expiry":"2021-08-18T14:02:24.8801233+07:00"}'}, {'id': 'd68c0510-110d-4c1c-8e9d-ade30fee0731', 'share_drive_id': '0AJsW50j8FC5wUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-DePs5IHakIQsCc3BP9aPU79mLZRUPBYVUPipHX1xuEKJJs5ype9jD6sE9QwlHnC90NIlyn07BUROHd6U62xaRNPFDN9MxAGe2MXKYi2OP93WPjRUD7naCvj7Y5F-aJgpRxaq4WYz-BpLcAyNpgQwJ","token_type":"Bearer","refresh_token":"1//0ecSgG99AkxXFCgYIARAAGA4SNwF-L9Ir4f6O5CqMOzI4zwY3HAAlG7okabV-CsAbGQANLsQhwz2LiD9PbkiVCC1FhXARIX-3mUI","expiry":"2021-08-18T14:02:52.6081411+07:00"}'}, {'id': 'a9aff0b0-c1e3-46d5-bae9-9496358da91b', 'share_drive_id': '0AGhwSSnPT8eYUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-iKpGD7o4uVTyIDJEXL-bMureN5pu1ARadejqqq7Oj7gKeoqYA4XbmWfD7LLAnCQ94bLhTWr2nhDIuf-j-C8ZCDcZ1OqupgbKcTRS22p57CWyxihAAm1TZtlSZSv3B9wfRDoP4OhCNU0GaLYKFFtGr","token_type":"Bearer","refresh_token":"1//0eCfgguWJ39FWCgYIARAAGA4SNwF-L9IrD2h5k3Ka9XC9QTPso_zQ5GUgNocKXBKa3RpuCfQW0Yk-kiHeVwHWs88W5Nhni6h76JI","expiry":"2021-08-18T14:03:19.5342573+07:00"}'}, {'id': 'e1fbfb95-d186-4a69-b28c-c8ae78fd2c1c', 'share_drive_id': '0AKr9iZmglpJcUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-qjbHpnUe6gD_z4XyhBnkOwk-LATd4DLIIjcXLyTOPnDFJCTRKp2MsaJYcppYJfhQM3wXnf0JenjgRpTHwJrwEpsJyY63FTjp2JtGZvBSS0oimdr49O59kkFjEsaiJhKoyhrFsUUq1AdOl5mXoHspL","token_type":"Bearer","refresh_token":"1//0eoou7VD-NIo0CgYIARAAGA4SNgF-L9IrokxfOm_5R5OPCL-9CIIjXj82B57E2Qc5gIFLwiQ2aR9banIHZbhroAbhhj2oP0m7dA","expiry":"2021-08-18T14:03:44.6511735+07:00"}'}, {'id': '0ffe673a-46ab-4750-8657-dcdc325e7fa9', 'share_drive_id': '0AAmtQg6QFtoMUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8xoiznWP9Ck5v9pYOQKJO0F_sKUrl5ihvZ4AtXN88FMcyaQJySXi3hPOL4auVqbCrW-wxtoO-9SKkcHViLH7pcVlsdxr-QYwsd6BF264DOBN0U8XxCizQLqDufGRg2QCPsbg61N45XCriOB9IROTFP","token_type":"Bearer","refresh_token":"1//0eJFyBswkABp-CgYIARAAGA4SNwF-L9Irdn9RkXyk7gmKIL8ubI1s9xbkl3NzFAIPFM5nCyMW8LoDmxeyP7XXh2gv_chVDHNcmsA","expiry":"2021-08-18T14:04:20.3403283+07:00"}'}, {'id': '669e0b81-2688-4a49-a0db-4ba2bc70e520', 'share_drive_id': '0AMud_w3uaiYiUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_M05-iqll3Idh8trXG_SGtYE1e7U3zc2OIwRm8P5-IhGF2lLN2wxB4KuwaChfbTmtdNGZLR0GF63B9C2ts2iD5oDyF61DtnUHgAkGLt9Vt2pQq4BLdCe1uVGdomb5JV771s_Vy_3KgTdGTIbmjFweG","token_type":"Bearer","refresh_token":"1//0e7keAsyNiE21CgYIARAAGA4SNwF-L9IrPEh9wVD8iVE8u9v14Wky1BjLOsjX7RE7KefT8C69tAanZBKF1rJYDDLiHmDibQVWGu8","expiry":"2021-08-18T14:04:52.2720643+07:00"}'}, {'id': 'fa918f38-f280-45be-a207-66754eceeceb', 'share_drive_id': '0AJuGJu4Qaqm-Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM98tadXGlXQA9jQ3JCzVPXcSJk0qlDrurc7iswxHMUKZpNgQ3UJ1ajSa-jXfcAt5JmtyM6tZJ6rUMURDNykT-d3U7vVISuzHQu7GdGGkXBwYib1c4tu3nk9ySBRO22Jbe2VkduNSUs7g9lZ244skDWW","token_type":"Bearer","refresh_token":"1//0emImTAfriNIECgYIARAAGA4SNwF-L9IrizCoH-5rZtiPyjnK7J062Q0Roi8z4TAIJjUCQ3CegFkVa9YjeXBAjlzHPxvsAESAq34","expiry":"2021-08-18T14:05:50.3927271+07:00"}'}, {'id': '99fe4841-da2b-4f22-bd54-e28a4da8a735', 'share_drive_id': '0AO6JGYYBwsIzUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM85VErNuOBtDpOWZx4qG4LQx0MZA9Fer2mUjK_PxzZLaGBZRyGnc6W7XwnrYgELneS19LJ3kWlu4he9mMGpzIBsRpmkvFL3Sgrq9Mrq_7zaJoUj9UuNDqN_QvqULfaxMxKqjXNZuUlgr2qaAgQmC8LN","token_type":"Bearer","refresh_token":"1//0eDb11FHL8DCtCgYIARAAGA4SNwF-L9IrHYf_xsUCYpPsAi99P7i4hQpYnqqGjltxILe_o-gD0Uu8PWI9i9TXIADBLNll8rKgMnc","expiry":"2021-08-18T14:06:17.9415136+07:00"}'}, {'id': '67f8d011-890c-49f5-a652-de8bafba5d7a', 'share_drive_id': '0AFvtgbiUFrh9Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9tu709t5x5rpLEBBpJQPWj49fZsNuzP906ECKbnFHbmSu0kYWuKlJziPwBWHED3HXXv0Xk_pfYJPZJ7vOq5fHl8rPvS-TxnqeozQNo2rQ_6nJ4sMsdVo7bmigrcIYc-mrAD51mw8INaVLSjPY3Nhy9","token_type":"Bearer","refresh_token":"1//0eubJO7eO10zOCgYIARAAGA4SNwF-L9IrrleqXGmP7fC_amUVCMZoAdus0rDF3nXYsoirKM2CPM5xyDPbv5ekEUblorkrRyeXAMk","expiry":"2021-08-18T14:06:41.8943525+07:00"}'}, {'id': '8021f41a-d456-4b7a-9ee8-88ab9af19ba1', 'share_drive_id': '0AIv9-32lf_dEUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_TmG3jDtv_HhuRv-wMnzylP0Sc7pzo_KTzidz9CXYTHuXVoFawHra7FaHS1yp9mudynKQJNWSo5NNrmKQfRVA5DpM82oh5LW3uMQxMT1-vCek7xCqpIWMIkuCotQjhOrkjIt1FynyD6-ue3x-5twwn","token_type":"Bearer","refresh_token":"1//0e1c5wJ6H5DhkCgYIARAAGA4SNwF-L9IrQcFbUBmjYrkyIacnwx44WMPwvw9NV89S0R-_rbpe6BJxOhtq_VuTTlFETHfcXb5J9Yc","expiry":"2021-08-18T14:07:06.1655253+07:00"}'}, {'id': '78e30677-ddf5-4f04-a837-aa4ffe1f067f', 'share_drive_id': '0AMUoRfdkyCkzUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_iPoc9zST3zFrAAqA6hothAeusb20qwSLhtkIkgKqNCdhI8UWN0YDB3C1AVqCbMbcieUISyJBwshuAPJu8kOjX28VWgjy-3VJwgV_ZXtaPjbiZNEGdGsBrgVVfrdzwgULZ45silabWfmFRoohQK5io","token_type":"Bearer","refresh_token":"1//0elaztZ4vkS26CgYIARAAGA4SNwF-L9Irk5bkDGSN8qdGRFznpIeEQXXTco-UWnbeMhcIR2CC9s5vIBUHSgOmfeRCb4rndHLenkY","expiry":"2021-08-18T14:08:11.5419379+07:00"}'}, {'id': '82d6c30a-2e3e-4a15-8241-872f6bd3a571', 'share_drive_id': '0AITOfNDNrxdVUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_-FtS1z8YSSoTfbJ9Trra0v2aBgAmbo_N1t7W6GHc7Awf2HzPHx68m5yi1b-1lc0xxfkixs3pQT2tkfxR1KIjCnKFVKJ1eX7Jh72eCJAUYtKsFqOCq53DeQqocM9kH_dsQsuXy4YkxayBUM78pkodB","token_type":"Bearer","refresh_token":"1//0e7v9Gm0aTh5wCgYIARAAGA4SNwF-L9Ir99XrCOzN2j9lISRSYEsDRMDSiB5VJ0yZPrm3ZkcvpFAfh2cAY7l8iJU4ECWYafy5Ph0","expiry":"2021-08-18T14:08:36.3854191+07:00"}'}, {'id': '334d7aba-5b97-4b77-9e02-9629a74f2ea4', 'share_drive_id': '0AI4qiCP77KdxUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8EAkm7iTjQT6-N-_JjRKC3Z69GCZlvohM1ooQsuzRsZD_gC2_fXRPDrW4oKVM5kqu68-w0Jqmm9SUldhrIikbsQviudZDqkGY7QtbcLGHNFN-Eg39CIJHmNkPhVCSjtJnh3Yj3Fg0keSTjzXlDcpWS","token_type":"Bearer","refresh_token":"1//0eYwTvZcihS_VCgYIARAAGA4SNwF-L9IrQMEV0LtUp3Cz7cXXFOi9kdMrBj1qJiXJFLAwWC4MPQr7dWGBwA_Y9IWr2Fi9BbLgBY8","expiry":"2021-08-18T14:09:11.6548198+07:00"}'}, {'id': '46c3def9-e29e-4b70-8ae4-916875d75d5a', 'share_drive_id': '0AIJGfDMwdEdQUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_S-9YmtSv6jTlIowRpgRs4x6D1jZnt1_Yb0aootqrnGUFxR848cnE9vV3c1Lt7D-SKK8_AfExVrJpJjxLH8R8qXw76EQJ4A2wSS7nXnxcjICB2Jmg3GA0XlXqMJYd3Cg9lC6i7GO2XrB5HihbnfvCB","token_type":"Bearer","refresh_token":"1//0ekXIRkEIaNCwCgYIARAAGA4SNwF-L9IrLPXDeoZv03gnFP2_o-olXIX6_UbF2KWDVJAVCeOJObD4_STkjeBJSEjZ81XehaY5ZgQ","expiry":"2021-08-18T14:09:43.6783757+07:00"}'}, {'id': '876a0ce1-4575-4194-9e91-53d5314a44ad', 'share_drive_id': '0AEgMg1eCSxIbUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM9Gvs1PjDSLLb09DzvDOlt-V9SZ5exf-NV6zXpmKWbWeLWKhvt8fNMs7aUZOLdt7IpOMQW2jZcy3sIS-OkfQp9Ox89M7ImdksvGR9W2UnJFWxJZkWTgEzSHGp-mr3o8bkWk0nvF--zEAVoImPDgM513","token_type":"Bearer","refresh_token":"1//0e44degUO2MovCgYIARAAGA4SNwF-L9IrydvtmWKP8u6OOMp7kHmbJ52hXMMWKOtP_W34FskXYz3U-V7dHPy-iVZwBV3BKnk99hs","expiry":"2021-08-18T14:10:06.1790713+07:00"}'}, {'id': 'bfeab28c-dc54-4004-9d70-209594009440', 'share_drive_id': '0AMItwcvKOguGUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_LLmdQOdey5Gb2s2G1Ln5MCWOYgX0pn7F5oCnkW34sYQtItBExNV3tW4HtdvLHw565b2EB9cH9bJrqMt8VG2fcCVbl6V1Gr9fG6SAOgf7_EziR6Rj_HistGAvY6OSKtmhnKwm57at2PaCTepDMa4tT","token_type":"Bearer","refresh_token":"1//0eAehLomLv3Z4CgYIARAAGA4SNwF-L9IrwDvUJ2-IL9g3f5HOPOjaRxbnIz1m-JlVeGepIticddSDD3MtgIcPwzfc1L8sAcbA884","expiry":"2021-08-18T14:17:34.8704993+07:00"}'}, {'id': '143e4730-f720-400f-8417-262da69699bb', 'share_drive_id': '0ACZ7R4ICHI66Uk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jK1mAwcTPH4eDBeeYTWjMjGIlfNiAFYnJ5mIdK8nvdT7m6NE-bDTcODV3wvEil-leU3rT68TMnZZous6WwDACahDI7SKDhHq-qsRCMDXP9-Iq2TD8zpuCQ-ZpllpVd7JQPFcD64TWf7Q8EfJSsZz_","token_type":"Bearer","refresh_token":"1//0eHEvoSI0GuwsCgYIARAAGA4SNwF-L9IrzVTstH4qb5BN1R7JplJYNJ_KrzhBOh7cnRBhmEQs_PrtKfE9TjBcP4_pdk0UpMCFvMs","expiry":"2021-08-18T14:18:02.120876+07:00"}'}, {'id': '1aba5c6a-6789-4aa9-a4c2-ee2c6389397f', 'share_drive_id': '0AIL9nsRSrDluUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM86lEsjC7NCsMt6jHEKOGmauIi5FVXBxuLnsRIk8Mw_0_k2-5wVFr0LpJChf1fGEaXZ4iW2-ABQHCeuKgdtxL2rn3MNb19q2jJvegzPi2KX8XuLrmHVUKW9c6CtliDeJxksKtzJXori3sE1M3Vj1sKk","token_type":"Bearer","refresh_token":"1//0eWi1ayt-7K2-CgYIARAAGA4SNwF-L9IrvTOztOdPmpgu34QvvvgPSFCqJRpzX17k6h8PQvUWE_nycDt-l7PCnhAGU_Ua_wf4B3A","expiry":"2021-08-18T14:18:32.0753091+07:00"}'}, {'id': '4ae50bcb-a9b7-4771-87d2-e9ab2701aede', 'share_drive_id': '0AH2Nl-m5shQmUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-MY2dUu8qynumI1kR3Kc30uOLbBmqu6m2OFiK3M5uvWd-YvQNfWlCIvYwCpiyws9zgA-xO1mqLDVkA6Gn0gLCaL-x6h1pi7uz_i_Zm8LD7rldFm3_F0L_BDntK23JRMXTAOxdcLMlMK2LSlZ6lYdTZ","token_type":"Bearer","refresh_token":"1//0eiuldKYpMjHcCgYIARAAGA4SNwF-L9IrtsYK3Gdt0yxwQrjJCT3OhOeYweZt2-NdEOs-ecu_iducM36RExRPdtVU6jH8zyT9PHQ","expiry":"2021-08-18T14:18:53.33193+07:00"}'}, {'id': '87974d44-0fae-42f7-baef-c1ec68041407', 'share_drive_id': '0AG4oPWMpJ1eZUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM--TN-Jjk64mtn6yJ4BnbRxuOR4P9dlYdV7zs1UU5o1caK68on6yh6iUYumq9XEDZj_BOjzcFUrt5NfNMJvzzCnmq84esx0ah1s9w97VU0FJc9LC2VI6kzq6RvU26JRA6hIYXMczBa7PRsD2WmZIhAy","token_type":"Bearer","refresh_token":"1//0esWLHZcAYmEuCgYIARAAGA4SNwF-L9IrS-Dr5JETd6Ncec8ixD0TLdRu4ebwfveg2mAhfIHu0gzCErjzPeDsXPJPFG2nj5axCS8","expiry":"2021-08-18T14:19:19.5777359+07:00"}'}, {'id': '48d0ca4b-de25-4f60-b3ed-fe75a98bfd49', 'share_drive_id': '0ABCeabzjIBXdUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM8C1Y8ZJzuEYePIeK1WnwnO8Xt0Lg25_apsnSLNjOCQk_VFX1i_hs5u19OCFlYDKvX5Bapvg2tlnvMWQsgkKdlmR-a6Zuv70-t6X-NkJPnl2bov5RWIXwLO54RIY1wJcMIqDPuZzOwqkY3osXia9YCF","token_type":"Bearer","refresh_token":"1//0eqq1LhGrDfvGCgYIARAAGA4SNwF-L9IrCZ0lV8i1yjwD0glniNZvv3GsRXGXsKEJrZX0pwygEiIx30lVMiyPOOZgOdGJv3dkVe4","expiry":"2021-08-18T14:21:06.5190624+07:00"}'}, {'id': '8b37d3b2-7e24-44d2-9630-3f09edba9e7d', 'share_drive_id': '0ADUW7qDuE2CEUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM-cKm6IScssDaZs7zZp-W30S98fM__fUfimebfIyGNNXLs-dnbAYzjwtcOIV4uaPA9ozTGJJZYLCjhot9oFCh0iDI9D_lNohTF88OJIzy5qXBwdK0iq28RKUQAiLuEnZLl39H4dfufEWT9I_3uqlyFo","token_type":"Bearer","refresh_token":"1//0ev9uGQ0Xf0DzCgYIARAAGA4SNwF-L9IrPi9mZCRKvvT3Z7mOKaHuN4SZI_CZekty9JL3TROaLBpJgWhaamnhV5kE7gE69TTDn6Y","expiry":"2021-08-18T14:21:28.8232665+07:00"}'}, {'id': '014c171e-3478-42e4-a953-0a58c39937f6', 'share_drive_id': '0AOHlwk-8ykPVUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_jDKcsUJ1goOgvLbZWJ_3zD_XXQUHvokXwNBcs4whBdQhfeBIQDIHaj1t2n0q6RXRY18zBR0drvOrVk4Bu6q0aRkbWgOTEJo6F-1ouXRn1CYXAgK77J5sVOUS-NLD1lbdyCnUZblbkoiZq2kKSpWd1","token_type":"Bearer","refresh_token":"1//0eI4RYA9IRUjyCgYIARAAGA4SNwF-L9Ir--RhDsbGEzNKmDpuBKLfSoIk44nC_EIIt9pEY1xiLciEx4BwgjCYCPtCFdPthNbyOwo","expiry":"2021-08-18T14:21:48.8429886+07:00"}'}, {'id': '966466b6-d6a6-4d6f-b6d5-84965b0f5c8e', 'share_drive_id': '0AKZAG_H9XznVUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_77uqbLV8LZJe-0b6tZ4W-uoBm-NulyFYaTCBXyV5sZe9i2kE14vQnKMKriyXId-qXs8pw0VKwuBhRZsYfg03tabSDC4YqxW8gCpxvfn6BKKbzoSoZmo_M351jau2D7pkdu-4U1419FvwVaPQPk2Qg","token_type":"Bearer","refresh_token":"1//0ejOfei10LH1MCgYIARAAGA4SNgF-L9IrXlh2-T_YYXGQVdy_9bL079c9zrqz7EUlVrY0LV3jBpqbs8f0On873B1pMkzh0J5VXw","expiry":"2021-08-18T14:22:19.1932152+07:00"}'}, {'id': '738aa914-1a52-453d-9ca0-eab87be9961b', 'share_drive_id': '0AJ-smoKkjGkDUk9PVA', 'rclone_token': '{"access_token":"ya29.a0ARrdaM_Q6BxZAcAcRCSK6SelvAqjBLp4whIXN-1w4DzUlj0cn6gPnN6ERrlSYjfsyWAOWYfLBYXTuUqI2yzDfiIL1APg3BSYv85C5tof0gg_vZECsN_-0dwOVMzKpvzo30e7Ey2-ipPb3oFx-vlU8KFyFJEn","token_type":"Bearer","refresh_token":"1//0egR0GI2y82OGCgYIARAAGA4SNwF-L9IrJky5ourm_u7PeIO--UufXtKZxbGLArrEdxyQfuj_GxfhRGArgUQSgODHDZihU7pvNUk","expiry":"2021-08-18T14:23:12.1659074+07:00"}'}]
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
#     delete_share_drive(access_token, drive_id)
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
