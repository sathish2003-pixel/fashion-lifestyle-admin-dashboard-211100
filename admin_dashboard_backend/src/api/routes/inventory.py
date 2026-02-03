"""
Inventory API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.crud import inventory as inventory_crud
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("/", response_model=List[schemas.InventoryResponse], summary="Get all inventory")
def get_all_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all inventory records with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of inventory records
    """
    inventory = inventory_crud.get_all_inventory(db, skip=skip, limit=limit)
    return inventory


@router.get("/{inventory_id}", response_model=schemas.InventoryResponse, summary="Get inventory by ID")
def get_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get specific inventory record by ID.
    
    Args:
        inventory_id: Inventory ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Inventory details
    """
    inventory = inventory_crud.get_inventory(db, inventory_id)
    if not inventory:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.get("/product/{product_id}", response_model=schemas.InventoryResponse, summary="Get inventory by product ID")
def get_inventory_by_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get inventory for a specific product.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Inventory details for the product
    """
    inventory = inventory_crud.get_inventory_by_product(db, product_id)
    if not inventory:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Inventory not found for this product")
    return inventory


@router.post("/", response_model=schemas.InventoryResponse, status_code=status.HTTP_201_CREATED, summary="Create inventory")
def create_inventory(
    inventory: schemas.InventoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new inventory record.
    
    Args:
        inventory: Inventory creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created inventory
    """
    return inventory_crud.create_inventory(db, inventory)


@router.put("/{inventory_id}", response_model=schemas.InventoryResponse, summary="Update inventory")
def update_inventory(
    inventory_id: int,
    inventory: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing inventory record.
    
    Args:
        inventory_id: Inventory ID
        inventory: Inventory update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated inventory
    """
    return inventory_crud.update_inventory(db, inventory_id, inventory)


@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete inventory")
def delete_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete an inventory record.
    
    Args:
        inventory_id: Inventory ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        No content
    """
    inventory_crud.delete_inventory(db, inventory_id)
    return None
