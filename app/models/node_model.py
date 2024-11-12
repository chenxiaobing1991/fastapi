from app.base.db.model import Model
from sqlmodel import Field
from datetime import datetime
from sqlmodel import SQLModel
"""

节点管理
"""
class NodeModel(Model):
    class Model(SQLModel,table=True):
        __tablename__ = "sale_nodes"  # 自定义表名
        name: str
        nums: int = 0
        total_nums: int = 0
        status: int = 0
        supplier: str
        id: int = Field(primary_key=True)
        created_at: datetime = datetime.now()
