# API Development Guide

This guide provides detailed information for developing APIs with this template.

## Table of Contents

- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Pydantic Schemas](#pydantic-schemas)
- [Controllers (Endpoints)](#controllers-endpoints)
- [Database Migrations](#database-migrations)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Project Structure

```
api/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI app entry point
├── routers.py               # Router registration
│
├── configs/                 # Configuration files
│   ├── database.py          # Database connection
│   └── settings.py          # App settings (env vars)
│
├── contrib/                 # Shared modules
│   ├── models.py            # Base database model
│   ├── schemas.py           # Base Pydantic schemas
│   └── dependencies.py      # Shared dependencies
│
└── <entity_name>/           # Entity module (one per resource)
    ├── __init__.py
    ├── models.py            # SQLAlchemy models
    ├── schemas.py           # Pydantic schemas
    └── controller.py        # API endpoints
```

## Database Models

Models define your database schema using SQLAlchemy ORM.

### Basic Model Structure

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from api.contrib.models import BaseModel

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
```

### Field Types

| Python Type | SQLAlchemy Type | Description |
|------------|-----------------|-------------|
| `int` | `Integer` | Integer numbers |
| `str` | `String(length)` | Text with max length |
| `float` | `Float` | Decimal numbers |
| `bool` | `Boolean` | True/False |
| `datetime` | `DateTime` | Date and time |
| `UUID` | `UUID` | Unique identifier |
| `str` | `Text` | Unlimited text |

### Constraints

```python
# Unique constraint
username: Mapped[str] = mapped_column(String(50), unique=True)

# Not nullable
email: Mapped[str] = mapped_column(String(100), nullable=False)

# Default value
is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# Index for faster queries
name: Mapped[str] = mapped_column(String(100), index=True)
```

### Relationships

**One-to-Many** (Parent has many children):

```python
# Parent Model (Category)
class CategoryModel(BaseModel):
    __tablename__ = 'categories'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['ProductModel']] = relationship(back_populates='category')

# Child Model (Product)
class ProductModel(BaseModel):
    __tablename__ = 'products'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.pk_id'))
    category: Mapped['CategoryModel'] = relationship(back_populates='products')
```

**Many-to-Many** (Students and Courses):

```python
# Association table
student_course = Table(
    'student_course',
    BaseModel.metadata,
    Column('student_id', ForeignKey('students.pk_id')),
    Column('course_id', ForeignKey('courses.pk_id'))
)

# Student Model
class StudentModel(BaseModel):
    __tablename__ = 'students'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    courses: Mapped[list['CourseModel']] = relationship(
        secondary=student_course,
        back_populates='students'
    )

# Course Model
class CourseModel(BaseModel):
    __tablename__ = 'courses'
    
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    students: Mapped[list['StudentModel']] = relationship(
        secondary=student_course,
        back_populates='courses'
    )
```

## Pydantic Schemas

Schemas validate request/response data.

### Schema Types

1. **Base Schema**: Contains all fields
2. **Input Schema** (`EntityIn`): For POST requests
3. **Output Schema** (`EntityOut`): For responses (includes id, created_at)
4. **Update Schema** (`EntityUpdate`): For PATCH requests (all optional)

### Example

```python
from typing import Annotated, Optional
from pydantic import Field, EmailStr
from api.contrib.schemas import BaseSchema, OutMixin

# Base schema
class User(BaseSchema):
    username: Annotated[str, Field(max_length=50, min_length=3)]
    email: Annotated[EmailStr, Field()]
    age: Annotated[int, Field(ge=18, le=120)]

# Input schema (for creation)
class UserIn(User):
    password: Annotated[str, Field(min_length=8)]

# Output schema (for responses)
class UserOut(User, OutMixin):
    # Automatically includes: id, created_at
    pass

# Update schema (all optional)
class UserUpdate(BaseSchema):
    username: Annotated[Optional[str], Field(None, max_length=50)]
    email: Annotated[Optional[EmailStr], Field(None)]
    age: Annotated[Optional[int], Field(None, ge=18, le=120)]
```

### Validation Rules

```python
from pydantic import Field, validator, EmailStr, HttpUrl

# String length
name: Annotated[str, Field(max_length=100, min_length=1)]

# Number range
age: Annotated[int, Field(ge=0, le=150)]  # 0 <= age <= 150
price: Annotated[float, Field(gt=0)]      # price > 0

# Email validation
email: Annotated[EmailStr, Field()]

# URL validation
website: Annotated[HttpUrl, Field()]

# Regex pattern
phone: Annotated[str, Field(pattern=r'^\+?1?\d{9,15}$')]

# Custom validator
@validator('username')
def validate_username(cls, v):
    if not v.isalnum():
        raise ValueError('Username must be alphanumeric')
    return v.lower()
```

## Controllers (Endpoints)

Controllers define API endpoints.

### CRUD Operations

#### Create (POST)

```python
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=EntityOut)
async def create(
    db_session: DatabaseDependency,
    entity_in: EntityIn = Body(...)
):
    entity_out = EntityOut(
        id=uuid4(),
        created_at=datetime.utcnow(),
        **entity_in.model_dump()
    )
    entity_model = EntityModel(**entity_out.model_dump())
    db_session.add(entity_model)
    await db_session.commit()
    return entity_out
```

#### Read (GET)

```python
# Get all
@router.get('/', response_model=Page[EntityOut])
async def get_all(db_session: DatabaseDependency):
    result = await db_session.execute(select(EntityModel))
    entities = result.scalars().all()
    return paginate([EntityOut.model_validate(e) for e in entities])

# Get by ID
@router.get('/{id}', response_model=EntityOut)
async def get_by_id(id: UUID4, db_session: DatabaseDependency):
    result = await db_session.execute(
        select(EntityModel).filter_by(id=id)
    )
    entity = result.scalars().first()
    if not entity:
        raise HTTPException(status_code=404, detail='Not found')
    return EntityOut.model_validate(entity)
```

#### Update (PATCH)

```python
@router.patch('/{id}', response_model=EntityOut)
async def update(
    id: UUID4,
    db_session: DatabaseDependency,
    entity_update: EntityUpdate = Body(...)
):
    result = await db_session.execute(
        select(EntityModel).filter_by(id=id)
    )
    entity = result.scalars().first()
    if not entity:
        raise HTTPException(status_code=404, detail='Not found')
    
    update_data = entity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entity, field, value)
    
    await db_session.commit()
    await db_session.refresh(entity)
    return EntityOut.model_validate(entity)
