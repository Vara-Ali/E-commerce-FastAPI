from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

