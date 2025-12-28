# Quick Start Guide

This guide will help you get started with the FastAPI Template quickly.

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.11 or higher installed
- PostgreSQL installed (or use Docker)
- Poetry or pip for package management
- Git for version control

## 🚀 Quick Setup (5 minutes)

### Step 1: Clone and Install

```bash
# Clone the repository
git clone <your-repo-url>
cd fastapi-template

# Install dependencies
poetry install  # or: pip install -r requirements.txt
poetry shell    # or: source venv/bin/activate
```

### Step 2: Configure Database

**Option A: Using Docker (Recommended)**
```bash
# Start PostgreSQL container
docker-compose up -d

# Database is now running at localhost:5432
# Default credentials:
#   - User: api_user
#   - Password: api_password
#   - Database: api_database
```

**Option B: Using Local PostgreSQL**
```bash
# Create a database
createdb api_database

# Copy environment file
cp .env.example .env

# Edit .env and update DB_URL
# DB_URL=postgresql+asyncpg://your_user:your_password@localhost/api_database
```

### Step 3: Run Migrations

```bash
# Apply database migrations
alembic upgrade head
```

### Step 4: Start the API

```bash
# Run the development server
uvicorn api.main:app --reload

# API is now running at: http://localhost:8000
# Documentation at: http://localhost:8000/docs
```

### Step 5: Test the API

Visit http://localhost:8000/docs and try these endpoints:

**Authentication:**
- **POST /auth/register** - Create a new user account
- **POST /auth/login** - Login and get JWT token
- **GET /auth/me** - Get current user info (requires token)

**Example Entities (Protected):**
- **POST /examples** - Create a new example entity (requires authentication)
- **GET /examples** - List all entities
- **GET /examples/{id}** - Get entity by ID
- **PATCH /examples/{id}** - Update entity (requires authentication)
- **DELETE /examples/{id}** - Delete entity (requires authentication)

#### Testing with Authentication

1. Register a user via `/auth/register`
2. Login via `/auth/login` to get your token
3. In Swagger UI, click the "Authorize" button (🔒 icon at top right)
4. Enter: `Bearer YOUR_TOKEN_HERE`
5. Now you can access protected endpoints!

## 🛠️ Creating Your First Entity

### 1. Create the Entity Folder

```bash
# Create a new entity folder (e.g., "products")
mkdir -p api/products
touch api/products/__init__.py
touch api/products/models.py
touch api/products/schemas.py
touch api/products/controller.py
```

### 2. Define the Model (`api/products/models.py`)

```python
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from api.contrib.models import BaseModel

class ProductModel(BaseModel):
    __tablename__ = 'products'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
```

### 3. Define Schemas (`api/products/schemas.py`)

```python
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from api.contrib.schemas import BaseSchema, OutMixin

class Product(BaseSchema):
    name: Annotated[str, Field(max_length=100)]
    price: Annotated[PositiveFloat, Field(ge=0)]
    description: Annotated[Optional[str], Field(None, max_length=500)]

class ProductIn(Product):
    pass

class ProductOut(Product, OutMixin):
    pass

class ProductUpdate(BaseSchema):
    name: Annotated[Optional[str], Field(None, max_length=100)]
    price: Annotated[Optional[PositiveFloat], Field(None, ge=0)]
    description: Annotated[Optional[str], Field(None, max_length=500)]
```

### 4. Create Controller (`api/products/controller.py`)

```python
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate

from api.contrib.dependencies import DatabaseDependency
from .schemas import ProductIn, ProductOut, ProductUpdate
from .models import ProductModel

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(
    db_session: DatabaseDependency,
    product_in: ProductIn = Body(...)
):
    product_out = ProductOut(
        id=uuid4(),
        created_at=datetime.utcnow(),
        **product_in.model_dump()
    )
    product_model = ProductModel(**product_out.model_dump())
    db_session.add(product_model)
    await db_session.commit()
    return product_out

@router.get('/', response_model=Page[ProductOut])
async def get_products(db_session: DatabaseDependency):
    result = await db_session.execute(select(ProductModel))
    products = result.scalars().all()
    return paginate([ProductOut.model_validate(p) for p in products])

# Add more endpoints...
```

### 5. Register Router (`api/routers.py`)

```python
from fastapi import APIRouter
from api.products.controller import router as products_router

api_router = APIRouter()
api_router.include_router(products_router, prefix='/products', tags=['products'])
```

### 6. Import Model in Alembic (`alembic/env.py`)

```python
# Add this import with the other model imports
from api.products.models import ProductModel
```

### 7. Create and Run Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Add products table"

# Review the generated file in alembic/versions/

# Apply migration
alembic upgrade head
```

### 8. Test Your New Endpoints

Visit http://localhost:8000/docs and you'll see your new product endpoints!

## 📚 Next Steps

- **Add Authentication**: Uncomment auth examples in `api/contrib/dependencies.py`
- **Add Relationships**: See relationship examples in `api/example_entity/models.py`
- **Add Validation**: Explore Pydantic validators in schemas
- **Add Tests**: Create test files using pytest
- **Configure CORS**: Add CORS middleware in `api/main.py`
- **Add Logging**: Configure logging for production

## 🔍 Useful Commands

```bash
# Start API server
uvicorn api.main:app --reload

# Start with different host/port
uvicorn api.main:app --host 0.0.0.0 --port 8080

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current

# View migration history
alembic history

# Format code (if you have black installed)
black api/

# Lint code (if you have ruff installed)
ruff check api/
```

## ❓ Common Issues

### Database connection error
- Check if PostgreSQL is running: `docker-compose ps`
- Verify DB_URL in .env file
- Test connection: `psql -h localhost -U api_user -d api_database`

### Alembic can't detect changes
- Ensure model is imported in `alembic/env.py`
- Check that model inherits from `BaseModel`
- Verify model is in a registered entity folder

### Import errors
- Make sure you're in the virtual environment: `poetry shell`
- Reinstall dependencies: `poetry install`
- Check Python version: `python --version` (should be 3.11+)

## 🆘 Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review the `example_entity` module for reference implementations
- Read FastAPI docs: https://fastapi.tiangolo.com/
- Read SQLAlchemy docs: https://docs.sqlalchemy.org/

Happy coding! 🎉
