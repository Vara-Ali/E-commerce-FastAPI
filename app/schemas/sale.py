# app/schemas/sale.py
from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional, List

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_date: date
    revenue: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int

    class Config:
        from_attributes = True

class SaleAnalysis(BaseModel):
    date: Optional[str] = None  
    week: Optional[str] = None
    month: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
    total_revenue: float
    total_sales: int

    @field_validator('date', mode='before')
    def convert_date_to_string(cls, value):
        if isinstance(value, date):
            return value.isoformat()
        return value

class PeriodData(BaseModel):
    total_revenue: float
    total_sales: int

class RevenueComparison(BaseModel):
    period1: PeriodData
    period2: PeriodData
    comparison: dict
