from datetime import datetime
from pydantic import BaseModel


class ItemCreate(BaseModel):
    id: int
    name: str
    cost: int
    brand: str
    size: str
    added_at: datetime
    description: str
    rating: float
    amount: int
    type: str