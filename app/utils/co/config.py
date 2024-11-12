


class Config:
    __merchant_code:str
    __secret_key:str
    __uri='https://api.2checkout.com'
    def __init__(self,config:dict):
        self.__secret_key=config['secret_key'] if 'secret_key' in config else ''
        self.__merchant_code=config['merchant_code'] if 'merchant_code' in config else ''


    def get_merchant_code(self)->str:
        return self.__merchant_code

    def get_secret_key(self)->str:
        return self.__secret_key

    def get_uri(self)->str:
        return self.__uri