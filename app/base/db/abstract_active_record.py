from sqlmodel import asc, desc
from sqlmodel import SQLModel
"""
连接引擎基类
"""
class AbstractActiveRecord:
    def __init__(self, query):
        self.query = query
    __passthru:list=['insert','update','count','delete']
    """
    传递对象
    """
    def set_model(self, model):
        self.model = model
        self.query.set_cls(model.Model)
        return self

    # 封装直接调用query_builder
    def __getattr__(self, name):
        def __call(*args):
            if name in self.__passthru:
                return getattr(self.query, name)(*args)
            getattr(self.query, name)(*args)
            return self
        if hasattr(self.query,name):
            if callable(getattr(self.query,name)):
                return __call
            return getattr(self.query,name)
