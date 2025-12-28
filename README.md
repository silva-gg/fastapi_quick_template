# FastAPI Template

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-11-blue.svg)](https://www.postgresql.org/)

**A straightforward, no-nonsense REST API template built with FastAPI.** Unlike other complex templates, this one focuses on simplicity and ease of understanding - perfect for developers who want to get started quickly without wading through layers of abstraction.

## 🎯 Why This Template?

**Simple & Direct** - No over-engineering, no unnecessary abstractions. Just clean, readable code that does what it needs to do.

**Easy to Understand** - Extensively commented with clear instructions in every file. You'll know exactly what's happening and why.

**Ready to Use** - Comes with authentication, pagination, and database migrations already configured. Start building your features immediately.

**Production-Ready** - Despite its simplicity, this template includes everything you need for a production API: JWT auth, password hashing, error handling, and database migrations.

### Compared to Other Templates:

| Feature | This Template | Complex Templates |
|---------|--------------|-------------------|
| **Learning Curve** | ✅ Gentle - Easy to understand | ❌ Steep - Many layers to learn |
| **Setup Time** | ✅ 5 minutes | ❌ 30+ minutes |
| **Code Clarity** | ✅ Direct and readable | ❌ Abstract and scattered |
| **Documentation** | ✅ Extensive inline comments | ❌ Often minimal |
| **Authentication** | ✅ Included & Simple | ⚠️ Complex or missing |
| **Flexibility** | ✅ Easy to modify | ❌ Rigid structure |

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Authentication](#-authentication)
- [Project Structure](#-project-structure)
- [Creating Your First Entity](#-creating-your-first-entity)
- [Documentation](#-documentation)

## ✨ Features

### Core Features
- **🔐 JWT Authentication** - Secure user authentication with password hashing (bcrypt)
- **👤 User Management** - Complete user registration, login, and profile management
- **⚡ Asynchronous** - Full async/await support for optimal performance
- **📄 Auto Documentation** - Interactive Swagger UI and ReDoc
- **📊 Pagination** - Built-in pagination for all list endpoints
- **🗄️ Database Migrations** - Version control for your database with Alembic
- **🐳 Docker Support** - PostgreSQL container included
- **🛡️ Type Safety** - Full type hints with Pydantic validation

### What Makes It Simple
- **Clear File Organization** - One entity = one folder with models, schemas, and controllers
- **Extensive Comments** - Every file explains what it does and how to use it
- **Working Examples** - Full CRUD example with authentication
- **Step-by-Step Guides** - Detailed instructions for common tasks
- **No Hidden Magic** - Explicit code that's easy to follow and modify

## 🚀 Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for Python
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints
- **[PostgreSQL](https://www.postgresql.org/)** - Powerful, open source database
- **[JWT](https://jwt.io/)** - JSON Web Tokens for authentication
- **[Bcrypt](https://github.com/pyca/bcrypt/)** - Password hashing
- **[Docker](https://www.docker.com/)** - Containerization platform

## 📦 Prerequisites

- Python 3.11 or higher
- PostgreSQL (or use the included Docker setup)
- pip or Poetry for package management

## ⚡ Quick Start

Get your API running in 5 minutes:

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd fastapi-template

# 2. Install dependencies
pip install -r requirements.txt
# or with Poetry: poetry install && poetry shell

# 3. Start database
docker-compose up -d

# 4. Copy environment file
cp .env.example .env
# Edit .env if needed (defaults work with Docker)

# 5. Run migrations
alembic upgrade head

# 6. Start the API
uvicorn api.main:app --reload
```

**That's it!** Your API is now running at http://localhost:8000

Visit http://localhost:8000/docs to see the interactive documentation.

## 🔐 Authentication

This template includes a complete authentication system that's simple to understand and use.

### Registration

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using Protected Endpoints

```bash
# Get current user info
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create a protected resource
curl -X POST "http://localhost:8000/examples" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Item", "value": 99.99}'
```

### Protecting Your Endpoints

It's incredibly simple to protect your endpoints:

```python
from api.contrib.dependencies import CurrentUser

@router.get('/protected')
async def protected_route(current_user: CurrentUser):
    return {"message": f"Hello {current_user.username}!"}
```

For admin-only endpoints:

```python
from api.contrib.dependencies import RequireAdmin

@router.delete('/admin/sensitive')
async def admin_only(admin: RequireAdmin):
    return {"message": "Admin access granted"}
```

## 📁 Project Structure

```
fastapi-template/
├── api/                          # Main API package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── routers.py                # API router configuration
│   ├── configs/                  # Configuration files
│   │   ├── __init__.py
│   │   ├── database.py           # Database connection setup
│   │   └── settings.py           # Application settings
│   ├── contrib/                  # Shared/common modules
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Shared dependencies
│   │   ├── models.py             # Base database models
│   │   └── schemas.py            # Base Pydantic schemas
│   └── example_entity/           # Example entity module (template)
│       ├── __init__.py
│       ├── controller.py         # API endpoints
│       ├── models.py             # Database models
│       └── schemas.py            # Pydantic schemas
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration versions
│   └── env.py                    # Alembic environment
├── alembic.ini                   # Alembic configuration
├── docker-compose.yml            # Docker services
├── pyproject.toml                # Project dependencies
├── requirements.txt              # Pip dependencies
└── README.md                     # This file
```

## 🛠️ Implementing Your API

### Step 1: Create a New Entity

1. **Create a new folder** under `api/` with your entity name (e.g., `api/products/`)

2. **Create the following files**:
   - `__init__.py` - Empty file to mark as Python package
   - `models.py` - Database models
   - `schemas.py` - Pydantic schemas for validation
   - `controller.py` - API endpoints (CRUD operations)

### Step 2: Define Your Model (models.py)

```python
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from api.contrib.models import BaseModel

class YourEntityModel(BaseModel):
    __tablename__ = 'your_entities'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    # Add your fields here
```

### Step 3: Define Your Schemas (schemas.py)

```python
from typing import Annotated, Optional
from pydantic import Field
from api.contrib.schemas import BaseSchema, OutMixin

class YourEntity(BaseSchema):
    name: Annotated[str, Field(description='Entity name', example='Example', max_length=100)]
    description: Annotated[Optional[str], Field(None, description='Entity description', max_length=500)]
    # Add your fields here

class YourEntityIn(YourEntity):
    pass

class YourEntityOut(YourEntity, OutMixin):
    pass

class YourEntityUpdate(BaseSchema):
    name: Annotated[Optional[str], Field(None, description='Entity name', max_length=100)]
    description: Annotated[Optional[str], Field(None, description='Entity description', max_length=500)]
    # Add optional fields for updates
```

### Step 4: Create Your Controller (controller.py)

```python
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate

from .schemas import YourEntityIn, YourEntityOut, YourEntityUpdate
from .models import YourEntityModel

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=YourEntityOut)
async def create(db_session: DatabaseDependency, entity_in: YourEntityIn = Body(...)):
    entity_out = YourEntityOut(id=uuid4(), created_at=datetime.utcnow(), **entity_in.model_dump())
    entity_model = YourEntityModel(**entity_out.model_dump())
    
    db_session.add(entity_model)
    await db_session.commit()
    
    return entity_out

@router.get('/', response_model=Page[YourEntityOut])
async def get_all(db_session: DatabaseDependency):
    result = await db_session.execute(select(YourEntityModel))
    entities = result.scalars().all()
    return paginate([YourEntityOut.model_validate(e) for e in entities])

# Add more endpoints: get_by_id, update, delete, etc.
```

### Step 5: Register Your Router

In `api/routers.py`:

```python
from fastapi import APIRouter
from api.your_entity.controller import router as your_entity_router

api_router = APIRouter()
api_router.include_router(your_entity_router, prefix='/your-entities', tags=['your-entities'])
```

### Step 6: Create Migration

```bash
alembic revision --autogenerate -m "Add your_entity table"
alembic upgrade head
```

### Step 7: Test Your API

Visit http://localhost:8000/docs to see and test your new endpoints!

## 📝 Example Entity Module

The template includes an `example_entity` module that demonstrates the complete structure. Use it as a reference when creating your own entities:

- **models.py**: Shows how to define database models with SQLAlchemy
- **schemas.py**: Shows how to create Pydantic schemas for validation
- **controller.py**: Shows how to implement CRUD endpoints with proper error handling

## 🤝 Best Practices

This template follows these simple principles:

1. **One Entity = One Folder** - Keep related code together
2. **Always Use Type Hints** - Makes code self-documenting
3. **Validate Everything** - Use Pydantic schemas for all inputs
4. **Handle Errors Gracefully** - Return proper HTTP status codes
5. **Use Async** - All database operations should be async
6. **Protect Your Endpoints** - Use `CurrentUser` dependency for auth
7. **Comment Your Code** - Explain the "why", not just the "what"

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)** - Detailed development instructions
- **[IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)** - Step-by-step checklist

## 🔒 Security Notes

- **Change SECRET_KEY in production!** Generate a secure key: `openssl rand -hex 32`
- Store secrets in environment variables, never in code
- Use HTTPS in production
- Keep dependencies updated: `pip list --outdated`

## 🚀 Production Deployment

1. Set proper environment variables
2. Change `SECRET_KEY` to a secure random value
3. Set `DEBUG=False`
4. Use a production WSGI server (uvicorn with gunicorn)
5. Set up proper logging
6. Configure database connection pooling
7. Enable CORS only for trusted domains
8. Set up monitoring and alerting

## 🤔 When to Use This Template

**Perfect for:**
- ✅ New projects that need to get started quickly
- ✅ Developers learning FastAPI
- ✅ MVPs and prototypes
- ✅ Small to medium-sized APIs
- ✅ When you value simplicity and clarity

**Consider alternatives if:**
- ❌ You need microservices architecture
- ❌ You want GraphQL instead of REST
- ❌ You need complex DDD patterns

## 💡 Tips for Success

1. **Start simple** - Don't add complexity until you need it
2. **Read the comments** - Every file has helpful instructions
3. **Use the example** - The `example_entity` module shows best practices
4. **Test as you go** - Use the Swagger UI to test endpoints immediately
5. **Keep it clean** - Follow the established patterns

## 📄 License

This template is available under the MIT License. Use it freely for your projects!

---

**Ready to build your API?** Start with the [Quick Start](#-quick-start) section above!

**Questions?** Check the extensive inline comments in the code - they explain everything!
