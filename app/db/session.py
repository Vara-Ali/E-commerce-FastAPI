from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:varaisme@localhost:5432/ecommerce"

# Add debugging for database connection
print(f"🔗 Connecting to database: {SQLALCHEMY_DATABASE_URL}")
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Test the connection
    with engine.connect() as connection:
        print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    print("Creating database session...")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("Closing database session...")
        db.close()