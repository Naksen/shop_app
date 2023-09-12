import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from item.schemas import ItemCreate
from item.service import ItemService

router = APIRouter(prefix="/item", tags=["Item"])


@router.post("/add", response_model=ItemCreate)
async def add_item(
    new_item: ItemCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        return await ItemService.add(new_item, session)
    except Exception:
        logging.info(f"Item {new_item} don't added")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "item not added",
            },
        )


@router.get("/get", response_model=ItemCreate)
async def get_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return await ItemService.get(item_id, session)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": None,
            },
    )


@router.get("/count")
async def count_items(session: AsyncSession = Depends(get_async_session)):
    try:
        return await ItemService.count(session)
    except:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "items not counted",
            },
        )


@router.delete("/delete")
async def delete_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return await ItemService.delete(item_id, session)
    except:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "items not deleted",
            },
        )
