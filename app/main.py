from fastapi import FastAPI
from .db.session import engine
from .models.base import Base
from .api.product import router as product_router
from .api.sale import router as sale_router
from .api.inventory import router as inventory_router

app = FastAPI()

# Add debugging for table creation
print("Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")

# Add debugging for router registration
print("Registering routers...")
app.include_router(product_router, tags=["products"])
app.include_router(sale_router, tags=["sales"])
app.include_router(inventory_router, tags=["inventory"])
print("Routers registered successfully")

# Add a root endpoint to test if API is running
@app.get("/")
def read_root():
    return {"message": "API is running", "status": "ok"}