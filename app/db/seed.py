# app/db/seed.py
from sqlalchemy.orm import Session
from datetime import date, timedelta
from ..models.base import Base
from ..models.product import Product
from ..models.sale import Sale
from ..models.inventory import Inventory
from .session import engine

def seed_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # Clear existing data
        session.query(Inventory).delete()
        session.query(Sale).delete()
        session.query(Product).delete()
        session.commit()

        # Sample products
        products = [
            {"name": "Laptop", "price": 999.99, "category": "Electronics", "description": "High-performance laptop"},
            {"name": "Smartphone", "price": 699.99, "category": "Electronics", "description": "Latest smartphone model"},
            {"name": "Headphones", "price": 149.99, "category": "Electronics", "description": "Noise-cancelling headphones"},
            {"name": "Smartwatch", "price": 199.99, "category": "Electronics", "description": "Fitness tracking smartwatch"},
            {"name": "Tablet", "price": 299.99, "category": "Electronics", "description": "Portable tablet device"}
        ]

        # Insert products
        for product in products:
            session.add(Product(**product))

        # Commit to get product IDs
        session.commit()

        # Get product IDs
        product_ids = [p.id for p in session.query(Product).all()]

        # Sample sales data for the last 30 days
        today = date.today()
        sales = []
        for i in range(1, 31):
            sales_date = today - timedelta(days=i)
            for product_id in product_ids:
                if i % 5 == 0:  # Create a sale every 5 days for each product
                    product = session.query(Product).filter(Product.id == product_id).first()
                    sales.append({
                        "product_id": product_id,
                        "quantity": i % 3 + 1,  # Quantity between 1 and 3
                        "sale_date": sales_date,
                        "revenue": (i % 3 + 1) * product.price
                    })

        # Insert sales
        for sale in sales:
            session.add(Sale(**sale))

        # Sample inventory data
        inventory = []
        for product_id in product_ids:
            inventory.append({
                "product_id": product_id,
                "quantity": (product_id * 10) + 5,  # Different quantities for each product
                "last_updated": today
            })

        # Insert inventory
        for item in inventory:
            session.add(Inventory(**item))

        session.commit()
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
