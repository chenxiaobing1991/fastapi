
#自定义请求类
class Request:
    __timeout:int=50
    def __init__(self,method,url,header,body):
        self.method=method.upper()
        self.url=url
        self.header=header
        self.body=body
    #设置超时时间
    def setTimeOut(self,num:int)->None:
        self.__timeout=num

    def getTimeOut(self)->int:
        return self.__timeout

    def toArray(self)->dict:
        return {
            'method':self.method,
            'url':self.url,
            'headers':self.header,
            'body':self.body
        }
