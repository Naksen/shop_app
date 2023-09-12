from typing import Literal, get_args
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Enum
from database import Base
from datetime import datetime

OrderStatus = Literal["Pending", "Shipped", "Delivered", "Canceled", "Refunded"]


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    date_of_purchase: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            *get_args(OrderStatus),
            name="orderstatus",
            create_constraint=True,
            validate_strings=True,
        )
    )
