from pydantic import BaseModel
from datetime import datetime
from order.models import OrderStatus


class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    date_of_purchase: datetime
    status: OrderStatus
