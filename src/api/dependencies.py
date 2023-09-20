from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from repositories.item_repo import ItemRepository
from repositories.order_repo import OrderRepository
from repositories.user_repo import UserRepository
from schemas.user_schema import UserReadSchema
from services.item_service import ItemService
from services.order_service import OrderService
from services.user_service import UserService, oauth2_scheme
from schemas.token_schema import TokenDataSchema
from core.config import settings


def item_service() -> ItemService:
    return ItemService(ItemRepository)


def user_service() -> UserService:
    return UserService(UserRepository)


def order_service() -> OrderService:
    return OrderService(OrderRepository)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(user_service)],
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
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserReadSchema, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
