import abc,json,copy
from .abstract_model import AbstractModel
from .event import event
class Model(AbstractModel):
    def get_default_events(self)->dict:
        return {
            'before_save':event.BeforeSaveEvent,
            'after_save':event.AfterSaveEvent,
            'after_find':event.AfterFindEvent
        }
    """
    数据格式化处理
    """
    def hydrate(self,row):
        if type(row)==list:
            result=[]
            for r in row:
                result.append(self.hydrate(r))
            return result
        elif row is not None:
            info=row._asdict()
            model=self.__class__()
            model.attribute=info
            model.sys_original()
            model.is_new_record=False
            return model
        return row

    """
    删除对象
    """
    def delete(self):
        return self.new_query().where(self.get_key()).delete()

    """
    验证是否新的实例化对象
    """
    def get_is_new_record(self)->bool:
        return self.is_new_record
    """
    编辑数据
    """
    def save(self)->bool:
        return self.insert() if self.is_new_record else self.update()
    """
    修改对象数据
    """
    def update(self):
        values = self.get_dirty()
        res=False
        if len(values)>0:
            res=self.new_query().where(self.get_key()).update(values)
            self.sys_original()
        return res

    def insert(self):
        res=self.new_query().insert(self.get_dirty())
        if res is not False and len(self.get_key_name())==1:
            setattr(self,self.get_key_name()[0],res)
            self.sys_original()
        return res

    """
    获取有变化的部分
    """
    def get_dirty(self,attributes:list=[]):
        values={}
        attributes=attributes if len(attributes)>0 else self.attributes()
        for key,value in self.attribute.items():
            if key in attributes and (key not in self.original or value!=self.original[key]):
                values[key]=value
        return values
    """
    获取所有数据对象
    """
    def to_array(self):
        return self.only(self.attributes())
    """
    获取指定的值
    """
    def only(self,columns:list=[])->dict:
        values={}
        for name in columns:
            values[name]=getattr(self,name)
        return values

    """
    同步修改
    """
    def sys_original(self):
        self.original=copy.deepcopy(self.attribute)

    """
    编辑前置处理
    """
    def before_save(self,event):
        pass

    """
    编辑后置处理
    """
    def after_save(self,event):
        pass
    """
    查询后置处理
    """
    def after_find(self,event):
        pass



