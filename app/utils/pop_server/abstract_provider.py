import poplib
from email.parser import Parser
import base64
from email.utils import parseaddr, formataddr
from email.header import decode_header
class AbstractProvider:
    account=None
    password=None
    __server=None
    def __init__(self,account:str,password:str):
        self.account=account
        self.password=password

    #获取账号
    def get_account(self)->str:
        return self.account
    #获取密码
    def get_password(self)->str:
        return self.password

    def get_uri(self):
        pass
    #获取引擎
    def get_server(self):
        if self.__server==None:
            try:
                self.__server=poplib.POP3_SSL(self.get_uri())
                self.__server.set_debuglevel(1)
                self.__server.user(self.account)
                self.__server.pass_(self.password)
            except Exception as e:
                pass
        return self.__server

    #获取邮箱明细列表
    def get_list(self):
        return self.get_server().list()
    #字符串解码
    def __decode_str(self,string):
        value, charset = decode_header(string)[0]
        return value.decode(charset) if charset else value
    #获取邮件明细内容
    def get_info(self,index:int):
        resp, lines, octets = self.get_server().retr(index)
        content = b'\r\n'.join(lines).decode('utf-8')
        email_parser = Parser()
        msg = email_parser.parsestr(content)
        return {
            'from':self.__get_from(msg),
            'to':self.__get_to(msg),
            'subject':self.__get_subject(msg),
            'items':self.__get_items(msg)
        }
    #获取邮件来源
    def __get_from(self,msg)->dict:
        value = msg.get('From', '')
        hdr, addr = parseaddr(value)
        return {
            "name":self.__decode_str(hdr),
            "email":addr
        }
    #获取主题内容
    def __get_subject(self,msg):
        value = msg.get('Subject', '')
        return self.__decode_str(value)
    #获取邮件去向
    def __get_to(self,msg)->dict:
        value = msg.get('To', '')
        hdr, addr = parseaddr(value)
        return {
            "name": self.__decode_str(hdr),
            "email": addr
        }
    def __get_items(self,msg,index=0):
        info={}
        if (msg.is_multipart()):
            parts = msg.get_payload()
            result=[]
            for n, part in enumerate(parts):
                result.append(self.get_items(part,index+1))
            return result

        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                content = content.decode('unicode_escape')
                info['text']=content
            else:
                attachment_data = msg.get_payload(decode=True)
                attachment_filename = msg.get_filename()
                if attachment_filename:
                    info['attachment']={
                        "content_type":content_type,
                        "name":attachment_filename,
                        "content":attachment_data
                    }
        return info

    def __guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