```

#### Delete (DELETE)

```python
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: UUID4, db_session: DatabaseDependency):
    result = await db_session.execute(
        select(EntityModel).filter_by(id=id)
    )
    entity = result.scalars().first()
    if not entity:
        raise HTTPException(status_code=404, detail='Not found')
    
    await db_session.delete(entity)
    await db_session.commit()
```

### Filtering and Pagination

```python
@router.get('/', response_model=Page[EntityOut])
async def get_all(
    db_session: DatabaseDependency,
    name: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
):
    query = select(EntityModel)
    
    if name:
        query = query.filter(EntityModel.name.ilike(f'%{name}%'))
    
    if is_active is not None:
        query = query.filter(EntityModel.is_active == is_active)
    
    query = query.order_by(EntityModel.created_at.desc())
    
    result = await db_session.execute(query)
    entities = result.scalars().all()
    return paginate([EntityOut.model_validate(e) for e in entities])
```

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user table"

# Create empty migration for manual changes
alembic revision -m "Custom migration"
```

### Applying Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

### Migration Best Practices

1. **Review auto-generated migrations** - Always check before applying
2. **Test in development first** - Never run untested migrations in production
3. **One change per migration** - Keep migrations focused
4. **Add data migrations separately** - Don't mix schema and data changes
5. **Never modify applied migrations** - Create new ones instead

## Error Handling

### HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate resource |
| 500 | Server Error | Unexpected error |

### Exception Handling

```python
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

try:
    # Database operation
    db_session.add(entity)
    await db_session.commit()
except IntegrityError as e:
    await db_session.rollback()
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Resource already exists'
    )
except Exception as e:
    await db_session.rollback()
    # Log the error
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='An error occurred'
    )
```

## Best Practices

### 1. Always Use Async Operations

```python
# ✅ Good
result = await db_session.execute(query)
await db_session.commit()

# ❌ Bad
result = db_session.execute(query)  # Blocking
```

### 2. Use Type Hints

```python
# ✅ Good
def get_user(user_id: UUID4) -> UserOut:
    ...

# ❌ Bad
def get_user(user_id):
    ...
```

### 3. Validate Input

```python
# ✅ Good - Use Pydantic schemas
@router.post('/', response_model=UserOut)
async def create_user(user_in: UserIn = Body(...)):
    ...

# ❌ Bad - Accept raw dicts
@router.post('/')
async def create_user(data: dict):
    ...
```

### 4. Handle Errors Gracefully

```python
# ✅ Good
if not entity:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Entity not found'
    )

# ❌ Bad
# Let it fail silently or return None
```

### 5. Use Pagination for Lists

```python
# ✅ Good
@router.get('/', response_model=Page[EntityOut])
async def get_all(...):
    return paginate(entities)

# ❌ Bad - Return all records
@router.get('/', response_model=list[EntityOut])
async def get_all(...):
    return entities  # Could be thousands!
```

### 6. Document Your Endpoints

```python
# ✅ Good
@router.post(
    '/',
    summary='Create new user',
    description='Creates a new user with the provided data',
    response_model=UserOut
)

# ❌ Bad - No documentation
@router.post('/')
```

### 7. Use Environment Variables

```python
# ✅ Good
from api.configs.settings import settings
db_url = settings.DB_URL

# ❌ Bad - Hardcoded values
db_url = "postgresql://user:pass@localhost/db"
```

### 8. Keep Controllers Thin

```python
# ✅ Good - Logic in service layer
@router.post('/')
async def create_user(user_in: UserIn, db: DatabaseDependency):
    return await user_service.create(db, user_in)

# ❌ Bad - All logic in controller
@router.post('/')
async def create_user(user_in: UserIn, db: DatabaseDependency):
    # 50 lines of business logic...
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
