import abc
from .component import Component
from .validators.validator import Validator
"""

基础model基类
"""
class Model(Component,metaclass=abc.ABCMeta):

    scenario:str='default'#方案背景
    __validators=None
    """
    规则定义
    """
    def rules(self)->list:
        return []
    #自定义字段
    @classmethod
    def attributes(cls)->list:
        return []
    def get_attributes(self,safe_only:bool=True):
        attributes = self.safe_attributes() if safe_only else self.attributes()
        info={}
        for key in attributes:
            if hasattr(self, key) and getattr(self,key) is not None:
                info[key]=getattr(self,key)
        return info
    """
    方案注册
    """
    def scenarios(self)->dict:
        scenarios={}
        scenarios[self.scenario]=[]
        for validator in self.get_validators():
            for scenario in validator.on:
                scenarios[scenario]={}
        for validator in self.get_validators():
            if len(validator.on)==0:
                for name,value in scenarios.items():
                    for attr in  validator.attributes:
                        scenarios[name].append(attr)
            else:
                for name in validator.on:
                    for attr in validator.attributes:
                        scenarios[name].append(attr)
        return scenarios


    """
    属性定义
    """
    @classmethod
    def attribute_labels(cls)->dict:
        return {

        }
    def get_validators(self)->list:
        if self.__validators is None:
            self.__validators=[]
            for value in self.rules():
                if len(value)>=2:
                    validator=Validator.create_validate(value[1],self,value[0],(value[2] if len(value)>=3 and type(value[2])==dict else {}))
                    self.__validators.append(validator)
        return self.__validators
    #获取确认属性
    def safe_attributes(self)->list:
        return self.scenarios()[self.scenario] if self.scenario in self.scenarios() else []
    #设置对象属性
    def set_attributes(self,params:dict,safe_only:bool=True):
        attributes=self.safe_attributes() if safe_only else self.attributes()
        for key,value in params.items():
            if key in attributes:
                setattr(self, key, value)
    def load(self,params:dict):
        self.set_attributes(params)





