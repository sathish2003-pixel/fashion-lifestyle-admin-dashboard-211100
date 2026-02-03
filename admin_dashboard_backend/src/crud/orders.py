"""
CRUD operations for orders.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import random
import string

from src import models, schemas
from src.crud import products as product_crud


def generate_order_number() -> str:
    """Generate a unique order number."""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{timestamp}-{random_str}"


# PUBLIC_INTERFACE
def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """
    Get an order by ID.
    
    Args:
        db: Database session
        order_id: Order ID
        
    Returns:
        Order if found, None otherwise
    """
    return db.query(models.Order).filter(models.Order.id == order_id).first()


# PUBLIC_INTERFACE
def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """
    Get all orders with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of orders
    """
    return db.query(models.Order).offset(skip).limit(limit).all()


# PUBLIC_INTERFACE
def get_customer_orders(db: Session, customer_id: int) -> List[models.Order]:
    """
    Get all orders for a specific customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
        
    Returns:
        List of customer orders
    """
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()


# PUBLIC_INTERFACE
def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """
    Create a new order.
    
    Args:
        db: Database session
        order: Order creation data
        
    Returns:
        Created order
        
    Raises:
        HTTPException: If customer not found or products don't exist
    """
    # Verify customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {order.customer_id} not found"
        )
    
    # Calculate total amount
    total_amount = order.subtotal + order.tax + order.shipping - order.discount_amount
    
    # Create order
    db_order = models.Order(
        order_number=generate_order_number(),
        customer_id=order.customer_id,
        status=order.status,
        subtotal=order.subtotal,
        tax=order.tax,
        shipping=order.shipping,
        discount_amount=order.discount_amount,
        total_amount=total_amount,
        notes=order.notes
    )
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items
    for item in order.items:
        # Verify product exists
        product = product_crud.get_product(db, item.product_id)
        if not product:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
        
        total_price = item.quantity * item.unit_price
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=total_price
        )
        db.add(db_item)
    
    # Update customer stats
    customer.total_orders += 1
    customer.total_spent += total_amount
    
    db.commit()
    db.refresh(db_order)
    return db_order


# PUBLIC_INTERFACE
def update_order(
    db: Session,
    order_id: int,
    order: schemas.OrderUpdate
) -> models.Order:
    """
    Update an order.
    
    Args:
        db: Database session
        order_id: Order ID
        order: Order update data
        
    Returns:
        Updated order
        
    Raises:
        HTTPException: If order not found
    """
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    update_data = order.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


# PUBLIC_INTERFACE
def delete_order(db: Session, order_id: int) -> bool:
    """
    Delete an order.
    
    Args:
        db: Database session
        order_id: Order ID
        
    Returns:
        True if deleted
        
    Raises:
        HTTPException: If order not found
    """
    db_order = get_order(db, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    db.delete(db_order)
    db.commit()
    return True
