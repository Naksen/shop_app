from fastapi import APIRouter
from api.endpoints import item, user, order

api_router = APIRouter()
api_router.include_router(item.router)
api_router.include_router(user.router)
api_router.include_router(order.router)
