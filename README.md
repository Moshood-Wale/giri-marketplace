# Artisan Marketplace API

A RESTful API for an artisan marketplace platform built with Django and PostgreSQL. This platform allows artisans to showcase their handmade products and customers to browse and purchase items.

## Features

- User Authentication with JWT
- Artisan Profile Management
- Product Management
- Order Processing
- Search and Filter Capabilities
- API Documentation with Swagger/ReDoc

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- Simple JWT for authentication
- drf-spectacular for API documentation

## Setup Instructions

1. Clone the repository:
git clone https://github.com/Moshood-Wale/giri-marketplace.git
cd giri-marketplace

2. Create and activate virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Create a .env file in the project root:
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/artisan_marketplace
JWT_SECRET_KEY=your-secret-key-here

5. Run migrations:
python manage.py migrate

6. Create superuser:
python manage.py createsuperuser

7. Run the development server:
python manage.py runserver

## API Documentation

API documentation is available at:

Swagger UI: /api/v1/doc/
ReDoc: /api/v1/redoc/

Main Endpoints
Authentication

POST /api/v1/auth/register/: Register new user
POST /api/v1/auth/login/: Get JWT tokens
POST /api/v1/auth/refresh/: Refresh JWT token

Artisans

GET /api/v1/artisans/: List all artisans
POST /api/v1/artisans/: Create artisan profile
GET /api/v1/artisans/{id}/: Retrieve artisan details
PUT /api/v1/artisans/{id}/: Update artisan profile
DELETE /api/v1/artisans/{id}/: Delete artisan profile

Products

GET /api/v1/products/: List all products (supports filtering and search)
POST /api/v1/products/: Create new product
GET /api/v1/products/{id}/: Retrieve product details
PUT /api/v1/products/{id}/: Update product
DELETE /api/v1/products/{id}/: Delete product

Orders

GET /api/v1/orders/: List user's orders
POST /api/v1/orders/: Create new order

## Design Decisions

Authentication:

Used JWT for stateless authentication
Email-based authentication instead of username
UUID fields for enhanced security


Models:

One-to-One relationship between User and Artisan
Products tied to specific Artisans
Order items stored separately for better data management

Permissions:

Authentication required for all endpoints
Artisans can only manage their own products
Users can only view their own orders

Pagination:

Implemented pagination for all list endpoints
Default page size: 10 items

## Testing
Run the test suite:
python manage.py test