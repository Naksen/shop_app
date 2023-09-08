from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from item.models import Item
from item.schemas import ItemCreate

router = APIRouter(
    prefix="/item",
    tags=["Item"]
)

@router.post("", response_model=ItemCreate)
async def add_item(new_item: ItemCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Item).values(**new_item.model_dump())
        await session.execute(stmt)
        await session.commit()
        return new_item
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None,
        })
    
@router.get("", response_model=list[ItemCreate])
async def get_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Item).where(Item.id == item_id)
        result = await session.execute(query)
        res = result.scalars().all()
        return res
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None,
        })