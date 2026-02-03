"""
CRUD operations for inventory.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from src import models, schemas
from src.crud import products as product_crud


# PUBLIC_INTERFACE
def get_inventory(db: Session, inventory_id: int) -> Optional[models.Inventory]:
    """
    Get inventory by ID.
    
    Args:
        db: Database session
        inventory_id: Inventory ID
        
    Returns:
        Inventory if found, None otherwise
    """
    return db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()


# PUBLIC_INTERFACE
def get_inventory_by_product(db: Session, product_id: int) -> Optional[models.Inventory]:
    """
    Get inventory for a specific product.
    
    Args:
        db: Database session
        product_id: Product ID
        
    Returns:
        Inventory if found, None otherwise
    """
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()


# PUBLIC_INTERFACE
def get_all_inventory(db: Session, skip: int = 0, limit: int = 100) -> List[models.Inventory]:
    """
    Get all inventory records with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of inventory records
    """
    return db.query(models.Inventory).offset(skip).limit(limit).all()


# PUBLIC_INTERFACE
def create_inventory(db: Session, inventory: schemas.InventoryCreate) -> models.Inventory:
    """
    Create a new inventory record.
    
    Args:
        db: Database session
        inventory: Inventory creation data
        
    Returns:
        Created inventory
        
    Raises:
        HTTPException: If product not found or inventory already exists
    """
    # Verify product exists
    product = product_crud.get_product(db, inventory.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {inventory.product_id} not found"
        )
    
    # Check if inventory already exists for this product
    existing = get_inventory_by_product(db, inventory.product_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Inventory already exists for product ID {inventory.product_id}"
        )
    
    # Calculate available quantity
    available = inventory.quantity - inventory.reserved
    
    db_inventory = models.Inventory(
        **inventory.model_dump(),
        available=available,
        last_restocked=datetime.utcnow()
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# PUBLIC_INTERFACE
def update_inventory(
    db: Session,
    inventory_id: int,
    inventory: schemas.InventoryUpdate
) -> models.Inventory:
    """
    Update inventory.
    
    Args:
        db: Database session
        inventory_id: Inventory ID
        inventory: Inventory update data
        
    Returns:
        Updated inventory
        
    Raises:
        HTTPException: If inventory not found
    """
    db_inventory = get_inventory(db, inventory_id)
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory with ID {inventory_id} not found"
        )
    
    update_data = inventory.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_inventory, field, value)
    
    # Recalculate available quantity
    db_inventory.available = db_inventory.quantity - db_inventory.reserved
    
    db.commit()
    db.refresh(db_inventory)
    return db_inventory


# PUBLIC_INTERFACE
def delete_inventory(db: Session, inventory_id: int) -> bool:
    """
    Delete inventory.
    
    Args:
        db: Database session
        inventory_id: Inventory ID
        
    Returns:
        True if deleted
        
    Raises:
        HTTPException: If inventory not found
    """
    db_inventory = get_inventory(db, inventory_id)
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory with ID {inventory_id} not found"
        )
    
    db.delete(db_inventory)
    db.commit()
    return True
