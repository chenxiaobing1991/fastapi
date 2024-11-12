from ..config import Config
import os
import time
import json
import hashlib
from urllib.parse import urlencode
from app.utils.network.client import HttpClient
from ..abstract_provider import AbstractProvider
class AuthToken(AbstractProvider):
    __access_token_file: str
    __info = {}
    def __init__(self,driver, config: Config):
        super().__init__(driver,config)
        md5 = hashlib.md5()
        md5.update(self.get_config().get_client_id().encode('utf-8'))
        self.__access_token_file = 'runtime/access_token_' + md5.hexdigest() + '.txt'
        self.__load()

    def __load(self):
        if os.path.exists(self.__access_token_file) is True:
            file = open(self.__access_token_file, 'rb')
            info = file.read()
            info = json.loads(info)
            if type(info) == dict:
                self.__info = info
    #获取过期时间
    def get_expire_at(self):
        return 0 if 'expire_time' not in self.__info else self.__info['expire_time']
    # 获取token令牌
    def get_access_token(self):
        if (self.get_expire_at() < time.time()):
            body = {
                'grant_type': 'client_credentials',
                'scope': 'GQL',
                'client_id': self.get_config().get_client_id(),
                'client_secret': self.get_config().get_client_secret()
            }
            response=HttpClient.post(self.get_config().get_uri()+'/connect/token',urlencode(body),{'Content-type': 'application/x-www-form-urlencoded'})
            if response.status_code==200:
                self.__info=json.loads(response.body)
                expire_in = self.__info['expires_in'] if 'expires_in' in self.__info else 0
                self.__info['expire_time'] = time.time() + expire_in
                with open(self.__access_token_file, "w") as file:
                    file.write(json.dumps(self.__info))
        return None if 'access_token' not in self.__info else self.__info['access_token']

