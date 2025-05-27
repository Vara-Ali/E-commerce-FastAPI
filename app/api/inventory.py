# app/api/inventory.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from datetime import date, timedelta
from typing import List, Optional
from ..schemas.inventory import (
    InventoryCreate, Inventory, InventoryUpdate,
    LowStockAlert, InventoryHistory, InventorySummary
)
from ..models.inventory import Inventory as InventoryModel
from ..models.product import Product as ProductModel
from ..db.session import get_db


router = APIRouter()

@router.post("/inventory/", response_model=Inventory)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(ProductModel).filter(ProductModel.id == inventory.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if inventory already exists for this product
    existing_inventory = db.query(InventoryModel).filter(
        InventoryModel.product_id == inventory.product_id
    ).first()

    if existing_inventory:
        raise HTTPException(
            status_code=400,
            detail="Inventory already exists for this product"
        )

    db_inventory = InventoryModel(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.get("/inventory/", response_model=List[Inventory])
def get_inventory(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    low_stock: Optional[bool] = None
):
    query = db.query(InventoryModel).join(ProductModel)

    if product_id:
        query = query.filter(InventoryModel.product_id == product_id)

    if category:
        query = query.filter(ProductModel.category == category)

    if low_stock:
        query = query.filter(InventoryModel.quantity <= InventoryModel.low_stock_threshold)

    return query.offset(skip).limit(limit).all()

@router.get("/inventory/{inventory_id}", response_model=Inventory)
def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(InventoryModel).filter(InventoryModel.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory

@router.put("/inventory/{inventory_id}", response_model=Inventory)
def update_inventory(
    inventory_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):
    db_inventory = db.query(InventoryModel).filter(InventoryModel.id == inventory_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # Track previous quantity for history
    previous_quantity = db_inventory.quantity

    # Update fields
    for field, value in inventory.model_dump(exclude_unset=True).items():
        setattr(db_inventory, field, value)

    # If quantity was updated, record the change
    if 'quantity' in inventory.model_dump(exclude_unset=True):
        change = db_inventory.quantity - previous_quantity
        # Here you would typically create an inventory history record
        # For this example, we'll just update the last_updated date
        db_inventory.last_updated = date.today()

    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# app/api/inventory.py
@router.get("/inventory/alerts/low-stock", response_model=List[LowStockAlert])
def get_low_stock_alerts(
    db: Session = Depends(get_db),
    threshold: Optional[int] = Query(None, description="Custom threshold for low stock"),
    category: Optional[str] = Query(None, description="Filter by product category"),
    debug: bool = Query(False, description="Enable debug output")
):
    try:
        # Get all inventory records for debugging
        if debug:
            all_inventory = db.query(InventoryModel).all()
            print(f"Total inventory records: {len(all_inventory)}")
            for item in all_inventory[:5]:
                print(f"Product ID: {item.product_id}, Quantity: {item.quantity}, Threshold: {item.low_stock_threshold}")

        query = db.query(
            InventoryModel.product_id,
            ProductModel.name,
            ProductModel.category,
            InventoryModel.quantity,
            InventoryModel.low_stock_threshold,
            (InventoryModel.low_stock_threshold - InventoryModel.quantity).label("deficit")
        ).join(
            ProductModel, InventoryModel.product_id == ProductModel.id
        )

        # Apply threshold filter
        if threshold is None:
            query = query.filter(InventoryModel.quantity <= InventoryModel.low_stock_threshold)
        else:
            query = query.filter(InventoryModel.quantity <= threshold)

        if category:
            query = query.filter(ProductModel.category == category)

        if debug:
            print(f"Generated SQL: {query.statement.compile(compile_kwargs={'literal_binds': True})}")

        results = query.all()

        if debug:
            print(f"Query results count: {len(results)}")

        return [
            LowStockAlert(
                product_id=row.product_id,
                product_name=row.name,
                quantity=row.quantity,
                low_stock_threshold=row.low_stock_threshold,
                deficit=row.deficit,
                category=row.category
            )
            for row in results
        ]
    except Exception as e:
        print(f"Error in low stock endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/inventory/history/{product_id}", response_model=List[InventoryHistory])
def get_inventory_history(
    product_id: int,
    db: Session = Depends(get_db),
    days: Optional[int] = Query(30, description="Number of days to look back")
):
    # In a real implementation, you would have an inventory_history table
    # For this example, we'll just return the current inventory with a calculated change
    current_inventory = db.query(InventoryModel).filter(
        InventoryModel.product_id == product_id
    ).first()

    if not current_inventory:
        raise HTTPException(status_code=404, detail="Product inventory not found")

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    # For demo purposes, we'll create a mock history
    # In a real app, you would query an inventory_history table
    mock_history = [
        InventoryHistory(
            product_id=product_id,
            product_name=product.name,
            quantity=current_inventory.quantity,
            last_updated=current_inventory.last_updated,
            change=0,  # No change in this simple example
            category=product.category
        )
    ]

    return mock_history

# Inventory summary endpoint (note the different path)
@router.get("/inventory/summary/", response_model=InventorySummary)
def get_inventory_summary(db: Session = Depends(get_db)):
    # Total products in inventory
    total_products = db.query(func.count(InventoryModel.product_id.distinct())).scalar()

    # Total quantity across all products
    total_quantity = db.query(func.sum(InventoryModel.quantity)).scalar() or 0

    # Count of low stock items
    low_stock_items = db.query(func.count(InventoryModel.id)).filter(
        InventoryModel.quantity <= InventoryModel.low_stock_threshold
    ).scalar() or 0

    # Categories breakdown
    categories = db.query(
        ProductModel.category,
        func.sum(InventoryModel.quantity).label("total_quantity")
    ).join(
        ProductModel, InventoryModel.product_id == ProductModel.id
    ).group_by(
        ProductModel.category
    ).all()

    return InventorySummary(
        total_products=total_products,
        total_quantity=total_quantity,
        low_stock_items=low_stock_items,
        categories=[{"category": cat, "quantity": qty} for cat, qty in categories]
    )

@router.post("/inventory/{product_id}/adjust", response_model=Inventory)
def adjust_inventory(
    product_id: int,
    adjustment: int = Query(..., description="Positive for addition, negative for subtraction"),
    db: Session = Depends(get_db)
):
    inventory = db.query(InventoryModel).filter(InventoryModel.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    new_quantity = inventory.quantity + adjustment
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Cannot have negative inventory")

    inventory.quantity = new_quantity
    inventory.last_updated = date.today()

    db.commit()
    db.refresh(inventory)
    return inventory
