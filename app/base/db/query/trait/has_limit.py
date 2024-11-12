
from ..abstract_builder import AbstractBuilder

class  HasLimit(AbstractBuilder):
    def  __init__(self,connect):
        super().__init__(connect)
        self.limit_nums=None
        self.page_nums=None
        self.offset_nums=None


    def limit(self,nums:int):
        self.limit_nums=nums
        return self

    def page(self,nums):
        self.page_nums=nums
        return self

    def offset(self,nums:int):
        self.offset_nums=nums
        return self

    def get_offset(self):
        return (self.page_nums-1)*self.limit_nums if self.limit_nums is not None and self.page_nums and self.offset_nums is None else self.offset_nums




