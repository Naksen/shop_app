from typing import Annotated
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import User as UserScheme, UserCreate, UserInDB, TokenData
from auth.models import User
from config import settings
from database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class UserService:
    @classmethod
    async def create(cls, new_user: UserCreate, session: AsyncSession):
        user_dict = new_user.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = get_password_hash(password)
        user = User(**user_dict)

        username = user.username
        user_is_exist = await cls.get_by_username(username, session)
        if user_is_exist:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="user with this username already exists",
                )
        session.add(user)
        await session.commit()
        return user

    @staticmethod
    async def get(id: int, session: AsyncSession):
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_by_username(username: str, session: AsyncSession):
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalars().first()
        if user:
            return UserInDB(**user.__dict__)
        return None

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def authenticate_user(
        cls, username: str, password: str, session: AsyncSession
    ):
        user = await cls.get_by_username(username, session)
        if not user:
            return False
        if not cls.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await UserService.get_by_username(
        username=token_data.username, session=session
    )
    if user is None:
        raise credentials_exception
    return user


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_active_user(
    current_user: Annotated[UserScheme, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
