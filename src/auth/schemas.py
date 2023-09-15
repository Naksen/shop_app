from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    registered_at: datetime
    is_active: bool | None = None
    role_id: int


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    password: str
    registered_at: datetime
    is_active: bool | None = None
    role_id: int
