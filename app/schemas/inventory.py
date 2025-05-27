# app/schemas/inventory.py
from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, List

class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    last_updated: date
    low_stock_threshold: int = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    last_updated: Optional[date] = None
    low_stock_threshold: Optional[int] = None

class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    low_stock_threshold: int
    deficit: int
    category: Optional[str] = None
    
    class Config:
        from_attributes = True

class InventoryHistory(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    last_updated: date
    change: Optional[int] = None
    category: Optional[str] = None

class InventorySummary(BaseModel):
    total_products: int
    total_quantity: int
    low_stock_items: int
    categories: List[dict]
