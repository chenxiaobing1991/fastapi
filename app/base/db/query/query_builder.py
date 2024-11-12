from sqlmodel import  select,asc,desc,text,table,update,Field
from .trait import  has_limit,hash_filter,hash_attributes
from .abstract_builder import AbstractBuilder
from app.utils.application_context import ApplicationContext
from app.utils.monolog.logger_factory import LoggerFactory
"""
query  table连接池
"""
class QueryBuilder(hash_attributes.HasAttributes,hash_filter.HasFilter,has_limit.HasLimit,AbstractBuilder):
    __cls__=None
    events=['first']
    def __init__(self,connect):
        super().__init__(connect)
        self.orders={}
        self.groups=[]
    """
    设置表名
    """
    def set_cls(self,cls):
        self.__cls__=cls
        return self
    #设置排序字段
    def order_by(self,column,direction='asc'):
        self.orders[column]=direction
        return self
    def order_by_desc(self,column):
        return self.order_by(column,'desc')

    #设置分组
    def group_by(self,*groups):
        for group in groups:
            self.groups.append(group)
        return self

    #获取sql
    def to_sql(self):
        query=select(table(str(self.__cls__.__table__)),text(','.join(str(arg) for arg in self.columns)))
        if hasattr(self,'orders'):
            for key, value in self.orders.items():
                key=text(key)
                query = query.order_by(asc(key) if value == 'asc' else desc(key))
        if hasattr(self, 'groups'):
            for value in self.groups:
                query = query.group_by(text(value))
        return self.filter(query)
    def count(self):
        query = self.filter(self.connect.query(self.__cls__))
        count= query.count()
        return count

    """
    获取条件数据
    """
    def all(self):
        def call():
            query=self.to_sql()
            if hasattr(self,'limit_nums'):
                query=query.limit(self.limit_nums)
            if hasattr(self,'offset_nums'):
                query=query.offset(self.offset_nums)
            return self.connect.execute(query).all()
        return self.__call(call)
    """
    查看单条数据
    """
    def first(self):
        result =self.limit(1).all()
        return result[0] if type(result)==list and len(result)>0 else result
    """
    
    """
    def insert(self,values):
        if type(values)==list:
            return self.insert_all(values)
        def call(values):
            model = self.__cls__(**values)
            self.connect.add(model)
            self.connect.commit()
            id = getattr(model, self.__cls__.__table__.primary_key.columns.keys()[0])
            self.connect.close()
            return id
        return self.__call(call,values)
    """
    批量添加
    """
    def insert_all(self,values):
        if type(values)!=list:
            raise Exception('数据结构不正确')
        def call(values):
            result = [self.__cls__(**args) for args in values]
            self.connect.add_all(result)
            self.connect.commit()
            self.connect.close()
            return True
        return self.__call(call, values)

    """
    修改数据对象
    """
    def update(self,values:dict):
        def call(values):
            query = self.filter(self.__connect.query(self.__cls__))
            info = {}
            for key, value in values.items():
                info[getattr(self.__cls__, key)] = value
            query.update(info)
            self.connect.commit()
            self.connect.close()
            return True
        return self.__call(call,values)

    def get_logger(self):
       return ApplicationContext.getContainer(LoggerFactory).get('default')

    """
    删除数据
    """
    def delete(self):
        def call():
            query = self.filter(self.connect.query(self.__cls__))
            query.delete()
            self.connect.commit()
            self.connect.close()
        return self.__call(call)

    def __call(self,callback,*args):
        try:
            return callback(*args)
        except Exception as e:
            self.get_logger().info(e)
            return None









