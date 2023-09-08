from datetime import datetime
from database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, Float, String

class Item(Base):
    __tablename__ = "item"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    cost = Column("cost", Integer, nullable=False)
    brand = Column("brand", String, nullable=False)
    size = Column("size", String, nullable=False)
    added_at = Column("added_at", TIMESTAMP, default=datetime.utcnow)
    description = Column("description", String)
    rating = Column("rating", Float)
    amount = Column("amount", Integer)
    type = Column("type", String)