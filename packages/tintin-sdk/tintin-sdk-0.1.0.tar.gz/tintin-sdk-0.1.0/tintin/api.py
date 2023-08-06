import requests

from tintin.auth import MinioAuth
from tintin.env import Environ

def _strip_leading_slash(str):
    if str.startswith('/'):
        return str[len('/'):] # strip leading '/'
    if str.startswith('./'):
        return str[len('./'):] # strip leading './'
    return str

class TintinApi():
    def __init__(self, host: str, env: Environ):
        self.env = env
        self.host = host

    def _token(self):
        return self.env.minio_token_name

    def _api(self):
        return self.host
 
    def get(self, uri: str):
        url = '{}/{}'.format(self._api(), _strip_leading_slash(uri))
        return requests.get(url, auth=MinioAuth(self._token()))

    def put(self, uri: str, data):
        url = '{}/{}'.format(self._api(), _strip_leading_slash(uri))
        return requests.put(url, data=data, headers={'Content-Type':
            'application/octet-stream'}, auth=MinioAuth(self._token()))
