from sqlalchemy import select

from models.order_model import Order
from utils.repository import SQLAlchemyRepository
from db.db import async_session_maker


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def get_by_user_id(self, user_id):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()
