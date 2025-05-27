from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from .base import Base 
from sqlalchemy.orm import relationship

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    sale_date = Column(Date)
    revenue = Column(Float)

    product = relationship("Product")  