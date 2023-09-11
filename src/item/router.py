from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from item.models import Item
from item.schemas import ItemCreate
from item.service import ItemService

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/add", response_model=ItemCreate)
async def add_item(
    new_item: ItemCreate, session: AsyncSession = Depends(get_async_session)
):
    return await ItemService.add(new_item, session)


@router.get("/get", response_model=ItemCreate)
async def get_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    return await ItemService.get(item_id, session)


@router.get("/count")
async def count_items(session: AsyncSession = Depends(get_async_session)):
    return await ItemService.count(session)


@router.delete("/delete")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    return await ItemService.delete(item_id, session)
