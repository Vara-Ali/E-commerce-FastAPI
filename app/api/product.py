from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas.product import ProductCreate, Product, ProductUpdate
from ..models.product import Product as ProductModel
from ..db.session import get_db
from datetime import date
from ..models.sale import Sale as SaleModel
from sqlalchemy import func, desc

router = APIRouter()


@router.post("/products/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=List[Product])
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = Query(None, description="Filter by product category"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter")
):
    """Get a list of products with optional filters"""
    query = db.query(ProductModel)

    if category:
        query = query.filter(ProductModel.category == category)

    if min_price:
        query = query.filter(ProductModel.price >= min_price)

    if max_price:
        query = query.filter(ProductModel.price <= max_price)

    return query.offset(skip).limit(limit).all()

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product



@router.get("/products/analytics/top-selling", response_model=List[Product])
def get_top_selling_products(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of products to return"),
    start_date: Optional[date] = Query(None, description="Start date for sales analysis"),
    end_date: Optional[date] = Query(None, description="End date for sales analysis")
):
    """Get top selling products by revenue"""
    query = db.query(
        ProductModel,
        func.sum(SaleModel.revenue).label("total_revenue")
    ).join(
        SaleModel, ProductModel.id == SaleModel.product_id
    )

    if start_date:
        query = query.filter(SaleModel.sale_date >= start_date)

    if end_date:
        query = query.filter(SaleModel.sale_date <= end_date)

    query = query.group_by(ProductModel.id).order_by(desc("total_revenue")).limit(limit)

    return [product for product, _ in query.all()]


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/products/analytics/by-category", response_model=dict[str, List[Product]])
def get_products_by_category(db: Session = Depends(get_db)):
    """Get products grouped by category"""
    products = db.query(ProductModel).all()

    categories = {}
    for product in products:
        if product.category not in categories:
            categories[product.category] = []
        # Convert SQLAlchemy model to Pydantic model
        categories[product.category].append(Product.model_validate(product))

    return categories

@router.get("/products/analytics/search", response_model=List[Product])
def search_products(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Search by product name"),
    description: Optional[str] = Query(None, description="Search by product description")
):
    """Search products by name or description"""
    query = db.query(ProductModel)

    if name:
        query = query.filter(ProductModel.name.ilike(f"%{name}%"))

    if description:
        query = query.filter(ProductModel.description.ilike(f"%{description}%"))

    return query.all()