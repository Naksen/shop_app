from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status

from db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def get():
        raise NotImplementedError

    @abstractmethod
    async def update():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def create(self, data: dict) -> int:
        async with async_session_maker() as session:
            try:
                stmt = insert(self.model).values(**data).returning(self.model)
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Resource already exists",
                )

    async def get_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def update(self, data: dict):
        async with async_session_maker() as session:
            try:
                id = data["id"]
                stmt = (
                    update(self.model)
                    .where(self.model.id == id)
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
                    detail="Resource with id does not exist",
                )

    async def delete(self, id: int):
        async with async_session_maker() as session:
            try:
                stmt = (
                    delete(self.model).where(self.model.id == id).returning(self.model)
                )
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
            except NoResultFound:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Resource with id does not exist",
                )
