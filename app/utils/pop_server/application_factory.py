from .provider.one_sex_three_provider import OneSexThreeProvider
from .provider.qq_provider import QQProvider
class ApplicationFactory:
    __account=None
    __password=None
    __provider={}
    __alias={
        '163':OneSexThreeProvider,
        'qq':QQProvider
    }
    def  __init__(self,account:str,password:str):
        self.__account=account
        self.__password=password
    #实例化引擎
    def  get(self,name:str):
        if name in self.__provider:
            return self.__provider[name]
        if name not in self.__alias:
            raise Exception('不存在的对象引擎')
        class_name=self.__alias[name]
        return class_name(self.__account,self.__password)

