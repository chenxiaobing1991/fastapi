from app.base.db.model import Model
from datetime import datetime
from sqlmodel import Field,SQLModel
"""
节点数据列表
"""
class NodeListModel(Model):
    class Model(SQLModel,table=True):
        __tablename__ = "sale_node_list"  # 自定义表名
        id: str = Field(primary_key=True)
        is_successor: int = 0
        node_id: int
        values: str
        created_at: datetime = datetime.now()