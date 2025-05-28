from app.db.session import SessionLocal
from ..models.product import Product as ProductModel
from ..models.inventory import Inventory as InventoryModel
from ..models.sale import Sale as SaleModel
from datetime import date, timedelta
from sqlalchemy import text
import random

def seed():
    db = SessionLocal()

    try:
        db.execute(text("TRUNCATE TABLE sales, inventory, products RESTART IDENTITY CASCADE"))
        
        # Walmart-style product catalog with diverse categories
        products = [
            # Electronics
            ProductModel(name="Samsung 65\" 4K Smart TV", price=85000, category="Electronics", description="65-inch QLED 4K Smart TV with HDR and voice control"),
            ProductModel(name="iPhone 15 Pro", price=120000, category="Electronics", description="Latest iPhone with A17 Pro chip, 256GB storage, titanium design"),
            ProductModel(name="MacBook Air M2", price=135000, category="Electronics", description="13-inch MacBook Air with M2 chip, 8GB RAM, 256GB SSD"),
            ProductModel(name="Sony WH-1000XM5 Headphones", price=35000, category="Electronics", description="Premium noise-canceling wireless headphones"),
            ProductModel(name="iPad Pro 12.9\"", price=110000, category="Electronics", description="12.9-inch iPad Pro with M2 chip and Liquid Retina display"),
            ProductModel(name="Dell XPS 13 Laptop", price=95000, category="Electronics", description="13-inch ultrabook with Intel i7 processor and 16GB RAM"),
            ProductModel(name="Nintendo Switch OLED", price=38000, category="Electronics", description="Gaming console with 7-inch OLED screen"),
            ProductModel(name="AirPods Pro (2nd Gen)", price=28000, category="Electronics", description="Wireless earbuds with active noise cancellation"),
            ProductModel(name="Canon EOS R6 Camera", price=185000, category="Electronics", description="Full-frame mirrorless camera with 4K video recording"),
            ProductModel(name="Bose SoundLink Flex Speaker", price=15000, category="Electronics", description="Portable Bluetooth speaker with waterproof design"),
            
            # Home & Garden
            ProductModel(name="KitchenAid Stand Mixer", price=45000, category="Home & Garden", description="5-quart tilt-head stand mixer in multiple colors"),
            ProductModel(name="Dyson V15 Detect Vacuum", price=65000, category="Home & Garden", description="Cordless vacuum with laser dust detection"),
            ProductModel(name="Instant Pot Duo 8-Quart", price=8500, category="Home & Garden", description="Multi-use pressure cooker with 7 functions"),
            ProductModel(name="Ninja Foodi Air Fryer", price=12000, category="Home & Garden", description="6.5-quart air fryer with multiple cooking functions"),
            ProductModel(name="Shark Navigator Vacuum", price=15000, category="Home & Garden", description="Upright vacuum with anti-allergen technology"),
            ProductModel(name="Hamilton Beach Coffee Maker", price=4500, category="Home & Garden", description="12-cup programmable coffee maker with auto shut-off"),
            ProductModel(name="Lodge Cast Iron Skillet", price=2500, category="Home & Garden", description="10.25-inch pre-seasoned cast iron skillet"),
            ProductModel(name="Cuisinart Food Processor", price=18000, category="Home & Garden", description="14-cup food processor with multiple attachments"),
            ProductModel(name="Black+Decker Toaster Oven", price=7500, category="Home & Garden", description="6-slice convection toaster oven with multiple settings"),
            ProductModel(name="Rubbermaid Storage Containers Set", price=3500, category="Home & Garden", description="20-piece food storage container set with leak-proof lids"),
            
            # Clothing
            ProductModel(name="Levi's 501 Original Jeans", price=6500, category="Clothing", description="Classic straight-leg jeans in various washes and sizes"),
            ProductModel(name="Nike Air Max 270 Sneakers", price=12000, category="Clothing", description="Men's running shoes with Max Air unit"),
            ProductModel(name="Adidas Ultraboost 22 Running Shoes", price=15000, category="Clothing", description="Premium running shoes with Boost midsole technology"),
            ProductModel(name="Champion Powerblend Hoodie", price=3500, category="Clothing", description="Fleece hoodie with kangaroo pocket, various colors"),
            ProductModel(name="Hanes ComfortSoft T-Shirts (6-Pack)", price=2000, category="Clothing", description="Pack of 6 cotton crew neck t-shirts"),
            ProductModel(name="Wrangler Relaxed Fit Jeans", price=4500, category="Clothing", description="Comfortable relaxed fit jeans for everyday wear"),
            ProductModel(name="Under Armour Tech 2.0 Polo", price=2800, category="Clothing", description="Moisture-wicking polo shirt for active wear"),
            ProductModel(name="Columbia Flash Forward Jacket", price=8500, category="Clothing", description="Waterproof windbreaker jacket with packable design"),
            ProductModel(name="Fruit of the Loom Underwear (12-Pack)", price=1800, category="Clothing", description="Pack of 12 cotton briefs in assorted colors"),
            ProductModel(name="Dickies Work Pants", price=3200, category="Clothing", description="Durable work pants with reinforced knees"),
            
            # Grocery & Food
            ProductModel(name="Great Value 2% Milk (1 Gallon)", price=350, category="Grocery", description="Fresh 2% reduced fat milk, 1 gallon jug"),
            ProductModel(name="Wonder Bread Classic White", price=180, category="Grocery", description="20-slice loaf of soft white bread"),
            ProductModel(name="Bananas (per lb)", price=120, category="Grocery", description="Fresh yellow bananas, sold per pound"),
            ProductModel(name="Ground Beef 80/20 (per lb)", price=650, category="Grocery", description="Fresh ground beef, 80% lean/20% fat"),
            ProductModel(name="Tide Laundry Detergent (100 oz)", price=1200, category="Grocery", description="High-efficiency liquid laundry detergent"),
            ProductModel(name="Coca-Cola (12-pack cans)", price=450, category="Grocery", description="12-pack of 12 oz Coca-Cola cans"),
            ProductModel(name="Lay's Classic Potato Chips", price=280, category="Grocery", description="Family size bag of classic potato chips"),
            ProductModel(name="Cheerios Cereal (18 oz)", price=520, category="Grocery", description="Whole grain oat cereal, heart-healthy"),
            ProductModel(name="Great Value Pasta (1 lb)", price=150, category="Grocery", description="Enriched macaroni pasta, 1 pound box"),
            ProductModel(name="Philadelphia Cream Cheese (8 oz)", price=320, category="Grocery", description="Original cream cheese spread, 8 oz package"),
            
            # Health & Beauty
            ProductModel(name="Crest 3D White Toothpaste", price=450, category="Health & Beauty", description="Whitening toothpaste with fluoride protection"),
            ProductModel(name="Head & Shoulders Shampoo", price=580, category="Health & Beauty", description="Anti-dandruff shampoo, 32.1 fl oz"),
            ProductModel(name="Dove Beauty Bar (8-pack)", price=650, category="Health & Beauty", description="Moisturizing beauty bar soap, pack of 8"),
            ProductModel(name="Tylenol Extra Strength (100 count)", price=880, category="Health & Beauty", description="Pain reliever and fever reducer, 100 caplets"),
            ProductModel(name="Neutrogena Daily Facial Cleanser", price="720", category="Health & Beauty", description="Oil-free acne wash with salicylic acid"),
            ProductModel(name="Pantene Pro-V Conditioner", price=520, category="Health & Beauty", description="Daily moisture renewal conditioner"),
            ProductModel(name="Secret Deodorant", price=380, category="Health & Beauty", description="48-hour odor protection antiperspirant"),
            ProductModel(name="Advil Ibuprofen (200 count)", price=1250, category="Health & Beauty", description="Pain reliever and fever reducer tablets"),
            ProductModel(name="Olay Regenerist Moisturizer", price=2200, category="Health & Beauty", description="Anti-aging moisturizer with amino-peptides"),
            ProductModel(name="Gillette Fusion5 Razors (4-pack)", price=1800, category="Health & Beauty", description="Men's razor cartridges with 5 blades"),
            
            # Sports & Outdoors
            ProductModel(name="Coleman 4-Person Tent", price=8500, category="Sports & Outdoors", description="Dome tent with WeatherTec system for camping"),
            ProductModel(name="Spalding NBA Basketball", price=2200, category="Sports & Outdoors", description="Official size composite leather basketball"),
            ProductModel(name="Wilson Tennis Racket", price="4500", category="Sports & Outdoors", description="Adult tennis racket with graphite composite frame"),
            ProductModel(name="Lifetime Folding Table", price=6500, category="Sports & Outdoors", description="6-foot commercial grade folding table"),
            ProductModel(name="Ozark Trail Camping Chair", price="1200", category="Sports & Outdoors", description="Folding camping chair with cup holder"),
            ProductModel(name="Spalding Portable Basketball Hoop", price=25000, category="Sports & Outdoors", description="Adjustable height basketball system"),
            ProductModel(name="Coleman Camping Cooler (48-Quart)", price=5500, category="Sports & Outdoors", description="Wheeled cooler with 3-day ice retention"),
            ProductModel(name="Intex Easy Set Pool (10ft)", price=12000, category="Sports & Outdoors", description="Inflatable above-ground swimming pool"),
            ProductModel(name="Schwinn Mountain Bike", price=35000, category="Sports & Outdoors", description="21-speed mountain bike with front suspension"),
            ProductModel(name="CAP Barbell Dumbbell Set", price=18000, category="Sports & Outdoors", description="Adjustable dumbbell set, 40 lbs total weight"),
            
            # Toys & Games
            ProductModel(name="LEGO Classic Creative Bricks", price=4500, category="Toys", description="790-piece LEGO building set for creative play"),
            ProductModel(name="Barbie Dreamhouse", price="8500", category="Toys", description="3-story dollhouse with furniture and accessories"),
            ProductModel(name="Hot Wheels 20-Car Pack", price=2200, category="Toys", description="Set of 20 die-cast Hot Wheels cars"),
            ProductModel(name="Play-Doh Modeling Compound (20-Pack)", price=1800, category="Toys", description="Set of 20 different colored Play-Doh containers"),
            ProductModel(name="Monopoly Board Game", price=2800, category="Toys", description="Classic property trading board game for families"),
            ProductModel(name="Nerf Elite 2.0 Commander Blaster", price=3500, category="Toys", description="Toy blaster with 6-dart rotating drum"),
            ProductModel(name="Crayola Crayons (64-count)", price=650, category="Toys", description="Set of 64 crayons with built-in sharpener"),
            ProductModel(name="Fisher-Price Rock-a-Stack", price=1200, category="Toys", description="Classic stacking toy for infants and toddlers"),
            ProductModel(name="UNO Card Game", price=850, category="Toys", description="Classic family card game for 2-10 players"),
            ProductModel(name="Pokémon Trading Card Game Battle Deck", price=1500, category="Toys", description="Ready-to-play deck with 60 cards"),
        ]
        
        db.add_all(products)
        db.commit()
        print(f"Added {len(products)} products to database")

        # Generate realistic inventory data
        inventories = []
        for i in range(1, len(products) + 1):
            # Different inventory levels based on product category
            if i <= 10:  # Electronics - lower stock, higher threshold
                quantity = random.randint(5, 50)
                threshold = random.randint(5, 15)
            elif i <= 20:  # Home & Garden - medium stock
                quantity = random.randint(20, 100)
                threshold = random.randint(10, 25)
            elif i <= 30:  # Clothing - higher stock
                quantity = random.randint(50, 200)
                threshold = random.randint(20, 40)
            elif i <= 40:  # Grocery - very high stock, frequent turnover
                quantity = random.randint(100, 500)
                threshold = random.randint(50, 100)
            elif i <= 50:  # Health & Beauty - medium stock
                quantity = random.randint(30, 150)
                threshold = random.randint(15, 30)
            elif i <= 60:  # Sports & Outdoors - lower stock for large items
                quantity = random.randint(10, 80)
                threshold = random.randint(5, 20)
            else:  # Toys - seasonal variation
                quantity = random.randint(25, 120)
                threshold = random.randint(10, 25)
                
            inventories.append(
                InventoryModel(
                    product_id=i,
                    quantity=quantity,
                    last_updated=date.today() - timedelta(days=random.randint(0, 30)),
                    low_stock_threshold=threshold
                )
            )
        
        db.add_all(inventories)
        db.commit()
        print(f"Added {len(inventories)} inventory records to database")

        # Generate sales data for the past 30 days
        sales = []
        for day_offset in range(30):  # Last 30 days
            sale_date = date.today() - timedelta(days=day_offset)
            
            # Generate 5-20 sales per day
            daily_sales_count = random.randint(5, 20)
            
            for _ in range(daily_sales_count):
                product_id = random.randint(1, len(products))
                
                # Get product price (simplified - in real app you'd query the product)
                product_prices = {
                    1: 85000, 2: 120000, 3: 135000, 4: 35000, 5: 110000,
                    6: 95000, 7: 38000, 8: 28000, 9: 185000, 10: 15000,
                    11: 45000, 12: 65000, 13: 8500, 14: 12000, 15: 15000,
                    16: 4500, 17: 2500, 18: 18000, 19: 7500, 20: 3500,
                    21: 6500, 22: 12000, 23: 15000, 24: 3500, 25: 2000,
                    26: 4500, 27: 2800, 28: 8500, 29: 1800, 30: 3200,
                    31: 350, 32: 180, 33: 120, 34: 650, 35: 1200,
                    36: 450, 37: 280, 38: 520, 39: 150, 40: 320,
                    41: 450, 42: 580, 43: 650, 44: 880, 45: 720,
                    46: 520, 47: 380, 48: 1250, 49: 2200, 50: 1800,
                    51: 8500, 52: 2200, 53: 4500, 54: 6500, 55: 1200,
                    56: 25000, 57: 5500, 58: 12000, 59: 35000, 60: 18000,
                    61: 4500, 62: 8500, 63: 2200, 64: 1800, 65: 2800,
                    66: 3500, 67: 650, 68: 1200, 69: 850, 70: 1500
                }
                
                price = product_prices.get(product_id, 1000)
                
                # Quantity based on product type (higher value items sold in lower quantities)
                if price > 50000:  # High-value electronics
                    quantity = random.randint(1, 3)
                elif price > 10000:  # Mid-range items
                    quantity = random.randint(1, 5)
                elif price > 1000:  # Regular items
                    quantity = random.randint(1, 10)
                else:  # Low-cost items (groceries, etc.)
                    quantity = random.randint(1, 20)
                
                revenue = price * quantity
                
                sales.append(
                    SaleModel(
                        product_id=product_id,
                        quantity=quantity,
                        sale_date=sale_date,
                        revenue=revenue
                    )
                )
        
        db.add_all(sales)
        db.commit()
        print(f"Added {len(sales)} sales records to database")

    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    seed()
