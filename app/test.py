from sqlalchemy import create_engine, text

def main():
    DATABASE_URL = "postgresql://postgres:varaisme@localhost:5432/ecommerce"
    
    try:
        # Connect to database
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        print("✅ Database connection successful!")
        print("=" * 50)
        
        # Get all table names
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        
        if not tables:
            print("No tables found in database")
            return
            
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  • {table}")
        
        print("\n" + "=" * 50)
        
        # Show data from each table
        for table in tables:
            print(f"\nTABLE: {table}")
            print("-" * 30)
            
            # Count records
            count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = count_result.scalar()
            print(f"Records: {count}")
            
            if count > 0:
                # Show first 5 records
                data_result = connection.execute(text(f"SELECT * FROM {table} LIMIT 5"))
                rows = data_result.fetchall()
                columns = data_result.keys()
                
                print("Columns:", list(columns))
                print("Sample data:")
                for i, row in enumerate(rows, 1):
                    print(f"  Row {i}: {dict(row)}")
            else:
                print("No data in this table")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()