"""
Base Database Models

This module provides the base model class that all entity models should inherit from.
It includes common fields like UUID and timestamps.

Instructions:
1. All your entity models should inherit from BaseModel
2. The id field (UUID) is automatically included
3. Add common fields here that should be in all entities (e.g., created_at, updated_at)

Example:
    from api.contrib.models import BaseModel
    
    class MyEntityModel(BaseModel):
        __tablename__ = 'my_entities'
        
        pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
        name: Mapped[str] = mapped_column(String(100), nullable=False)
"""

from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class BaseModel(DeclarativeBase):
    """
    Base model for all database entities
    
    Provides:
    - id: UUID field for unique identification
    - DeclarativeBase: SQLAlchemy ORM base class
    
    All entity models should inherit from this class.
    
    Example:
        class UserModel(BaseModel):
            __tablename__ = 'users'
            
            pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
            username: Mapped[str] = mapped_column(String(50), unique=True)
    """
    
    # UUID field - unique identifier for each record
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        default=uuid4,
        nullable=False,
        unique=True,
        index=True,
    )
    
    # Optional: Add common timestamp fields
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    # updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Optional: Add soft delete support
    # is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
