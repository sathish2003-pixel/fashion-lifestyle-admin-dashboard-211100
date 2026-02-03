"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Token schemas
class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


class UserLogin(BaseModel):
    """User login schema."""
    username: str
    password: str


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Product schemas
class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, description="Product name")
    sku: str = Field(..., min_length=1, description="Product SKU")
    description: Optional[str] = None
    category: Optional[str] = None
    price: float = Field(..., gt=0, description="Product price must be positive")
    cost: Optional[float] = Field(None, ge=0, description="Product cost")
    image_url: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    """Product creation schema."""
    pass


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    cost: Optional[float] = Field(None, ge=0)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Product response schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Customer schemas
class CustomerBase(BaseModel):
    """Base customer schema."""
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Customer creation schema."""
    pass


class CustomerUpdate(BaseModel):
    """Customer update schema."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Customer response schema."""
    id: int
    created_at: datetime
    total_spent: float
    total_orders: int

    class Config:
        from_attributes = True


# Order item schemas
class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    unit_price: float = Field(..., gt=0, description="Unit price must be positive")


class OrderItemCreate(OrderItemBase):
    """Order item creation schema."""
    pass


class OrderItemResponse(OrderItemBase):
    """Order item response schema."""
    id: int
    total_price: float

    class Config:
        from_attributes = True


# Order schemas
class OrderBase(BaseModel):
    """Base order schema."""
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    subtotal: float = Field(..., ge=0)
    tax: float = Field(default=0.0, ge=0)
    shipping: float = Field(default=0.0, ge=0)
    discount_amount: float = Field(default=0.0, ge=0)
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Order creation schema."""
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Order must have at least one item")


class OrderUpdate(BaseModel):
    """Order update schema."""
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    """Order response schema."""
    id: int
    order_number: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


# Inventory schemas
class InventoryBase(BaseModel):
    """Base inventory schema."""
    product_id: int
    quantity: int = Field(default=0, ge=0)
    reserved: int = Field(default=0, ge=0)
    available: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=10, ge=0)
    reorder_quantity: int = Field(default=50, gt=0)


class InventoryCreate(InventoryBase):
    """Inventory creation schema."""
    pass


class InventoryUpdate(BaseModel):
    """Inventory update schema."""
    quantity: Optional[int] = Field(None, ge=0)
    reserved: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    reorder_quantity: Optional[int] = Field(None, gt=0)


class InventoryResponse(InventoryBase):
    """Inventory response schema."""
    id: int
    last_restocked: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True


# Discount schemas
class DiscountBase(BaseModel):
    """Base discount schema."""
    code: str = Field(..., min_length=1)
    description: Optional[str] = None
    discount_type: str = Field(..., pattern="^(percentage|fixed)$")
    discount_value: float = Field(..., gt=0)
    min_purchase: float = Field(default=0.0, ge=0)
    max_discount: Optional[float] = Field(None, gt=0)
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    usage_limit: Optional[int] = Field(None, gt=0)

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class DiscountCreate(DiscountBase):
    """Discount creation schema."""
    pass


class DiscountUpdate(BaseModel):
    """Discount update schema."""
    description: Optional[str] = None
    discount_value: Optional[float] = Field(None, gt=0)
    min_purchase: Optional[float] = Field(None, ge=0)
    max_discount: Optional[float] = Field(None, gt=0)
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    usage_limit: Optional[int] = Field(None, gt=0)


class DiscountResponse(DiscountBase):
    """Discount response schema."""
    id: int
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Analytics schemas
class DashboardStats(BaseModel):
    """Dashboard statistics."""
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    avg_order_value: float
    revenue_growth: float
    orders_growth: float


class RevenueByPeriod(BaseModel):
    """Revenue aggregated by time period."""
    period: str
    revenue: float
    orders: int


class TopProduct(BaseModel):
    """Top selling product."""
    product_id: int
    product_name: str
    total_sold: int
    total_revenue: float


class AnalyticsResponse(BaseModel):
    """Analytics response."""
    dashboard_stats: DashboardStats
    revenue_by_day: List[RevenueByPeriod]
    top_products: List[TopProduct]
