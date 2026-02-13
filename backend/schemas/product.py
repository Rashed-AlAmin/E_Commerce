from pydantic import BaseModel
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: float

    class Config:
        from_attributes = True
