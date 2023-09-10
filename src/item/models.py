from datetime import datetime
from typing import Optional
from database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    added_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    description: Mapped[Optional[str]] = mapped_column(String)
    rating: Mapped[Optional[float]] = mapped_column(Float)
    amount: Mapped[int] = mapped_column(Integer)
    type: Mapped[Optional[str]] = mapped_column(String)
