import hashlib
import sys
import subprocess
import threading
import os
import math
import time
import email.utils

import requests

from bs4 import BeautifulSoup

# FOLDER_ABS_PATH = 'C:\\Users\\maste\\PycharmProjects\\BrabusUploadWorker\\diablo2.zip'
try:
    FILE_ABS_PATH = sys.argv[1]
    BUCKET_NAME = sys.argv[2]
    # FILE_ABS_PATH = 'C:\\Users\\maste\\PycharmProjects\\BrabusUploadWorker\\nayhayne5.ts'
    # DESTINATION_FOLDER_NAME = 'test'
except IndexError:
    FILE_ABS_PATH = None
    BUCKET_NAME = None


class UploadToGcsWorker(threading.Thread):
    THREAD_COUNT = 6
    CHUNK_SIZE = 256 * 1000 * 1000

    def __init__(self, bucket_name, abs_file_name):
        threading.Thread.__init__(self)
        self.bucket_name = bucket_name
        self.abs_file_path = abs_file_name
        self.file_name = os.path.basename(self.abs_file_path)
        self.access_token = self._get_access_token()
        self.upload_id = self._init_multipart_upload_and_get_upload_id(self.access_token, self.bucket_name,
                                                                       self.file_name)
        self.part_buff_list = self._split_file_into_parts(self.abs_file_path, self.CHUNK_SIZE)
        self.lock = threading.RLock()
        self.etag_map = {}
        self.list_thread = []
        self.latest_chunk_position = 0
        self.file_size = os.path.getsize(self.abs_file_path)

    @staticmethod
    def _get_access_token():
        command_return_obj = subprocess.run('gcloud auth print-access-token'.split(' '), capture_output=True)
        if command_return_obj.returncode == 0:
            return command_return_obj.stdout.decode().strip()
        else:
            return False

    @staticmethod
    def _init_multipart_upload_and_get_upload_id(access_token, bucket_name, file_name):
        if not access_token:
            return False
        endpoint = 'https://storage.googleapis.com/{bucket_name}/{file_name}?uploads'.format(
            bucket_name=bucket_name,
            file_name=file_name,
        )
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token),
            'Content-Type': 'text/csv'
        }
        response = requests.post(endpoint, headers=headers)
        print(response.text)
        if not response.status_code == 200:
            return False
        soup = BeautifulSoup(response.text, 'xml')
        if not soup.find('InitiateMultipartUploadResult').find('UploadId'):
            return False
        return soup.find('InitiateMultipartUploadResult').find('UploadId').get_text()

    @staticmethod
    def _split_file_into_parts(abs_file_path, chunk_size):
        file_size = os.path.getsize(abs_file_path)
        if file_size < chunk_size:
            return [[0, file_size]]
        return_buff_list = [[chunk_size * part + 1, chunk_size * (1 + part)] for part in
                            range(math.ceil(file_size / chunk_size))]
        return_buff_list[len(return_buff_list) - 1][1] = file_size
        return_buff_list[0][0] = 0
        return return_buff_list

    def _generate_xml_to_complete_multipart_upload(self):
        s = BeautifulSoup(features='html.parser')
        root_tag = s.new_tag('CompleteMultipartUpload')
        for part in sorted(self.etag_map):
            part_tag = s.new_tag('Part')
            part_number = s.new_tag('PartNumber')
            etag = s.new_tag('ETag')
            part_number.string = str(part)
            etag.string = self.etag_map[part]
            part_tag.append(part_number)
            part_tag.append(etag)
            root_tag.append(part_tag)
        soup = BeautifulSoup(str(root_tag), "xml")
        return soup.prettify()

    def _submit_uploaded_object(self):
        print('Start submit finished object')
        endpoint = 'https://storage.googleapis.com/' + \
                   '{bucket_name}/{file_name}?uploadId={upload_id}'.format(
                       bucket_name=self.bucket_name,
                       file_name=self.file_name,
                       upload_id=self.upload_id
                   )
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
            'Content-Type': 'application/xml',
            'Host': 'storage.googleapis.com',
            'Date': email.utils.formatdate(usegmt=True)
        }
        test = self._generate_xml_to_complete_multipart_upload()
        return requests.post(endpoint, data=test, headers=headers)

    def _make_put_request_to_upload_chunked_file(self, access_token, bucket_name, file_name, part_number, upload_id
                                                 , chunk_data, retry_time=0):
        endpoint = 'https://storage.googleapis.com/' + \
                   '{bucket_name}/{file_name}?partNumber={part_number}&uploadId={upload_id}'.format(
                       bucket_name=bucket_name,
                       file_name=file_name,
                       part_number=part_number,
                       upload_id=upload_id,
                   )
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token),
        }
        re = requests.put(endpoint, data=chunk_data, headers=headers)
        if re.status_code == 200 and re.headers.get('ETag').replace('\"', '') == hashlib.md5(chunk_data).hexdigest():
            with self.lock:
                self.etag_map[part_number] = re.headers.get('ETag')
        else:
            if retry_time == 5:
                print('Error on upload chunk will abort')
                os.abort()
            print('Error on upload chunk will retry {}/5'.format(retry_time + 1))
            self._make_put_request_to_upload_chunked_file(access_token, bucket_name, file_name, part_number,
                                                          upload_id, chunk_data, retry_time + 1)

    @staticmethod
    def read_in_chunks(file_object, chunk_size=CHUNK_SIZE):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def check_file_is_existed(self) -> bool:
        endpoint = 'https://storage.googleapis.com/{}?acl'.format(self.file_name)
        headers = {
            'Authorization': 'Bearer {access_token}'.format(access_token=self.access_token),
            'Host': '{}.storage.googleapis.com'.format(self.bucket_name),
        }
        re = requests.get(endpoint, headers=headers)
        if re.status_code != 200:
            return False
        return True

    def run(self):
        if self.check_file_is_existed():
            return
        if self.upload_id:
            with open(self.abs_file_path, 'rb') as f:
                part = 1
                total_uploaded = 0
                while True:
                    chunk_data = f.read(self.CHUNK_SIZE)
                    if not chunk_data:
                        break
                    while len(self.list_thread) >= self.THREAD_COUNT:
                        self.list_thread = [thread for thread in self.list_thread if thread.is_alive()]
                        time.sleep(0.01)
                    upload_parts_worker = threading.Thread(
                        target=self._make_put_request_to_upload_chunked_file,
                        args=[
                            self.access_token,
                            self.bucket_name,
                            self.file_name,
                            part,
                            self.upload_id,
                            chunk_data
                        ]
                    )
                    upload_parts_worker.start()
                    self.list_thread.append(upload_parts_worker)
                    part += 1
                    total_uploaded += len(chunk_data)
            f.close()
            for t in self.list_thread:
                t.join()

            # Check total part in happy case vs real equal
            if math.ceil(self.file_size / self.CHUNK_SIZE) == len(self.etag_map):
                print('Total upload part checked ok')
                response = self._submit_uploaded_object()
                print(response.status_code, 'Return status code', response.text)
            else:
                print('Missing some part of file')
                pass
        else:
            print('Token error')


if FILE_ABS_PATH and BUCKET_NAME:
    worker = UploadToGcsWorker(BUCKET_NAME, FILE_ABS_PATH)
    worker.start()
else:
    print('Please specify abs path, bucket name and destination folder name of upload file')
