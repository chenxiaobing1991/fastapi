
import  abc

class Event(metaclass=abc.ABCMeta):

    def __init__(self,name:str,model):
        self.name=name
        self.model=model

    """
    获取执行方法
    """
    def get_method(self)->str:
        return self.name

    def get_model(self):
        return self.model

    def handle(self):
        if hasattr(self.model,self.name) and callable(getattr(self.model,self.name)):
            return getattr(self.model,self.name)(self)
"""
修改前置处理
"""
class BeforeSaveEvent(Event):
    pass

"""
修改后置处理
"""
class AfterSaveEvent(Event):
    pass

class AfterFindEvent(Event):
    pass
