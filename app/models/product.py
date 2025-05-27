from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String(50))
