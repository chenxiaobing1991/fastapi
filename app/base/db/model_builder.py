from .abstract_active_record import AbstractActiveRecord
from app.utils.application_context import ApplicationContext
"""
数据模型与query_builder中间层
"""

class ModelBuilder(AbstractActiveRecord):
    """
    查询单条数据
    """
    def first(self):
        return self.model.hydrate(self.query.first())

    """
    查询列表数据
    """
    def all(self):
        return self.model.hydrate(self.query.all())
    def count(self):
        return self.query.count()




