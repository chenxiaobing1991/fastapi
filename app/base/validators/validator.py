from ..component import Component

class Validator(Component):
    on:list=[]
    attributes:list=[]
    message:str=''
    def __init__(self,params:dict={}):
        for key,value in params.items():
            if hasattr(self,key):
                setattr(self,key,value)
    @classmethod
    def get_built_in_validators(cls)->dict:
        from .safe_validator import SafeValidator
        from .filter_validator import FilterValidator
        return {
            'filter':FilterValidator,
            'safe':SafeValidator
        }
    def validate_value(self,value):
        return None
    #验证属性
    def validate_attribute(self,cls:Component,attribute):
        message=self.validate_value(getattr(cls,attribute))
        if message is not None:
            cls.set_error(attribute,message)#追加日志

    #验证属性值
    def validate_attributes(self,cls,attributes=None):
        if type(attributes)==list:
            new_attributes=[]
            for value in attributes:
                if value in self.attributes:
                    new_attributes.append(value)
            attributes=new_attributes
        else:
            attribute=self.attributes
        for value in  attributes:
            self.validate_attribute(cls,value)

    @classmethod
    def create_validate(cls,category:str,model,attributes,params:dict={}):
        params['attributes']=attributes
        class_name=None
        if 'class' in params:
            class_name=params['class']
            delattr(params,'class')
        if hasattr(model,category) and callable(getattr(model,category)):#暂未实现
            pass
        elif category in cls.get_built_in_validators():
            class_name=cls.get_built_in_validators()[category]
        else:
            class_name=SafeValidator
        return class_name(params) if class_name is not  None  else None





