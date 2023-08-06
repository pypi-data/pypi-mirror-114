from simulo.utils import unique_id as uid_util
from simulo.utils import json_transformations as json_t
from uuid import UUID
from simulo import config
import math
import os
import requests
import jwt

class AuthInfo(object):
    def __init__(self):
        self.username = None
        self.user_home_org_id = -1
        self.operating_org_id = -1
        self.token = None
        self.token_type = 'bearer'
        self.auth_success = False
        self.error_message = None


class Authenticate:
    def __init__(self):
        self._auth_info = None

    def login(self, username: str, password: str):
        """
        Attempts to log a user in
        :param username: the username to use to login
        :param password: the password to use to login
        :return: AuthInfo the object containing various auth related info
        """
        self._auth_info = AuthInfo()
        if not username or not password:
            self._auth_info.auth_success = False
            self._auth_info.error_message = "You must suppy a valid username or password to continue"
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json'
        }
        response = requests.post(config.BASE_ACCT_MGMT_URL + 'login', json={'Username': username, 'Password': password}, headers=headers, verify=config.VERIFY_CERTIFICATE)
        if response.status_code == 200:
            self._auth_info.username = response.json()["username"]
            self._auth_info.token = response.json()["token"]
            self._auth_info.auth_success = True
            decoded_token = jwt.decode(self._auth_info.token, options={"verify_signature": False})
            self._auth_info.user_home_org_id = [int(i) for i in decoded_token["BelongsToOrgIds"].split(',')][0] # take the first one, but this needs to change to have it be picked up from backend
            self._auth_info.operating_org_id = [int(i) for i in decoded_token["BelongsToOrgIds"].split(',')][0] # take the first one, but this needs to change to have the user pick the desired org
            #print (decoded_token)
        elif response.status_code == 404:
            self._auth_info.auth_success = False
            self._auth_info.error_message = "API route is not valid"
        else:
            self._auth_info.auth_success = False
            response.json()["message"]

        return self._auth_info
