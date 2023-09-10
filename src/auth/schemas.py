from fastapi_users import schemas
from datetime import datetime


class UserRead(schemas.BaseUser[int]):
    role_id: int
    username: str
    registered_at: datetime


class UserCreate(schemas.BaseUserCreate):
    role_id: int
    username: str
    registered_at: datetime


class UserUpdate(schemas.BaseUserUpdate):
    role_id: int
    username: str
    registered_at: datetime
