from ..abstract_provider import AbstractProvider
import pandas as pd
import os
#读取excel
class Provider(AbstractProvider):
    """
    获取pd对象
    """
    def read(self,**kwargs):
        if self.shuffix() not in ['xlsx','xls']:
            return self.get_app().get('csv').read(**kwargs)
        return pd.read_excel(self.path,**kwargs)