from typing import Annotated
from datetime import timedelta

import logging
from fastapi import FastAPI, Depends,HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from item.router import router as router_items
from order.router import router as router_order
from pages.router import router as router_pages
from auth.schemas import User as UserScheme, Token, UserInDB
from auth.service import UserService, get_current_active_user
from config import settings
from database import get_async_session


logging.basicConfig(filename="app_log.log", level=logging.INFO)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserService.authenticate_user(form_data.username, form_data.password, session)
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


@app.get("/users/me/", response_model=UserScheme)
async def read_users_me(
    current_user: Annotated[UserScheme, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserScheme, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/user/get", response_model= UserInDB | None)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_async_session)):
    return await UserService.get_user(username, session)

app.include_router(router_items)
app.include_router(router_order)
app.include_router(router_pages)
