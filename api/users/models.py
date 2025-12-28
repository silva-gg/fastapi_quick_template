"""
User Database Models

This file defines the database schema for users and authentication.
"""

from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from api.contrib.models import BaseModel


class UserModel(BaseModel):
    """
    User Model for Authentication
    
    Stores user credentials and authentication information.
    
    Attributes:
        pk_id: Primary key
        username: Unique username
        email: User email address
        hashed_password: Bcrypt hashed password
        is_active: Whether user account is active
        is_superuser: Whether user has admin privileges
        created_at: Account creation timestamp
    """
    
    __tablename__ = 'users'
    
    pk_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='Primary key'
    )
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='Unique username'
    )
    
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment='User email address'
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment='Hashed password'
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment='Account active status'
    )
    
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment='Admin privileges'
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Account creation timestamp'
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.pk_id}, username='{self.username}', email='{self.email}')>"
