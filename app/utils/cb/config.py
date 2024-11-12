
class Config:
    __client_id:str=None
    __client_secret:str=None
    __uri:str=' https://identity.cleverbridge.com'
    __graph_uri:str='https://graph.cleverbridge.com'
    def __init__(self,config:dict):
        self.__client_id=None if 'client_id' not in config else config['client_id']
        self.__client_secret=None if 'client_secret' not in config else config['client_secret']

    def get_client_id(self):
        return self.__client_id

    def get_client_secret(self):
        return self.__client_secret

    def get_uri(self)->str:
        return self.__uri
    def get_graph_uri(self)->str:
        return self.__graph_uri
