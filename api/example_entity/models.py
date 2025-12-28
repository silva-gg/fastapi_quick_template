"""
Example Entity Database Models

This file defines the database schema for the example entity using SQLAlchemy ORM.

Instructions for creating your own models:
1. Import the BaseModel from api.contrib.models
2. Define your model class inheriting from BaseModel
3. Set the __tablename__ attribute (use plural, snake_case)
4. Define columns using Mapped and mapped_column
5. Add relationships if needed with foreign keys

Column types commonly used:
- Integer: For integer numbers
- String(length): For text with max length
- Float: For decimal numbers
- Boolean: For true/false values
- DateTime: For timestamps
- ForeignKey: For relationships

Example relationships:
- One-to-Many: Use relationship() with back_populates
- Many-to-One: Use ForeignKey and relationship()
- Many-to-Many: Create an association table

After creating/modifying models:
1. Run: alembic revision --autogenerate -m "Description of changes"
2. Run: alembic upgrade head
"""

from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from api.contrib.models import BaseModel


class ExampleEntityModel(BaseModel):
    """
    Example Entity Database Model
    
    This is a template showing different field types and configurations.
    Replace this with your actual entity model.
    
    Attributes:
        pk_id: Primary key (auto-increment integer)
        name: Entity name (required, max 100 chars)
        description: Entity description (optional, text field)
        value: Numeric value (optional, float)
        is_active: Active status flag (default True)
        created_at: Creation timestamp (auto-set)
        
    Table name: example_entities
    """
    
    __tablename__ = 'example_entities'
    
    # Primary Key - Auto-incrementing integer
    pk_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='Primary key'
    )
    
    # Required string field with max length
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,  # Add index for faster queries
        comment='Entity name'
    )
    
    # Optional text field (no length limit)
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment='Entity description'
    )
    
    # Optional numeric field
    value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment='Numeric value'
    )
    
    # Boolean field with default value
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment='Active status'
    )
    
    # Timestamp field
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Creation timestamp'
    )
    
    # Examples of other field types:
    
    # Unique field:
    # code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Field with check constraint:
    # age: Mapped[int] = mapped_column(Integer, CheckConstraint('age >= 0'), nullable=False)
    
    # Enum field:
    # from enum import Enum
    # class Status(str, Enum):
    #     ACTIVE = "active"
    #     INACTIVE = "inactive"
    # status: Mapped[str] = mapped_column(String(20), default=Status.ACTIVE, nullable=False)
    
    # Foreign Key example (Many-to-One):
    # category_id: Mapped[int] = mapped_column(ForeignKey("categories.pk_id"), nullable=False)
    # category: Mapped['CategoryModel'] = relationship(back_populates="examples", lazy='selectin')
    
    # One-to-Many relationship example (in parent model):
    # examples: Mapped[list['ExampleEntityModel']] = relationship(back_populates="category", lazy='selectin')
    
    def __repr__(self) -> str:
        """String representation of the model"""
        return f"<ExampleEntity(id={self.pk_id}, name='{self.name}')>"
