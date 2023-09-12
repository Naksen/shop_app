from item.schemas import ItemCreate
from item.models import Item
from sqlalchemy import insert, select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession


class ItemService:
    @classmethod
    async def add(cls, new_item: ItemCreate, session: AsyncSession):
        stmt = insert(Item).values(**new_item.model_dump())
        await session.execute(stmt)
        await session.commit()
        return new_item

    @classmethod
    async def get(cls, item_id: int, session: AsyncSession):
        query = select(Item).where(Item.id == item_id)
        result = await session.execute(query)
        res = result.scalars().first()
        return res

    @classmethod
    async def count(cls, session: AsyncSession):
        query = select(func.count(Item.id)).select_from(Item)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def delete(cls, item_id: int, session: AsyncSession):
        stmt = delete(Item).where(Item.id == item_id)
        await session.execute(stmt)
        await session.commit()
