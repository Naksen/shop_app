from fastapi import Depends, HTTPException
from item.schemas import ItemCreate
from item.models import Item
from sqlalchemy import insert, select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from database import *


class ItemService:
    @classmethod
    async def add(cls, new_item: ItemCreate, session: AsyncSession):
        try:
            stmt = insert(Item).values(**new_item.model_dump())
            await session.execute(stmt)
            await session.commit()
            return new_item
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "data": None,
                    "details": "item not added",
                },
            )

    @classmethod
    async def get(cls, item_id: int, session: AsyncSession):
        try:
            query = select(Item).where(Item.id == item_id)
            result = await session.execute(query)
            res = result.scalars().first()
            return res
        except Exception:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "data": None,
                    "details": None,
                },
            )

    @classmethod
    async def count(cls, session: AsyncSession):
        query = select(func.count(Item.id)).select_from(Item)
        result = await session.execute(query)
        return result.scalar()
        # except:
        #     raise HTTPException(
        #         status_code=500,
        #         detail={
        #             "status": "error",
        #             "data": None,
        #             "details": "items not counted",
        #         },
        #     )

    @classmethod
    async def delete(cls, item_id: int, session: AsyncSession):
        try:
            stmt = delete(Item).where(Item.id == item_id)
            await session.execute(stmt)
            await session.commit()
        except:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "data": None,
                    "details": "items not deleted",
                },
            )
