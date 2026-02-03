"""
Database initialization script with sample data for testing.
This script should be run once to populate the database with initial data.
"""
from datetime import datetime, timedelta
import random

from src.database import SessionLocal, engine, Base
from src import models
from src.auth import get_password_hash


def init_db():
    """Initialize database with sample data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(models.User).count()
        if existing_users > 0:
            print("Database already initialized. Skipping...")
            return
        
        print("Creating sample users...")
        # Create admin user
        admin = models.User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin)
        
        # Create regular user
        user = models.User(
            email="user@example.com",
            username="user",
            full_name="Regular User",
            hashed_password=get_password_hash("user123")
        )
        db.add(user)
        db.flush()
        
        print("Creating sample products...")
        categories = ["Dresses", "Tops", "Bottoms", "Outerwear", "Accessories"]
        products = []
        
        for i in range(1, 21):
            category = random.choice(categories)
            product = models.Product(
                name=f"{category[:-1]} Item {i}",
                sku=f"SKU-{category[:3].upper()}-{1000+i}",
                description=f"Premium quality {category.lower()} for fashion-forward individuals.",
                category=category,
                price=round(random.uniform(29.99, 299.99), 2),
                cost=round(random.uniform(15.00, 150.00), 2),
                image_url=f"/assets/product-{i}.jpg",
                is_active=True
            )
            db.add(product)
            products.append(product)
        
        db.flush()
        
        print("Creating sample inventory...")
        for product in products:
            quantity = random.randint(50, 500)
            reserved = random.randint(0, 20)
            inventory = models.Inventory(
                product_id=product.id,
                quantity=quantity,
                reserved=reserved,
                available=quantity - reserved,
                reorder_level=random.randint(10, 30),
                reorder_quantity=random.randint(50, 100),
                last_restocked=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(inventory)
        
        print("Creating sample customers...")
        customers = []
        first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Isabella", "William"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
        
        for i in range(20):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            customer = models.Customer(
                first_name=first_name,
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
                phone=f"+1-555-{random.randint(1000, 9999)}",
                address=f"{random.randint(100, 9999)} Main St",
                city=random.choice(cities),
                country="USA",
                postal_code=f"{random.randint(10000, 99999)}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365))
            )
            db.add(customer)
            customers.append(customer)
        
        db.flush()
        
        print("Creating sample orders...")
        statuses = [models.OrderStatus.PENDING, models.OrderStatus.PROCESSING, 
                   models.OrderStatus.SHIPPED, models.OrderStatus.DELIVERED]
        
        for i in range(50):
            customer = random.choice(customers)
            subtotal = 0
            order_items_count = random.randint(1, 5)
            
            order = models.Order(
                order_number=f"ORD-{datetime.now().strftime('%Y%m%d')}-{10000+i}",
                customer_id=customer.id,
                status=random.choice(statuses),
                subtotal=0,  # Will be calculated
                tax=0,
                shipping=random.choice([0, 5.99, 9.99, 14.99]),
                discount_amount=random.choice([0, 0, 0, 5, 10, 15]),
                total_amount=0,  # Will be calculated
                notes="",
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
            )
            db.add(order)
            db.flush()
            
            # Add order items
            selected_products = random.sample(products, order_items_count)
            for product in selected_products:
                quantity = random.randint(1, 3)
                unit_price = product.price
                total_price = quantity * unit_price
                subtotal += total_price
                
                order_item = models.OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                db.add(order_item)
            
            # Update order totals
            order.subtotal = subtotal
            order.tax = round(subtotal * 0.08, 2)  # 8% tax
            order.total_amount = order.subtotal + order.tax + order.shipping - order.discount_amount
            
            # Update customer stats
            customer.total_orders += 1
            customer.total_spent += order.total_amount
        
        print("Creating sample discounts...")
        discount_codes = [
            ("WELCOME10", "percentage", 10, "Welcome discount for new customers"),
            ("SUMMER25", "percentage", 25, "Summer sale - 25% off"),
            ("SAVE50", "fixed", 50, "Save $50 on orders over $200"),
            ("FLASH20", "percentage", 20, "Flash sale - 20% off"),
            ("VIP15", "percentage", 15, "VIP member exclusive discount")
        ]
        
        for code, disc_type, value, desc in discount_codes:
            discount = models.Discount(
                code=code,
                description=desc,
                discount_type=disc_type,
                discount_value=value,
                min_purchase=100 if disc_type == "fixed" else 0,
                max_discount=100 if disc_type == "percentage" else None,
                start_date=datetime.utcnow() - timedelta(days=7),
                end_date=datetime.utcnow() + timedelta(days=30),
                is_active=True,
                usage_limit=random.randint(50, 200),
                usage_count=random.randint(0, 30)
            )
            db.add(discount)
        
        db.commit()
        print("Database initialized successfully with sample data!")
        print("\nTest credentials:")
        print("Admin - username: admin, password: admin123")
        print("User - username: user, password: user123")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
