"""
Order API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.crud import orders as order_crud
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("/", response_model=List[schemas.OrderResponse], summary="Get all orders")
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all orders with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of orders
    """
    orders = order_crud.get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=schemas.OrderResponse, summary="Get order by ID")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get a specific order by ID.
    
    Args:
        order_id: Order ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Order details
    """
    order = order_crud.get_order(db, order_id)
    if not order:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED, summary="Create new order")
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new order.
    
    Args:
        order: Order creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created order
    """
    return order_crud.create_order(db, order)


@router.put("/{order_id}", response_model=schemas.OrderResponse, summary="Update order")
def update_order(
    order_id: int,
    order: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing order.
    
    Args:
        order_id: Order ID
        order: Order update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated order
    """
    return order_crud.update_order(db, order_id, order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete order")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete an order.
    
    Args:
        order_id: Order ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        No content
    """
    order_crud.delete_order(db, order_id)
    return None
