# Fashion & Lifestyle Admin Dashboard - Backend API

FastAPI backend server for the Fashion & Lifestyle e-commerce admin dashboard.

## Features

- **Authentication**: JWT-based authentication with user registration and login
- **Products**: Complete CRUD operations for product catalog management
- **Customers**: Customer management with order history tracking
- **Orders**: Order processing with status tracking and line items
- **Inventory**: Real-time inventory management with stock tracking
- **Discounts**: Coupon and promotional code management
- **Analytics**: Dashboard KPIs, revenue trends, and top product reports

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: Secure authentication tokens
- **Bcrypt**: Password hashing

## Prerequisites

- Python 3.9+
- PostgreSQL database running (configured via environment variables)
- pip or pip3 package manager

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

The database connection variables (POSTGRES_URL, POSTGRES_USER, etc.) are set automatically by the orchestrator from the database container.

## Database Setup

The database tables are created automatically on first startup. To populate with sample data:

```bash
python -m src.init_db
```

This creates:
- 2 test users (admin/admin123, user/user123)
- 20 sample products across different categories
- 20 sample customers
- 50 sample orders with order items
- Inventory records for all products
- 5 discount codes

## Running the Server

### Using the startup script (recommended):
```bash
chmod +x start.sh
./start.sh
```

### Manual start:
```bash
# Initialize database (first time only)
python -m src.init_db

# Generate OpenAPI spec
python -m src.api.generate_openapi

# Start server
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

The API will be available at:
- API: http://localhost:3001
- Swagger docs: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc
- OpenAPI spec: http://localhost:3001/openapi.json

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer by ID
- `POST /api/customers` - Create customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Orders
- `GET /api/orders` - List all orders
- `GET /api/orders/{id}` - Get order by ID
- `POST /api/orders` - Create order
- `PUT /api/orders/{id}` - Update order
- `DELETE /api/orders/{id}` - Delete order

### Inventory
- `GET /api/inventory` - List all inventory
- `GET /api/inventory/{id}` - Get inventory by ID
- `GET /api/inventory/product/{product_id}` - Get inventory by product
- `POST /api/inventory` - Create inventory record
- `PUT /api/inventory/{id}` - Update inventory
- `DELETE /api/inventory/{id}` - Delete inventory

### Discounts
- `GET /api/discounts` - List all discounts
- `GET /api/discounts/active` - List active discounts
- `GET /api/discounts/{id}` - Get discount by ID
- `POST /api/discounts` - Create discount
- `PUT /api/discounts/{id}` - Update discount
- `DELETE /api/discounts/{id}` - Delete discount

### Analytics
- `GET /api/analytics` - Get comprehensive analytics
- `GET /api/analytics/dashboard` - Get dashboard statistics

## Authentication

Most endpoints require authentication. To authenticate:

1. Register or login to get a JWT token:
```bash
curl -X POST "http://localhost:3001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

2. Use the token in subsequent requests:
```bash
curl -X GET "http://localhost:3001/api/products" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Database Schema

### Users
- Authentication and user management

### Products
- Product catalog with SKU, pricing, categories

### Customers
- Customer information and contact details

### Orders
- Order headers with customer, status, totals

### OrderItems
- Line items for each order

### Inventory
- Stock levels, reorder points for each product

### Discounts
- Promotional codes with validity periods and usage limits

## Development

### Running tests:
```bash
pytest
```

### Code quality:
```bash
flake8 src/
```

### Generate OpenAPI spec:
```bash
python -m src.api.generate_openapi
```

## CORS Configuration

CORS is configured to allow requests from the frontend. Configure allowed origins in `.env`:

```
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

## Environment Variables

Key environment variables:

- `POSTGRES_URL` - Full PostgreSQL connection string
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name
- `POSTGRES_PORT` - Database port
- `SECRET_KEY` - JWT secret key (min 32 characters)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `ALLOWED_ORIGINS` - CORS allowed origins
- `PORT` - Server port (default: 3001)

## Project Structure

```
admin_dashboard_backend/
├── src/
│   ├── api/
│   │   ├── routes/          # API endpoint routers
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── customers.py
│   │   │   ├── orders.py
│   │   │   ├── inventory.py
│   │   │   ├── discounts.py
│   │   │   └── analytics.py
│   │   ├── main.py          # FastAPI app instance
│   │   └── generate_openapi.py
│   ├── crud/                # Database CRUD operations
│   │   ├── products.py
│   │   ├── customers.py
│   │   ├── orders.py
│   │   ├── inventory.py
│   │   └── discounts.py
│   ├── services/            # Business logic
│   │   └── analytics.py
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   └── init_db.py           # Database initialization
├── interfaces/
│   └── openapi.json         # OpenAPI specification
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.example             # Example environment variables
├── start.sh                 # Startup script
└── README.md               # This file
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc

## Support

For issues or questions, please check:
1. The API documentation at `/docs`
2. The OpenAPI specification at `/openapi.json`
3. The application logs for error messages
