"""
User Pydantic Schemas

Defines validation schemas for user-related operations.
"""

from typing import Annotated, Optional
from pydantic import Field, EmailStr, field_validator
from api.contrib.schemas import BaseSchema, OutMixin


class UserBase(BaseSchema):
    """Base user schema with common fields"""
    
    username: Annotated[
        str,
        Field(
            description='Username',
            example='johndoe',
            max_length=50,
            min_length=3
        )
    ]
    
    email: Annotated[
        EmailStr,
        Field(
            description='Email address',
            example='john@example.com'
        )
    ]
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username is alphanumeric"""
        if not v.replace('_', '').replace('-', '').replace('.', '').isalnum():
            raise ValueError('Username must be alphanumeric (can include _ and -)')
        return v.lower()


class UserCreate(UserBase):
    """Schema for user registration"""
    
    password: Annotated[
        str,
        Field(
            description='Password (min 8 characters)',
            example='SecurePass123!',
            min_length=8,
            max_length=100
        )
    ]
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseSchema):
    """Schema for user login"""
    
    username: Annotated[
        str,
        Field(
            description='Username or email',
            example='johndoe'
        )
    ]
    
    password: Annotated[
        str,
        Field(
            description='Password',
            example='SecurePass123!'
        )
    ]


class UserOut(UserBase, OutMixin):
    """Schema for user responses (excludes password)"""
    
    is_active: Annotated[bool, Field(description='Account active status')]
    is_superuser: Annotated[bool, Field(description='Admin privileges')]


class UserUpdate(BaseSchema):
    """Schema for updating user information"""
    
    email: Annotated[
        Optional[EmailStr],
        Field(
            None,
            description='Email address'
        )
    ]
    
    password: Annotated[
        Optional[str],
        Field(
            None,
            description='New password',
            min_length=8,
            max_length=100
        )
    ]
    
    is_active: Annotated[
        Optional[bool],
        Field(
            None,
            description='Account active status'
        )
    ]


class Token(BaseSchema):
    """Schema for JWT token response"""
    
    access_token: Annotated[str, Field(description='JWT access token')]
    token_type: Annotated[str, Field(default='bearer', description='Token type')]


class TokenData(BaseSchema):
    """Schema for decoded token data"""
    
    username: Annotated[Optional[str], Field(None, description='Username from token')]
