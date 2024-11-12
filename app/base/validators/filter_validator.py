
from app.base.validators.validator import Validator

class FilterValidator(Validator):

    filt=None
    skip_on_array:bool = False
    skip_on_empty:bool=False
    def __init__(self,params:dict={}):
        super.__init__(params)
        if self.filt is None:
            raise Exception('The "filter" property must be set.')


    def validate_attribute(self,cls,attribute):
        value=getattr(cls,attribute)
        if self.skip_on_array is False:
            self.filt(value)

