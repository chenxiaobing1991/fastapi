


class Component:
    __errors:dict={}#错误日志集合
    __attributes:dict={}
    #追加错误日志
    def set_error(self,key:str,value)->None:
        self.__errors.setdefault(key,value)

    def has_error(self)->bool:
        return True if not bool(self.__errors) else False
    #初始化录入
    def load(self,params:dict):
        self.set_attributes(params)
    def set_attributes(self,values:dict,safeOnly=True):
        # attributes = self.safeAttributes(safeOnly)
        for k,v in values.items():
            if k in attributes:
                setattr(self,k,v)
    #校验
    def validate(self)->bool:
        return True
    #获取所有错误
    def get_errors(self)->dict:
        return self.__errors