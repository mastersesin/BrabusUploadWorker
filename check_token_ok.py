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


def delete_share_drive(_access_token, drive_id):
    endpoint_delete_drive = f'https://www.googleapis.com/drive/v3/drives/{drive_id}'
    headers = {
        'Authorization': f'Bearer {_access_token}'
    }
    try:
        response = requests.delete(url=endpoint_delete_drive, headers=headers)
    except (requests.exceptions.ReadTimeout, TimeoutError, requests.exceptions.SSLError):
        return delete_share_drive(_access_token, drive_id)
    if response.status_code == 204:
        print(f'Delete drive {drive_id} successfully')
        return True
    else:
        if response.status_code == 403:
            time.sleep(3)
            return delete_share_drive(_access_token, drive_id)
        print(response.text, response.status_code)


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
            print(response.text)
    except (requests.exceptions.ReadTimeout, TimeoutError):
        return add_email_to_drive(_email, _drive_id, _access_token)


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
    return_code = os.system(f'rclone copy checkplot.service {drive_id}:')
    if not return_code == 0:
        return False
    return_code = os.system(f'rclone delete {drive_id}:/checkplot.service')
    if not return_code == 0:
        input('Cannot delete file but drive ok... Press any key')
    return True


access_token = get_access_token_from_refresh_token(_refresh_token=refresh_token)
list_credential = session.query(Credential).all()


def worker(cre, access_token):
    new_drive_id = create_new_drive(_access_token=access_token)
    add_email_to_drive(cre.email, new_drive_id, access_token)
    if not test_rclone(token=cre.json_credential, drive_id=new_drive_id):
        print(f'Err with credential email {cre.email}')
    delete_share_drive(_access_token=access_token, drive_id=new_drive_id)


# list_thread = []
# PROCESS_COUNT = 5
# for cre in list_credential:
#     cre: Credential
#     new_thread = threading.Thread(target=worker, args=(cre, access_token))
#     new_thread.start()
#     list_thread.append(new_thread)
#     while len(list_thread) >= PROCESS_COUNT:
#         list_thread = [running_process for running_process in list_thread if running_process.is_alive()]
#         time.sleep(0.01)
# for p in list_thread:
#     p.join()

test_rclone(token='{"access_token":"ya29.a0ARrdaM81b6k61sUGsTrO_aMZcow9yCTbqfoSBg3jFCIpYbidV-I4UiVr0hADhEraFNyoW05JWxBq2rlyeDd8FeRp0UXGIwW41vlgotgXfCBCGRbotwOQp5kHRzI7SdvKqGUVbVr0k6Xv9Ao0_bkp8xOim3yp","token_type":"Bearer","refresh_token":"1//0e1hMO-vPoNuoCgYIARAAGA4SNwF-L9IrEO6TpW0pABAUhQdc8Hh5INBIqL0xCOBNBm1YgpS2WWRbESD2XIiF77_jcs1tf6whyr4","expiry":"2021-08-18T11:59:13.3059316+07:00"}', drive_id='0AFMU6sBP8cB_Uk9PVA')