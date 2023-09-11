from typing import Literal, get_args, Optional
from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Enum

from database import Base


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    permission: Mapped[Optional[str]] = mapped_column(String)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    username: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


OrderStatus = Literal["Pending", "Shipped", "Delivered", "Canceled", "Refunded"]


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
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
