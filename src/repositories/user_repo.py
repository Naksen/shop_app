from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from models.user_model import User
from utils.repository import SQLAlchemyRepository
from db.db import async_session_maker


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_by_username(self, username: str):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.username == username)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def update(self, data: dict):
        async with async_session_maker() as session:
            try:
                username = data["username"]
                stmt = (
                    update(self.model)
                    .where(self.model.username == username)
                    .values(**data)
                    .returning(self.model)
                )
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
            except NoResultFound:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this username does not exist",
                )
