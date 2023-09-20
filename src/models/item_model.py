from datetime import datetime
from typing import Optional

from sqlalchemy import TIMESTAMP, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer)
    added_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
