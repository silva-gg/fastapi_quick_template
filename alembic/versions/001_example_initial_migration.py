"""Initial migration - Create example_entity table

Revision ID: 001
Revises: 
Create Date: 2025-12-28

This is an example migration file showing how to create a table.
When you run 'alembic revision --autogenerate', Alembic will generate
files similar to this automatically based on your models.

Instructions:
- This file is for reference only
- Delete it and create your own migrations based on your models
- Run: alembic revision --autogenerate -m "Initial migration"
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '001_example'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Apply migration - Create example_entities table
    
    This function is called when you run: alembic upgrade head
    """
    # Create example_entities table
    op.create_table(
        'example_entities',
        sa.Column('pk_id', sa.Integer(), autoincrement=True, nullable=False, comment='Primary key'),
        sa.Column('id', UUID(as_uuid=True), nullable=False, comment='UUID identifier'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Entity name'),
        sa.Column('description', sa.Text(), nullable=True, comment='Entity description'),
        sa.Column('value', sa.Float(), nullable=True, comment='Numeric value'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='Active status'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='Creation timestamp'),
        sa.PrimaryKeyConstraint('pk_id'),
        sa.UniqueConstraint('id'),
        comment='Example entities table'
    )
    
    # Create indexes
    op.create_index(op.f('ix_example_entities_name'), 'example_entities', ['name'], unique=False)
    op.create_index(op.f('ix_example_entities_id'), 'example_entities', ['id'], unique=False)


def downgrade() -> None:
    """
    Rollback migration - Drop example_entities table
    
    This function is called when you run: alembic downgrade -1
    """
    # Drop indexes
    op.drop_index(op.f('ix_example_entities_id'), table_name='example_entities')
    op.drop_index(op.f('ix_example_entities_name'), table_name='example_entities')
    
    # Drop table
    op.drop_table('example_entities')
