from ..abstract_builder import AbstractBuilder


"""
查询部分
"""
class HasAttributes(AbstractBuilder):
    def __init__(self,connect):
        super().__init__(connect)
        self.columns=['*']

    """
    设置查询过滤字段
    """
    def select(self,columns:list):
        self.columns=columns
        return self
    
    def select_raw(self,columns:str):
        self.add_select(columns)
        return self

    def add_select(self,columns):
        if type(columns)==list:
            self.columns=self.columns.extend(columns)
        elif type(columns)==str:
            self.columns.append(columns)
        return self



