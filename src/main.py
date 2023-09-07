from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from database import get_async_session, Item as Item_table
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    cost: int
    brand: str
    size: str
    added_at: datetime
    description: str
    rating: float
    amount: int
    type: str

@app.post("/items")
async def add_item(new_item: Item, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Item_table).values(**new_item.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@app.get("/")
async def root():
    return {"message": "Hello World"}