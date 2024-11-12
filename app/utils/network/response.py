

class Response:
    status_code:int=200
    duration=0
    headers={}
    body=None
    error:str
    request=None
    def __init__(self,status_code,duration,headers={},body=None,error_msg=None,request=None):
        self.status_code=status_code
        self.duration=duration
        self.headers=headers
        self.body=body
        self.error_msg=error_msg
        self.request=request

    def toArray(self)->dict:
        return {
            'status_code':self.status_code,
            'duration':self.duration,
            'headers':self.headers,
            'body':self.body,
            'error_msg':self.error_msg,
            'request':self.request
        }