import abc
from ..model import Model as BaseModel
from sqlmodel import SQLModel
from .model_builder import ModelBuilder
from .query import query_builder,connect_resolver
from app.utils.application_context import ApplicationContext
class AbstractModel(BaseModel,metaclass=abc.ABCMeta):
    is_new_record: bool = True
    connect: str = 'default'
    def __init__(self):
        self.attribute = {}
        self.original = {}
        self.is_new_record=True
    def __repr__(self):
        return f"is_new_record={self.is_new_record} original={self.original} attribute={self.attribute}"

    def __setattr__(self,name,value):
        if name in self.attributes():
            self.attribute[name]=value
            return
        super().__setattr__(name, value)
    def __getattr__(self, name):
        if name in self.attribute:
            return self.attribute[name]
        method='get_'+name
        if hasattr(self,method) and callable(getattr(self,method)):
            return getattr(self,method)()
        super().__getattr__(name)
    class Model(SQLModel):
        pass

    """
       主键内容
       """

    @classmethod
    def get_key_name(cls) -> list:
        return cls.Model.__table__.primary_key.columns.keys()

    """
    获取表名
    """

    @classmethod
    def table_name(cls) -> str:
        return cls.Model.__table__

    """
    主键值
    """

    def get_key(self):
        return self.only(self.get_key_name())

    """
    获取连接池
    """

    def get_connect(self):
        SessionLocal = ApplicationContext.getContainer(connect_resolver.ConnectionResolver).connect(self.connect)
        with SessionLocal() as session:
            return session
        return None

    """
    初始化对象
    """

    @classmethod
    def query(cls):
        return cls().new_query()

    """
    新model query
    """

    def new_query(self):
        return ModelBuilder(self.new_query_builder()).set_model(self)

    """
    连接池会话
    """
    def new_query_builder(self):
        return query_builder.QueryBuilder(self.get_connect())
    """
    数据模型的字段管理
    """
    @classmethod
    def attributes(cls) -> list:
        return cls.Model.__table__.columns.keys()

    @classmethod
    def find_one(cls, id):
        if type(id) != dict:
            id = {cls.get_key_name()[0]: id}
        return cls.query().where(id).first()

    @classmethod
    def first_or_new(cls, filter: dict):
        model = cls.find_one(filter)
        if model is None:
            model = cls()
            model.set_attributes(filter, False)
        return model
