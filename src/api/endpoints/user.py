from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_current_active_user, user_service
from schemas.token_schema import TokenSchema
from schemas.user_schema import UserCreateSchema, UserReadSchema
from services.user_service import UserService
from core.config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/create_user", response_model=UserReadSchema)
async def create_user(
    user: UserCreateSchema,
    user_service: Annotated[UserService, Depends(user_service)],
):
    user_db = await user_service.create_user(user)
    return user_db


@router.get("/get_users", response_model=list[UserReadSchema])
async def get_users(
    user_service: Annotated[UserService, Depends(user_service)],
):
    users = await user_service.get_users()
    return users


@router.get("/get_user", response_model=UserReadSchema | None)
async def get_user(
    user_service: Annotated[UserService, Depends(user_service)],
    user_id: int = Query(ge=0),
):
    user = await user_service.get_user(user_id)
    return user


@router.put("/update_user", response_model=UserReadSchema)
async def update_user(
    user_new: UserCreateSchema,
    user_service: Annotated[UserService, Depends(user_service)],
):
    user_db = await user_service.update_user(user_new)
    return user_db


@router.delete("/delete_user", response_model=UserReadSchema)
async def delete_user(
    user_service: Annotated[UserService, Depends(user_service)],
    user_id: int = Query(ge=0),
):
    user = await user_service.delete_user(user_id)
    return user


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(user_service)],
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserReadSchema)
async def read_users_me(
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)]
):
    return current_user
