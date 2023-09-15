from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from database import get_async_session
from auth.schemas import User as UserScheme, Token, UserCreate, UserInDB
from auth.service import UserService, get_current_active_user
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserService.authenticate_user(
        form_data.username, form_data.password, session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserScheme)
async def read_users_me(
    current_user: Annotated[UserScheme, Depends(get_current_active_user)]
):
    return current_user


@router.get("/me/items")
async def read_own_items(
    current_user: Annotated[UserScheme, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/get", response_model=UserInDB | None)
async def get_user_by_username(
    username: str, session: AsyncSession = Depends(get_async_session)
):
    return await UserService.get_by_username(username, session)


@router.post("/register", response_model=UserScheme | None)
async def get_user_by_username(
    new_user: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    return await UserService.create(new_user, session)
