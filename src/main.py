import logging
from fastapi import FastAPI, Depends
from item.router import router as router_items
from order.router import router as router_order
from pages.router import router as router_pages
from auth.schemas import UserCreate, UserRead
from auth.models import User
from auth.user import auth_backend, current_active_user, fastapi_users

logging.basicConfig(filename="app_log.log", level=logging.INFO)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(router_items)
app.include_router(router_order)
app.include_router(router_pages)
