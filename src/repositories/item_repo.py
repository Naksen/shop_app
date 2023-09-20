from models.item_model import Item
from utils.repository import SQLAlchemyRepository


class ItemRepository(SQLAlchemyRepository):
    model = Item
