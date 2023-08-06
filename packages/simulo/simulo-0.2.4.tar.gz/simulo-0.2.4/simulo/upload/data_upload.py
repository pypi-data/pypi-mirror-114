
from simulo.utils import unique_id as uid_util
from simulo.utils import json_transformations as json_t
from simulo.auth.authenticator import AuthInfo, Authenticate
from uuid import UUID
from simulo import config
from pathlib import Path 
import math
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class DataAgentInfo(object):
    def __init__(self):
        self.uid = 'test'
        self.ip_address = '1.1.1.2'
        self.app_name = "Simulo SDK"


class DataUploadClient:
    def __init__(self):
        self._session_map = dict()

    def create_session(self, files_lists: list, type_of_files: str, auth_info: AuthInfo):
        """
        Creates the session in the backend
        :param all_files: list of list of files to upload (nested/2D list of files)
        :param type_of_files: Type of file being uploaded: DICOM, NIFTI, etc.
        :param auth_info: Authentication info
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session_id = self._initialize_session(files_lists, type_of_files)
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        # call rest api to create the session
        response = requests.post(config.BASE_IMG_UPLD_URL + 'session-create', json=session_camel_case, headers=headers, verify=config.VERIFY_CERTIFICATE)
        return {'session_id': session_id, 'status_code': response.status_code}

    def start_session(self, session_id: str, auth_info: AuthInfo):
        """
        Starts the session corresponding to the session id
        :param session_id: unique id of the session
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        # call rest api to start the session
        response = requests.put(config.BASE_IMG_UPLD_URL + 'session-start', json=session_camel_case, headers=headers, verify=config.VERIFY_CERTIFICATE)
        return {'status_code': response.status_code}

    def resume_session(self, session_id: str, auth_info: AuthInfo):
        """
        Resumes the session corresponding to the session id
        :param session_id: unique id of the session
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        # call rest api to resume the session
        response = requests.put(config.BASE_IMG_UPLD_URL + 'session-resume', json=session_camel_case, headers=headers, verify=config.VERIFY_CERTIFICATE)
        return {'status_code': response.status_code}

    def cancel_session(self, session_id: str, auth_info: AuthInfo):
        """
        Cancels the session corresponding to the session id
        :param session_id: unique id of the session
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        # call rest api to cancel the session
        response = requests.put(config.BASE_IMG_UPLD_URL + 'session-cancel', json=session_camel_case, headers=headers, verify=config.VERIFY_CERTIFICATE)
        return {'status_code': response.status_code}
        

    def end_session(self, session_id: str, auth_info: AuthInfo):
        """
        Ends the session corresponding to the session id
        :param session_id: unique id of the session
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        # call rest api to end the session
        response = requests.put(config.BASE_IMG_UPLD_URL + 'session-end', json=session_camel_case, headers=headers, verify=config.VERIFY_CERTIFICATE)
        return {'status_code': response.status_code}

    def send_files(self, session_id: str, auth_info: AuthInfo):
        """
        Uploads the files in the session corresponding to the session id
        :param session_id: unique id of the session
        :return: dict - a map containing response code and other values including unique id of the session

        """
        session = self._session_map[session_id]
        api_prep = self._prepare_api_request(session, auth_info)
        #session_camel_case = api_prep['session_camel_case']
        headers = api_prep['headers']
        for file_id, file_info in session['fileMap'].items():
            if (file_info['transmittedFlag']):
                continue
            else:
                orig_file_handle = session['origFileHandleMap'][file_id]
                print("sending file {0} with {1} chunk(s)...".format(orig_file_handle, file_info['totalChunks']), end = '')
                start = 0
                end = 0
                for i in range (file_info['totalChunks']):
                    chunkInfo = file_info['chunks'][i]
                    if (chunkInfo['transmittedFlag']): 
                        continue
                    fd = {}
                    start = 0 if (i == 0) else (start + file_info['chunks'][i - 1]['size'])
                    end = start + chunkInfo['size']
                    file_object = open(orig_file_handle, 'rb')
                    blob = next(self._read_in_chunks(file_object, start, end))

                    form = MultipartEncoder({
                        "file": (chunkInfo['name'], blob, "application/octet-stream"),
                        "chunkLength": str(len(blob)),
                        "sessionId": session['sessionId']
                    })
                    # upload chunk
                    formDataHeaders = {
                        'Authorization': headers['Authorization'],
                        'X-Sim-HomeOrgId': headers['X-Sim-HomeOrgId'],
                        'Content-Type': form.content_type
                    }
                    response = requests.post(config.BASE_IMG_UPLD_URL + session['sessionId'], data=form, headers=formDataHeaders, verify=config.VERIFY_CERTIFICATE)
                    if response.status_code == 200:
                        chunkInfo['transmittedFlag'] = True
                        print('chunk {0} done...'.format(i), end='')
                        file_info['transmittedFlag'] = True #assume whole file submitted
                        for ci in file_info['chunks']:
                            if not ci['transmittedFlag'] == True:
                                file_info['transmittedFlag'] = False # turn the flag back to False if assumption is false
                                break
                        if file_info['transmittedFlag'] == True:
                            print('done.')
                    else:
                        print('failed.')
        # if any of the files failed to transmit inform the user                
        for file_id, file_info in session['fileMap'].items():
            if not (file_info['transmittedFlag']):
                return False
        # return true by default
        return True

    def _prepare_api_request(self, session: dict, auth_info: AuthInfo):
        session['orgId'] = auth_info.user_home_org_id
        session_camel_case = json_t.convert_json(session, json_t.underscore_to_camel)
        # print(session_json)
        headers = {
            'Authorization': '{0} {1}'.format(auth_info.token_type, auth_info.token),
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'X-Sim-HomeOrgId': str(session['orgId'])
        }
        return {'session_camel_case': session_camel_case, 'headers': headers}

    def _initialize_session(self, files_lists: list, type_of_files: str):
        """
        Initialize the session.
        :param all_files: list of list of files to upload (nested/2D list of files)
        :param type_of_files: Type of file being uploaded: DICOM, NIFTI, etc.
        :return: UUID - unique id of the session

        """
        all_files = [item for sublist in files_lists for item in sublist] #flattens the 2D list
        dai = DataAgentInfo() # all hardcoded values for now
        session_id = str(uid_util.generate_uuid4())
        data_send_session = {
            'sessionState': 'STARTED',
            'sessionId': session_id,
            'dataAgentInfo': dai.__dict__,
            'typeOfFiles': type_of_files,
            'totalBytesToBeTransmitted': self._get_bytes_to_be_transmitted(all_files),
            'totalFilesToBeTransmitted': len(all_files)
        }
        self._session_map[session_id] = data_send_session
        self._initialize_file_lookups(session_id, files_lists)
        return session_id

    def _initialize_file_lookups(self, session_id: UUID, files_lists: list):
        data_send_session = self._session_map[session_id]
        data_send_session['fileMap'] = {}
        data_send_session['progressMap'] = {}
        data_send_session['origFileHandleMap'] = {}
        for cid in range(len(files_lists)):
            files = files_lists[cid]
            data_send_session['progressMap'][cid] = { 'files': [], 'progress': 0 }
            for i in range(len(files)):
                file = files[i] # this is the name of the file
                fileId = str(uid_util.generate_uuid4())
                file_size = os.path.getsize(file)
                data_file_info = {
                    'fileId':  fileId,
                    'originalName': Path(file).name,
                    'name': "{0}_{1}_{2}".format(session_id, cid, i),
                    'size': file_size,
                    'totalChunks': math.ceil(file_size / config.CHUNK_UPLOAD_SIZE),
                    'transmittedFlag': False,
                    'collectionID': cid,
                    'chunks': [],
                    'progress': 0
                }
                for j in range(data_file_info['totalChunks']):
                    chunk_info = {}
                    chunk_info['chunkNumber'] = j + 1
                    chunk_info['name'] = "{0}_{1}".format(data_file_info['name'], chunk_info['chunkNumber'])
                    remaining_file_size = data_file_info['size'] - (j * config.CHUNK_UPLOAD_SIZE)
                    chunk_info['size'] = config.CHUNK_UPLOAD_SIZE if (remaining_file_size > config.CHUNK_UPLOAD_SIZE) else remaining_file_size
                    chunk_info['transmittedFlag'] = False
                    data_file_info['chunks'].append(chunk_info)
                data_send_session['fileMap'][fileId] = data_file_info
                prog_map_coll_dict = data_send_session['progressMap'][cid]
                prog_map_coll_dict['files'].append(data_file_info)
                prog_map_coll_dict['collectionSizeInBytes'] =  0 if 'collectionSizeInBytes' not in prog_map_coll_dict else prog_map_coll_dict['collectionSizeInBytes']
                prog_map_coll_dict['collectionSizeInBytes'] += os.path.getsize(file)
                data_send_session['origFileHandleMap'][fileId] = file

    def _get_bytes_to_be_transmitted(self, files):
        total_bytes = sum(os.path.getsize(f) for f in files if os.path.isfile(f))
        return total_bytes

    def _read_in_chunks(self, file_object, offset_bytes, chunk_size):
        """Lazy function (generator) to read a file piece by piece."""
        file_object.seek(offset_bytes)
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def to_string(self) -> str:
        """
        Returns a string representation of the object
        :return: string representation of the object

        :example:

        >>> str1 = to_string()
        """
        return "My session id is {0}.".format(list(self._session_map.keys())[0])

