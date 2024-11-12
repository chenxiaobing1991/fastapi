
from .config import Config
from app.config.co import config as config_data
from .provider.auth_token import AuthToken
from .provider.product_provider import ProductProvider
from .provider.order_provider import OrderProvider
class ApplicationFactory:
    __config:Config

    __alias={
        'auth':AuthToken,
        'product':ProductProvider,
        'order':OrderProvider
    }
    __provider={}
    def __init__(self):
        self.__config=Config(config_data)
    #获取引擎
    def get(self,name:str):
        if name in self.__provider:
            return self.__provider[name]
        if name not in self.__alias:
            raise Exception('不支持的第三方引擎')
        cls=self.__alias[name]
        self.__provider[name]=cls(self,self.__config)
        return self.__provider[name]
