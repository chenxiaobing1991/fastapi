from .provider.csv_provider import Provider as CsvProvider
from .provider.excel_provider import Provider as ExcelProvider
import os
#初始化工厂
class ApplicationFactory:
    __alias={
        'excel':ExcelProvider,
        "csv":CsvProvider
    }
    __successor=None
    def __init__(self,path:str):
        self.path=path
        self.__successor=self.get('excel')#获取默认的调用
    #获取具体的执行引擎
    def get(self,name:str):
        if name not in self.__alias:
            raise Exception('不支持的引擎')
        cls=self.__alias[name]
        return cls(self,self.path)

    def __getattr__(self, name):
        def __call(*args,**kwargs):
            return getattr(self.__successor,name)(*args,**kwargs) if callable(getattr(self.__successor, name)) else getattr(self.__successor,name)
        return __call if hasattr(self.__successor,name) else None



