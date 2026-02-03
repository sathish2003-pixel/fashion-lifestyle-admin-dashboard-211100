"""
Customer API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.crud import customers as customer_crud
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("/", response_model=List[schemas.CustomerResponse], summary="Get all customers")
def get_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all customers with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of customers
    """
    customers = customer_crud.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=schemas.CustomerResponse, summary="Get customer by ID")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get a specific customer by ID.
    
    Args:
        customer_id: Customer ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Customer details
    """
    customer = customer_crud.get_customer(db, customer_id)
    if not customer:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED, summary="Create new customer")
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new customer.
    
    Args:
        customer: Customer creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created customer
    """
    return customer_crud.create_customer(db, customer)


@router.put("/{customer_id}", response_model=schemas.CustomerResponse, summary="Update customer")
def update_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing customer.
    
    Args:
        customer_id: Customer ID
        customer: Customer update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated customer
    """
    return customer_crud.update_customer(db, customer_id, customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete customer")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a customer.
    
    Args:
        customer_id: Customer ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        No content
    """
    customer_crud.delete_customer(db, customer_id)
    return None
