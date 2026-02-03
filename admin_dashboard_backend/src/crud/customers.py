"""
CRUD operations for customers.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src import models, schemas


# PUBLIC_INTERFACE
def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    """
    Get a customer by ID.
    
    Args:
        db: Database session
        customer_id: Customer ID
        
    Returns:
        Customer if found, None otherwise
    """
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


# PUBLIC_INTERFACE
def get_customer_by_email(db: Session, email: str) -> Optional[models.Customer]:
    """
    Get a customer by email.
    
    Args:
        db: Database session
        email: Customer email
        
    Returns:
        Customer if found, None otherwise
    """
    return db.query(models.Customer).filter(models.Customer.email == email).first()


# PUBLIC_INTERFACE
def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    """
    Get all customers with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of customers
    """
    return db.query(models.Customer).offset(skip).limit(limit).all()


# PUBLIC_INTERFACE
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    """
    Create a new customer.
    
    Args:
        db: Database session
        customer: Customer creation data
        
    Returns:
        Created customer
        
    Raises:
        HTTPException: If email already exists
    """
    existing = get_customer_by_email(db, customer.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with email '{customer.email}' already exists"
        )
    
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# PUBLIC_INTERFACE
def update_customer(
    db: Session,
    customer_id: int,
    customer: schemas.CustomerUpdate
) -> models.Customer:
    """
    Update a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
        customer: Customer update data
        
    Returns:
        Updated customer
        
    Raises:
        HTTPException: If customer not found
    """
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    
    update_data = customer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


# PUBLIC_INTERFACE
def delete_customer(db: Session, customer_id: int) -> bool:
    """
    Delete a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
        
    Returns:
        True if deleted
        
    Raises:
        HTTPException: If customer not found
    """
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    
    db.delete(db_customer)
    db.commit()
    return True
