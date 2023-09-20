from datetime import datetime

from pydantic import BaseModel, Field

from models.order_model import OrderStatus


class OrderUserSchema(BaseModel):
    item_id: int = Field(ge=0)


class OrderCreateSchema(OrderUserSchema):
    date_of_purchase: datetime
    status: OrderStatus
    user_id: int = Field(ge=0)


class OrderDBSchema(OrderCreateSchema):
    id: int = Field(ge=0)
