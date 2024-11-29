# Artisan Marketplace API

A RESTful API for an artisan marketplace platform built with Django and PostgreSQL. This platform enables artisans to showcase handmade products and customers to browse and purchase items.

## Features
- **User Authentication**: Secure JWT-based authentication.
- **Artisan Profile Management**: Manage artisan profiles.
- **Product Management**: Add, update, and delete products.
- **Order Processing**: Handle customer orders efficiently.
- **Search & Filter**: Find artisans and products quickly.
- **API Documentation**: Swagger and ReDoc integration.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Simple JWT
- **API Documentation**: drf-spectacular

## Setup Instructions
### Clone the Repository
`git clone https://github.com/Moshood-Wale/giri-marketplace.git`  
`cd giri-marketplace`

### Create and Activate a Virtual Environment
`python -m venv venv`  
**Linux/Mac**: `source venv/bin/activate`  
**Windows**: `venv\Scripts\activate`

### Install Dependencies
`pip install -r requirements.txt`

### Configure Environment Variables
Create a `.env` file in the project root and add the following:  

SECRET_KEY=your-secret-key-here

DATABASE_URL=postgresql://user:password@localhost:5432/artisan_marketplace

JWT_SECRET_KEY=your-secret-key-here


### Run Migrations
`python manage.py migrate`

### Create a Superuser
`python manage.py createsuperuser`

### Run the Development Server
`python manage.py runserver`

## API Documentation
- **Swagger UI**: `/api/v1/doc/`
- **ReDoc**: `/api/v1/redoc/`

## Main Endpoints
### Authentication
- **POST** `/api/v1/auth/register/`: Register new users.
- **POST** `/api/v1/auth/login/`: Obtain JWT tokens.
- **POST** `/api/v1/auth/refresh/`: Refresh JWT tokens.

### Artisans
- **GET** `/api/v1/artisans/`: List all artisans.
- **POST** `/api/v1/artisans/`: Create artisan profiles.
- **GET** `/api/v1/artisans/{id}/`: Retrieve artisan details.
- **PUT** `/api/v1/artisans/{id}/`: Update artisan profiles.
- **DELETE** `/api/v1/artisans/{id}/`: Delete artisan profiles.

### Products
- **GET** `/api/v1/products/`: List all products (supports filtering and search).
- **POST** `/api/v1/products/`: Create new products.
- **GET** `/api/v1/products/{id}/`: Retrieve product details.
- **PUT** `/api/v1/products/{id}/`: Update products.
- **DELETE** `/api/v1/products/{id}/`: Delete products.

### Orders
- **GET** `/api/v1/orders/`: List user orders.
- **POST** `/api/v1/orders/`: Create new orders.

## Design Decisions
### Authentication
- Used JWT for stateless authentication.
- Email-based authentication instead of username.
- UUID fields for enhanced security.

### Models
- One-to-One relationship between User and Artisan.
- Products tied to specific Artisans.
- Order items stored separately for better data management.

### Permissions
- Authentication required for all endpoints.
- Artisans can only manage their own products.
- Users can only view their own orders.

### Pagination
- Implemented pagination for all list endpoints.
- Default page size: 10 items.

## Testing
Run the test suite:  
`python manage.py test`
