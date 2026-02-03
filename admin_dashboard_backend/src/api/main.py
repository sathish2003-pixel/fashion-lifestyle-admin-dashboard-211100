"""
Main FastAPI application for Fashion & Lifestyle Admin Dashboard Backend.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from src.database import engine, Base
from src.api.routes import auth, products, customers, orders, inventory, discounts, analytics

load_dotenv()

# Application metadata
app = FastAPI(
    title="Fashion & Lifestyle Admin Dashboard API",
    description="""
    Backend API for managing a fashion and lifestyle e-commerce admin dashboard.
    
    ## Features
    
    * **Authentication**: JWT-based authentication with user registration and login
    * **Products**: Complete CRUD operations for product management
    * **Customers**: Customer management with order history tracking
    * **Orders**: Order processing with status tracking and item management
    * **Inventory**: Real-time inventory tracking with reorder alerts
    * **Discounts**: Coupon and discount code management
    * **Analytics**: Dashboard statistics, revenue trends, and top product reports
    
    ## Authentication
    
    Most endpoints require authentication. Use the `/api/auth/register` endpoint to create an account,
    then `/api/auth/login` to get an access token. Include the token in the Authorization header:
    
    ```
    Authorization: Bearer <your_token_here>
    ```
    
    ## Database
    
    The API connects to a PostgreSQL database with the following entities:
    - Users (authentication)
    - Products (product catalog)
    - Customers (customer records)
    - Orders & Order Items (order management)
    - Inventory (stock management)
    - Discounts (promotional codes)
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints"
        },
        {
            "name": "Products",
            "description": "Product catalog management"
        },
        {
            "name": "Customers",
            "description": "Customer data management"
        },
        {
            "name": "Orders",
            "description": "Order processing and tracking"
        },
        {
            "name": "Inventory",
            "description": "Inventory and stock management"
        },
        {
            "name": "Discounts",
            "description": "Discount and coupon code management"
        },
        {
            "name": "Analytics",
            "description": "Dashboard analytics and reporting"
        }
    ]
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
ALLOWED_HEADERS = os.getenv("ALLOWED_HEADERS", "*").split(",")
ALLOWED_METHODS = os.getenv("ALLOWED_METHODS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "status_code": 500
        }
    )


# Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise


# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Returns service status and version information.
    """
    return {
        "message": "Fashion & Lifestyle Admin Dashboard API",
        "status": "healthy",
        "version": "1.0.0"
    }


# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(inventory.router)
app.include_router(discounts.router)
app.include_router(analytics.router)
