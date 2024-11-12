import  abc

class AbstractBuilder(metaclass=abc.ABCMeta):
    connect=None
    def __init__(self,connect):
        self.connect=connect


    def new_query(self):
        return self.__class__(self.connect)