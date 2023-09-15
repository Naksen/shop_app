from datetime import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from order.schemas import OrderCreate
from order.service import OrderService
from auth.schemas import UserInDB, User
from auth.service import get_current_active_user

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/add", response_model=OrderCreate)
async def add_order(
    item_id: int,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        new_order = OrderCreate(
            user_id=user.id,
            item_id=item_id,
            date_of_purchase=datetime.utcnow(),
            status="Pending",
        )
        return await OrderService.add(new_order, session)
    except Exception:
        logging.error(f"Order {new_order} wasn't added")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Database conflict",
            },
        )


@router.get("/get")
async def get_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return await OrderService.get(order_id, session)
    except Exception:
        logging.error(f"Order {order_id} wasn't got")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Database conflict",
            },
        )
