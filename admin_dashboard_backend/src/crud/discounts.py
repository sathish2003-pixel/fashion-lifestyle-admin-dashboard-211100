"""
CRUD operations for discounts.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from src import models, schemas


# PUBLIC_INTERFACE
def get_discount(db: Session, discount_id: int) -> Optional[models.Discount]:
    """
    Get a discount by ID.
    
    Args:
        db: Database session
        discount_id: Discount ID
        
    Returns:
        Discount if found, None otherwise
    """
    return db.query(models.Discount).filter(models.Discount.id == discount_id).first()


# PUBLIC_INTERFACE
def get_discount_by_code(db: Session, code: str) -> Optional[models.Discount]:
    """
    Get a discount by code.
    
    Args:
        db: Database session
        code: Discount code
        
    Returns:
        Discount if found, None otherwise
    """
    return db.query(models.Discount).filter(models.Discount.code == code).first()


# PUBLIC_INTERFACE
def get_discounts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Discount]:
    """
    Get all discounts with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of discounts
    """
    return db.query(models.Discount).offset(skip).limit(limit).all()


# PUBLIC_INTERFACE
def get_active_discounts(db: Session) -> List[models.Discount]:
    """
    Get all active discounts.
    
    Args:
        db: Database session
        
    Returns:
        List of active discounts
    """
    now = datetime.utcnow()
    return db.query(models.Discount).filter(
        models.Discount.is_active == True,
        models.Discount.start_date <= now,
        models.Discount.end_date >= now
    ).all()


# PUBLIC_INTERFACE
def create_discount(db: Session, discount: schemas.DiscountCreate) -> models.Discount:
    """
    Create a new discount.
    
    Args:
        db: Database session
        discount: Discount creation data
        
    Returns:
        Created discount
        
    Raises:
        HTTPException: If code already exists
    """
    existing = get_discount_by_code(db, discount.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Discount with code '{discount.code}' already exists"
        )
    
    db_discount = models.Discount(**discount.model_dump())
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount


# PUBLIC_INTERFACE
def update_discount(
    db: Session,
    discount_id: int,
    discount: schemas.DiscountUpdate
) -> models.Discount:
    """
    Update a discount.
    
    Args:
        db: Database session
        discount_id: Discount ID
        discount: Discount update data
        
    Returns:
        Updated discount
        
    Raises:
        HTTPException: If discount not found
    """
    db_discount = get_discount(db, discount_id)
    if not db_discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Discount with ID {discount_id} not found"
        )
    
    update_data = discount.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_discount, field, value)
    
    db.commit()
    db.refresh(db_discount)
    return db_discount


# PUBLIC_INTERFACE
def delete_discount(db: Session, discount_id: int) -> bool:
    """
    Delete a discount.
    
    Args:
        db: Database session
        discount_id: Discount ID
        
    Returns:
        True if deleted
        
    Raises:
        HTTPException: If discount not found
    """
    db_discount = get_discount(db, discount_id)
    if not db_discount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Discount with ID {discount_id} not found"
        )
    
    db.delete(db_discount)
    db.commit()
    return True
