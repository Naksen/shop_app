from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserReadSchema(BaseModel):
    id: int = Field(ge=0)
    username: str
    full_name: str | None
    email: EmailStr | None
    role_id: int
    registered_at: datetime
    is_active: bool


class UserCreateSchema(BaseModel):
    username: str
    full_name: str | None = None
    email: EmailStr | None = None
    password: str
    role_id: int
    registered_at: datetime = datetime.utcnow()
    is_active: bool


class UserInDBSchema(UserReadSchema):
    hashed_password: str


class UserCreateOutSchema(BaseModel):
    user_id: int
