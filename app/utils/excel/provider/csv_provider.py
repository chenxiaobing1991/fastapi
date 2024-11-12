import pandas as pd
from ..abstract_provider import AbstractProvider


# 读取csv
class Provider(AbstractProvider):
    # 读取csv
    def read(self, **kwargs):
        if self.shuffix() not in ['csv']:
            raise Exception('不支持的引擎')
        try:
            fd=pd.read_csv(self.path,encoding='utf-8',low_memory=False)
        except Exception as e:
            fd=pd.read_csv(self.path,encoding='latin1',low_memory=False)
        finally:
            return fd
