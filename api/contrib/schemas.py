"""
Base Pydantic Schemas

This module provides base schema classes for request/response validation.
All entity schemas should inherit from these base classes.

Instructions:
1. Use BaseSchema for all your Pydantic models
2. Use OutMixin for response schemas that need id and created_at fields
3. Create Input, Output, and Update schemas for each entity

Schema naming conventions:
- EntityName: Base schema with all fields
- EntityNameIn: Input schema for creation (inherits from EntityName)
- EntityNameOut: Output schema with id and created_at (inherits from EntityName and OutMixin)
- EntityNameUpdate: Update schema with optional fields

Example:
    class User(BaseSchema):
        username: str
        email: str
    
    class UserIn(User):
        password: str
    
    class UserOut(User, OutMixin):
        pass
    
    class UserUpdate(BaseSchema):
        username: Optional[str] = None
        email: Optional[str] = None
"""

from typing import Annotated
from pydantic import UUID4, BaseModel as PydanticBaseModel, Field, ConfigDict
from datetime import datetime


class BaseSchema(PydanticBaseModel):
    """
    Base Pydantic schema for all entities
    
    Configuration:
    - extra='forbid': Reject any extra fields not defined in the schema
    - from_attributes=True: Allow creating schemas from ORM models (formerly orm_mode)
    
    All entity schemas should inherit from this class.
    
    Example:
        class Product(BaseSchema):
            name: str
            price: float
            description: Optional[str] = None
    """
    
    model_config = ConfigDict(
        extra='forbid',  # Reject extra fields
        from_attributes=True,  # Enable ORM mode (convert from SQLAlchemy models)
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,  # Validate on attribute assignment
    )


class OutMixin(BaseSchema):
    """
    Mixin for output schemas that includes common response fields
    
    Fields:
    - id: UUID identifier (automatically generated)
    - created_at: Timestamp of creation
    
    Use this mixin with your output schemas to include these fields.
    
    Example:
        class ProductOut(Product, OutMixin):
            pass
        
        # This will include: name, price, description, id, created_at
    """
    
    id: Annotated[UUID4, Field(description='Unique identifier')]
    created_at: Annotated[datetime, Field(description='Creation timestamp')]
    
    # Optional: Add more common output fields
    # updated_at: Annotated[Optional[datetime], Field(None, description='Last update timestamp')]


class PaginationParams(BaseSchema):
    """
    Schema for pagination parameters
    
    Use this for routes that support pagination.
    
    Example:
        @router.get('/')
        async def get_items(
            db: DatabaseDependency,
            pagination: PaginationParams = Depends()
        ):
            # Use pagination.page and pagination.size
            pass
    """
    
    page: Annotated[int, Field(default=1, ge=1, description='Page number')]
    size: Annotated[int, Field(default=50, ge=1, le=100, description='Items per page')]


class MessageResponse(BaseSchema):
    """
    Generic message response schema
    
    Use this for simple success/error messages.
    
    Example:
        return MessageResponse(message='Item created successfully')
    """
    
    message: Annotated[str, Field(description='Response message')]
