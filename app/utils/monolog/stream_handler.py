import logging
import os
import datetime
class StreamHandler:
    __filename:str
    __level=None
    __format=None
    def __init__(self,filename:str,level='INFO'):
        self.__filename=filename
        self.__level=level
        self.__format=format
        self.__load()
    def __load(self):
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)
        os.chmod(os.path.dirname(self.__filename),0o777)
        dirname=os.path.dirname(self.__filename)+'/'+str(datetime.datetime.now().date())
        os.makedirs(dirname, exist_ok=True)
        os.chmod(dirname, 0o777)
        self.__filename=dirname+'/'+os.path.basename(self.__filename)

    def info(self,msg):
        now=datetime.datetime.now()
        error=f'[{now}] {self.__level} {msg}]\r\n'
        with open(self.__filename, "a") as file:
            file.write(error)
        return True


