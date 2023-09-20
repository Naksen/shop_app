from schemas.item_schema import ItemSchema
from repositories.item_repo import ItemRepository


class ItemService:
    def __init__(self, item_repo: ItemRepository):
        self.item_repo: ItemRepository = item_repo()

    async def create_item(self, item: ItemSchema):
        item_dict = item.model_dump()
        item_db = await self.item_repo.create(item_dict)
        return item_db

    async def get_items(self):
        items = await self.item_repo.get_all()
        return items

    async def get_item(self, item_id: int):
        item = await self.item_repo.get(item_id)
        return item

    async def update_item(self, item_new: ItemSchema):
        item_dict = item_new.model_dump()
        item_db = await self.item_repo.update(item_dict)
        return item_db

    async def delete_item(self, item_id: int):
        item = await self.item_repo.delete(item_id)
        return item
