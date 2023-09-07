from typing import AsyncGenerator
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, Float, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Base(AsyncAttrs, DeclarativeBase):
    pass

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

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
