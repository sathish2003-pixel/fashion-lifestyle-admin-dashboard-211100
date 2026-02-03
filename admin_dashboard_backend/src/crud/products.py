"""
CRUD operations for products.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src import models, schemas


# PUBLIC_INTERFACE
def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Get a product by ID.
    
    Args:
        db: Database session
        product_id: Product ID
        
    Returns:
        Product if found, None otherwise
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


# PUBLIC_INTERFACE
def get_product_by_sku(db: Session, sku: str) -> Optional[models.Product]:
    """
    Get a product by SKU.
    
    Args:
        db: Database session
        sku: Product SKU
        
    Returns:
        Product if found, None otherwise
    """
    return db.query(models.Product).filter(models.Product.sku == sku).first()


# PUBLIC_INTERFACE
def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """
    Get all products with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of products
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


# PUBLIC_INTERFACE
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Create a new product.
    
    Args:
        db: Database session
        product: Product creation data
        
    Returns:
        Created product
        
    Raises:
        HTTPException: If SKU already exists
    """
    # Check if SKU already exists
    existing = get_product_by_sku(db, product.sku)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product.sku}' already exists"
        )
    
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# PUBLIC_INTERFACE
def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate
) -> models.Product:
    """
    Update a product.
    
    Args:
        db: Database session
        product_id: Product ID
        product: Product update data
        
    Returns:
        Updated product
        
    Raises:
        HTTPException: If product not found
    """
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


# PUBLIC_INTERFACE
def delete_product(db: Session, product_id: int) -> bool:
    """
    Delete a product.
    
    Args:
        db: Database session
        product_id: Product ID
        
    Returns:
        True if deleted
        
    Raises:
        HTTPException: If product not found
    """
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    db.delete(db_product)
    db.commit()
    return True
