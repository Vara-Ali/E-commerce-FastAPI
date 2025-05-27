from sqlalchemy import Column, Integer, ForeignKey, Date
from .base import Base
from sqlalchemy.orm import relationship

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    last_updated = Column(Date)
    low_stock_threshold = Column(Integer, default=10) 

    product = relationship("Product") 