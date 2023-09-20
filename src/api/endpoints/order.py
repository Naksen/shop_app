from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.dependencies import get_current_active_user, order_service
from schemas.order_schema import OrderCreateSchema, OrderDBSchema, OrderUserSchema
from schemas.user_schema import UserReadSchema
from services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/create_order", response_model=OrderDBSchema)
async def create_order(
    order: OrderUserSchema,
    order_service: Annotated[OrderService, Depends(order_service)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
):
    user_id = current_user.id
    order_create = OrderCreateSchema(
        user_id=user_id,
        item_id=order.item_id,
        date_of_purchase=datetime.utcnow(),
        status="Pending",
    )
    order_db = await order_service.create_order(order_create)
    return order_db


@router.get("/get_orders", response_model=list[OrderDBSchema])
async def get_orders(order_service: Annotated[OrderService, Depends(order_service)]):
    orders = await order_service.get_orders()
    return orders


@router.get("/get_my_orders", response_model=list[OrderDBSchema])
async def get_my_orders(
    order_service: Annotated[OrderService, Depends(order_service)],
    current_user: Annotated[UserReadSchema, Depends(get_current_active_user)],
):
    user_id = current_user.id
    my_orders = await order_service.get_orders_by_user_id(user_id)
    return my_orders


@router.put("/update_order", response_model=OrderDBSchema)
async def update_order(
    order_new: OrderCreateSchema,
    order_service: Annotated[OrderService, Depends(order_service)],
    order_id: int = Query(ge=0),
):
    order_db = OrderDBSchema(
        id=order_id,
        **order_new.model_dump(),
    )
    order = await order_service.update_order(order_db)
    return order


@router.delete("/delete_order", response_model=OrderDBSchema)
async def delete_order(
    order_service: Annotated[OrderService, Depends(order_service)],
    order_id: int = Query(ge=0),
):
    order = await order_service.delete_order(order_id)
    return order
