from app.config.logger import config as configs
import os
from app.utils.monolog.stream_handler import StreamHandler
class LoggerFactory:

    __loggers={}
    def __init__(self):
       pass

    def __handler(self,config:dict):
        if 'level' not in config:
            raise Exception(f'logger config[{name}] level is not defined.')
        if 'filename' not in config:
            raise Exception(f'logger config[{name}] filename is not defined.')
        cls=StreamHandler if 'class' not in config else config['class']
        return cls(config['filename'],config['level'])

    def make(self,name:str):
        if name not in configs:
            raise Exception(f'logger config[{name}] is not defined.')
        config=configs[name]
        return self.__handler(config)

    #获取日志引擎
    def get(self,name:str):
        if name in self.__loggers:
            return self.__loggers[name]
        self.__loggers[name]=self.make(name)
        return self.__loggers[name]
