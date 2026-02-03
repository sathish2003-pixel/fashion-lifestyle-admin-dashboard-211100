"""
Discount API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.crud import discounts as discount_crud
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/discounts", tags=["Discounts"])


@router.get("/", response_model=List[schemas.DiscountResponse], summary="Get all discounts")
def get_discounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all discounts with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of discounts
    """
    discounts = discount_crud.get_discounts(db, skip=skip, limit=limit)
    return discounts


@router.get("/active", response_model=List[schemas.DiscountResponse], summary="Get active discounts")
def get_active_discounts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all currently active discounts.
    
    Args:
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of active discounts
    """
    discounts = discount_crud.get_active_discounts(db)
    return discounts


@router.get("/{discount_id}", response_model=schemas.DiscountResponse, summary="Get discount by ID")
def get_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get a specific discount by ID.
    
    Args:
        discount_id: Discount ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Discount details
    """
    discount = discount_crud.get_discount(db, discount_id)
    if not discount:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.post("/", response_model=schemas.DiscountResponse, status_code=status.HTTP_201_CREATED, summary="Create discount")
def create_discount(
    discount: schemas.DiscountCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new discount.
    
    Args:
        discount: Discount creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created discount
    """
    return discount_crud.create_discount(db, discount)


@router.put("/{discount_id}", response_model=schemas.DiscountResponse, summary="Update discount")
def update_discount(
    discount_id: int,
    discount: schemas.DiscountUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing discount.
    
    Args:
        discount_id: Discount ID
        discount: Discount update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated discount
    """
    return discount_crud.update_discount(db, discount_id, discount)


@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete discount")
def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a discount.
    
    Args:
        discount_id: Discount ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        No content
    """
    discount_crud.delete_discount(db, discount_id)
    return None
