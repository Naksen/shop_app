from datetime import timedelta, datetime

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

from schemas.user_schema import UserCreateSchema
from repositories.user_repo import UserRepository
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo: UserRepository = user_repo()

    async def create_user(self, user: UserCreateSchema):
        user_dict = user.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.get_password_hash(password)

        user_is_exist = await self.user_repo.get_by_username(user.username)
        if user_is_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
        user_db = await self.user_repo.create(user_dict)
        return user_db

    async def get_user_by_username(self, username: str):
        user = await self.user_repo.get_by_username(username)
        return user

    async def get_users(self):
        users = await self.user_repo.get_all()
        return users

    async def get_user(self, user_id: int):
        user = await self.user_repo.get(user_id)
        return user

    async def update_user(self, user: UserCreateSchema):
        user_dict = user.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.get_password_hash(password)
        user_db = await self.user_repo.update(user_dict)
        return user_db

    async def delete_user(self, user_id: int):
        user = await self.user_repo.delete(user_id)
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

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
