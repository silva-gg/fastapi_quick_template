"""
Example Entity Pydantic Schemas

This file defines the data validation and serialization schemas using Pydantic.

Instructions for creating your own schemas:
1. Import BaseSchema and OutMixin from api.contrib.schemas
2. Create a base schema with all fields
3. Create Input schema (for POST requests) - inherits from base
4. Create Output schema (for responses) - inherits from base + OutMixin
5. Create Update schema (for PATCH requests) - all fields optional
6. Use Annotated with Field for validation and documentation

Pydantic Field parameters:
- description: Field description for API docs
- example: Example value for API docs
- max_length: Maximum string length
- min_length: Minimum string length
- ge: Greater than or equal (for numbers)
- le: Less than or equal (for numbers)
- gt: Greater than (for numbers)
- lt: Less than (for numbers)
- pattern: Regex pattern for strings

Common types:
- str: String
- int: Integer
- float: Float
- bool: Boolean
- datetime: DateTime
- UUID4: UUID
- Optional[type]: Optional field (can be None)
- list[type]: List of items
"""

from typing import Annotated, Optional
from pydantic import Field, PositiveFloat, constr
from api.contrib.schemas import BaseSchema, OutMixin


class ExampleEntity(BaseSchema):
    """
    Base Example Entity Schema
    
    This schema defines all fields for the entity.
    It's used as a base for Input and Output schemas.
    
    Instructions:
    - Replace these fields with your actual entity fields
    - Use Annotated with Field for validation and documentation
    - Add validation rules as needed
    """
    
    name: Annotated[
        str,
        Field(
            description='Name of the entity',
            example='Example Item',
            max_length=100,
            min_length=1
        )
    ]
    
    description: Annotated[
        Optional[str],
        Field(
            None,
            description='Description of the entity',
            example='This is an example entity for demonstration purposes',
            max_length=500
        )
    ]
    
    value: Annotated[
        Optional[PositiveFloat],
        Field(
            None,
            description='Numeric value (must be positive)',
            example=99.99,
            ge=0.0
        )
    ]
    
    is_active: Annotated[
        bool,
        Field(
            default=True,
            description='Whether the entity is active',
            example=True
        )
    ]
    
    # Examples of other field types:
    
    # Email field:
    # from pydantic import EmailStr
    # email: Annotated[EmailStr, Field(description='Email address', example='user@example.com')]
    
    # URL field:
    # from pydantic import HttpUrl
    # website: Annotated[Optional[HttpUrl], Field(None, description='Website URL')]
    
    # Enum field:
    # from enum import Enum
    # class StatusEnum(str, Enum):
    #     ACTIVE = "active"
    #     INACTIVE = "inactive"
    # status: Annotated[StatusEnum, Field(description='Entity status')]
    
    # List field:
    # tags: Annotated[list[str], Field(default_factory=list, description='List of tags')]
    
    # Constrained string (regex pattern):
    # code: Annotated[constr(pattern=r'^[A-Z]{3}\d{3}$'), Field(description='Code format: ABC123')]
    
    # Date/DateTime fields:
    # from datetime import date, datetime
    # birth_date: Annotated[date, Field(description='Birth date')]
    # created_at: Annotated[datetime, Field(description='Creation timestamp')]


class ExampleEntityIn(ExampleEntity):
    """
    Input Schema for Creating Example Entity
    
    This schema is used for POST requests (creating new entities).
    It inherits all fields from the base schema.
    
    Instructions:
    - Add any fields that are required only on creation (e.g., password)
    - Remove any fields that shouldn't be settable by users (e.g., id, timestamps)
    - Keep fields that users should provide when creating
    """
    pass
    
    # Example: Add password field only for creation
    # password: Annotated[str, Field(description='User password', min_length=8)]


class ExampleEntityOut(ExampleEntity, OutMixin):
    """
    Output Schema for Example Entity
    
    This schema is used for API responses (GET, POST, PATCH).
    It includes all fields from the base schema plus id and created_at from OutMixin.
    
    Instructions:
    - This automatically includes: id (UUID) and created_at (datetime)
    - Add any computed fields or relationships
    - Don't include sensitive fields (e.g., passwords)
    """
    pass
    
    # Example: Add computed field
    # @property
    # def full_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"
    
    # Example: Add relationship
    # from api.categories.schemas import CategoryOut
    # category: Annotated[CategoryOut, Field(description='Related category')]


class ExampleEntityUpdate(BaseSchema):
    """
    Update Schema for Example Entity
    
    This schema is used for PATCH requests (updating existing entities).
    All fields are optional - users can update only the fields they want.
    
    Instructions:
    - Make all fields Optional
    - Include only fields that can be updated
    - Don't include id, created_at, or other immutable fields
    """
    
    name: Annotated[
        Optional[str],
        Field(
            None,
            description='Name of the entity',
            example='Updated Name',
            max_length=100,
            min_length=1
        )
    ]
    
    description: Annotated[
        Optional[str],
        Field(
            None,
            description='Description of the entity',
            max_length=500
        )
    ]
    
    value: Annotated[
        Optional[PositiveFloat],
        Field(
            None,
            description='Numeric value (must be positive)',
            ge=0.0
        )
    ]
    
    is_active: Annotated[
        Optional[bool],
        Field(
            None,
            description='Whether the entity is active'
        )
    ]


class ExampleEntityList(BaseSchema):
    """
    Simplified Schema for List Responses
    
    This schema is used when returning lists of entities.
    It includes only essential fields to reduce response size.
    
    Instructions:
    - Include only the most important fields
    - Use this for GET /entities (list endpoint)
    - Keep response size small for better performance
    """
    
    name: Annotated[str, Field(description='Entity name')]
    is_active: Annotated[bool, Field(description='Active status')]
    
    # Add id and created_at if needed
    # But typically you want to keep list responses lightweight
