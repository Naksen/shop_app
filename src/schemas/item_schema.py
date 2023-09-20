from datetime import datetime

from pydantic import BaseModel, Field


class ItemSchema(BaseModel):
    id: int = Field(ge=0)
    name: str
    cost: int = Field(ge=0)
    brand: str
    size: str
    amount: int = Field(ge=0)
    added_at: datetime | None
    description: str | None
    rating: float | None
    type: str | None
