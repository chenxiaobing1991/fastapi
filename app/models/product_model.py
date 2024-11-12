from app.base.db.model import Model
from datetime import datetime
from sqlmodel import Field,SQLModel
from decimal import Decimal
"""
产品管理
"""
class ProductModel(Model):

    """
    数据模型配置
    """
    class Model(SQLModel,table=True):
        __tablename__ = "sale_products"  # 自定义表名
        id: str = Field(primary_key=True)
        name: str
        code: str = ''
        supplier: str
        version: str = ''
        pid: str = ''
        addr: str = None
        price:Decimal='0.00'
        created_at: datetime = datetime.now()