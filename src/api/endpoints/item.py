from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.dependencies import item_service
from schemas.item_schema import ItemSchema
from services.item_service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.post("/create_item", response_model=ItemSchema)
async def create_item(
    item: ItemSchema,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    item_db = await item_service.create_item(item)
    return item_db


@router.get("/get_items", response_model=list[ItemSchema])
async def get_items(
    item_service: Annotated[ItemService, Depends(item_service)],
):
    items = await item_service.get_items()
    return items


@router.get("/get_item", response_model=ItemSchema | None)
async def get_item(
    item_service: Annotated[ItemService, Depends(item_service)],
    item_id: int = Query(ge=0),
):
    item = await item_service.get_item(item_id)
    return item


@router.put("/update_item", response_model=ItemSchema)
async def update_item(
    item_new: ItemSchema,
    item_service: Annotated[ItemService, Depends(item_service)],
):
    item_db = await item_service.update_item(item_new)
    return item_db


@router.delete("/delete_item", response_model=ItemSchema)
async def delete_item(
    item_service: Annotated[ItemService, Depends(item_service)],
    item_id: int = Query(ge=0),
):
    item = await item_service.delete_item(item_id)
    return item
