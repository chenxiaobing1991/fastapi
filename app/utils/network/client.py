from .request import Request
from .response import Response
import requests as base_request
import time,abc,paramiko,os,datetime
from ftplib import FTP
#HTTP协议
class HttpClient:

    @classmethod
    def get(cls,url,params,headers)->Response:
        request=Request("get",url,headers,params)
        return cls.send_request(request)


    @classmethod
    def post(cls,url,body,headers)->Response:
        request=Request('POST',url,headers,body)
        return cls.send_request(request)


    @classmethod
    def send_request(cls,request:Request)->Response:
        current_time=time.time()*1000
        result=base_request.request(request.method,request.url,headers=request.header,data=request.body)
        return Response(result.status_code,(time.time()*1000-current_time),request.header,result.text)



#ftp请求
class FtpClient:

    def __init__(self,host:str,username,password,port:int=21):
        self.host=host
        self.username=username
        self.password=password
        self.port=port

    """
    ftp登录
    """
    def login(self):
        try:
            ftp= FTP()
            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)
        except Exception as e:
            return None
        return ftp
    @abc.abstractmethod
    def logout(self)->bool:
        pass
    @abc.abstractmethod
    def get(self,path,local_path):
        path
"""  
sftp客户端
"""
class SftpClient(FtpClient):
    """
    sftp登录
    """
    def login(self):
        try:
            self.transport = paramiko.Transport(self.host, int(self.port))
            self.transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            return None
        return sftp

    """
    sftp退出登录
   """
    def logout(self)->bool:
        if self.driver is not None:
            self.driver.close()
            self.transport.close()
        return True
    """
    遍历目录
    """
    def list(self,path:str='/',is_tree:bool=False):
        result = self.driver.listdir_attr(path)
        print(result)
        data=[]
        for file in result:
            type=2
            if file.st_mode & 0o40000:  # 判断是否为文件夹
                type = 1
                if is_tree==True:
                    data['children']=self.list(path + file.filename,is_tree)
            data.append({'path': path + file.filename, 'type': 2})
        return data

    """
    获取文件到指定位置
    """
    def get(self, path, local_path)->bool:
        try:
            self.driver.get(path,local_path)
        except Exception as e:
            pass
        return os.path.exists(local_path)

