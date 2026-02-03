"""
Product API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import get_db
from src import models, schemas
from src.crud import products as product_crud
from src.auth import get_current_active_user

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=List[schemas.ProductResponse], summary="Get all products")
def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all products with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of products
    """
    products = product_crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=schemas.ProductResponse, summary="Get product by ID")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get a specific product by ID.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Product details
    """
    product = product_crud.get_product(db, product_id)
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED, summary="Create new product")
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Create a new product.
    
    Args:
        product: Product creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created product
    """
    return product_crud.create_product(db, product)


@router.put("/{product_id}", response_model=schemas.ProductResponse, summary="Update product")
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Update an existing product.
    
    Args:
        product_id: Product ID
        product: Product update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated product
    """
    return product_crud.update_product(db, product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete product")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        No content
    """
    product_crud.delete_product(db, product_id)
    return None
