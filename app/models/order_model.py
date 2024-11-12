from app.base.db.model import Model
from datetime import datetime
from sqlmodel import Field,SQLModel
from decimal import Decimal
from datetime import datetime
"""
订单管理
"""
class OrderModel(Model):

    class Model(SQLModel,table=True):
        __tablename__ = "sale_orders"  # 自定义表名
        id: int = Field(primary_key=True)
        order_id: int=0  # 第三方订单
        product_id:int=0
        platform: str = '2checkout'
        product_name: str
        product_version: str
        quantity: int = 1
        net_profit_converted: Decimal
        gross_price: Decimal='0.00'
        is_renewal: int
        hash_id:str
        status: str = 'Completed'
        link_id: str = None
        finish_at: datetime = None
        created_at: datetime = datetime.now()