import app.config.cb as cb
from .config import Config
from .provider.product_provider import ProductProvider
from .provider.auth_token import AuthToken
class ApplicationFactory:
    __config:Config
    __alias={
        'product':ProductProvider,
        'auth':AuthToken
    }
    __provider={}
    def __init__(self):
        self.__config=Config(cb.config)

    def get(self,name:str):
        if name in self.__provider:
            return self.__provider[name]
        if name not in self.__alias:
            raise Exception('不支持的引擎')
        cls=self.__alias[name]
        self.__provider[name]=cls(self,self.__config)
        return self.__provider[name]
