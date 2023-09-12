from order.schemas import OrderCreate
from order.models import Order
from sqlalchemy import insert, select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession


class OrderService:
    @classmethod
    async def add(cls, new_order: OrderCreate, session: AsyncSession):
        stmt = insert(Order).values(**new_order.model_dump())
        await session.execute(stmt)
        await session.commit()
        return new_order

    @classmethod
    async def get(cls, order_id: int, session: AsyncSession):
        query = select(Order).where(Order.id == order_id)
        result = await session.execute(query)
        res = result.scalars().first()
        return res

    @classmethod
    async def count(cls, session: AsyncSession):
        query = select(func.count(Order.id)).select_from(Order)
        result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def delete(cls, order_id: int, session: AsyncSession):
        stmt = delete(Order).where(Order.id == order_id)
        await session.execute(stmt)
        await session.commit()
        return True
