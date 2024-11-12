import abc
import os
from app.base.component import Component

"""
文档读取基类
"""
class AbstractProvider(Component,metaclass=abc.ABCMeta):

    def __init__(self, app, path:str):
        self.__app = app
        self.path = path
    def get_app(self):
        return self.__app
    @abc.abstractmethod
    def read(self, **keywords):
        pass
    """
    获取文件后缀    
    """
    def shuffix(self):
        return str(self.path.split('.')[-1]).lower()
