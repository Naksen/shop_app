from schemas.order_schema import OrderCreateSchema, OrderDBSchema
from repositories.order_repo import OrderRepository


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo: OrderRepository = order_repo()

    async def create_order(self, order: OrderCreateSchema):
        order_dict = order.model_dump()
        order_db = await self.order_repo.create(order_dict)
        return order_db

    async def get_orders(self):
        orders = await self.order_repo.get_all()
        return orders

    async def get_order(self, order_id: int):
        order = await self.order_repo.get(order_id)
        return order

    async def get_orders_by_user_id(self, user_id: int):
        orders = await self.order_repo.get_by_user_id(user_id)
        return orders

    async def update_order(self, order_new: OrderDBSchema):
        order_dict = order_new.model_dump()
        order_db = await self.order_repo.update(order_dict)
        return order_db

    async def delete_order(self, order_id: int):
        order = await self.order_repo.delete(order_id)
        return order
