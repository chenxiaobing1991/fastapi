from .config import Config
from app.utils.network.response import Response
from app.utils.network.request import Request
import time,hashlib,abc,json
from app.utils.network.client import HttpClient
class AbstractProvider(metaclass=abc.ABCMeta):
    __config: Config
    __driver=None
    def __init__(self,driver, config: Config):
        self.__config = config
        self.__driver=driver

    def get_config(self)->Config:
        return self.__config

    # 请求封装
    def request(self, path: str, method: str, body=None, header={}) -> Response:
        if self.__driver.get('auth').get_access_token() is None:
            return Response(-1,0,{},None,'授权令牌不能为空')
        header={
            'Content-Type':'application/json',
            'Authorization':'Bearer '+self.__driver.get('auth').get_access_token()
        }
        request = Request(method,self.__config.get_graph_uri()+path, header,"{\"query\":\""+body+"\"}")
        return self.handle_response(HttpClient.send_request(request))

    # 返回处理
    def handle_response(self, response: Response) -> Response:
        if response.status_code!=200:
            return response
        response.body=json.loads(response.body)
        return response



