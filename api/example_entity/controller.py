"""
Example Entity API Controller

This file defines the API endpoints (routes) for the example entity.
It implements CRUD operations: Create, Read, Update, Delete.

Instructions for creating your own controller:
1. Import necessary modules and your schemas/models
2. Create a router instance
3. Implement endpoints following REST conventions:
   - POST /   : Create new entity
   - GET /    : List all entities (with pagination)
   - GET /{id}: Get single entity by ID
   - PATCH /{id}: Update entity
   - DELETE /{id}: Delete entity
4. Use proper HTTP status codes
5. Handle exceptions appropriately
6. Add query parameters for filtering
7. Document endpoints with summary and description

HTTP Status Codes:
- 200 OK: Successful GET request
- 201 Created: Successful POST request
- 204 No Content: Successful DELETE request
- 400 Bad Request: Invalid input
- 404 Not Found: Resource not found
- 409 Conflict: Duplicate resource
- 500 Internal Server Error: Server error

Error Handling:
- Use HTTPException for expected errors
- Catch IntegrityError for database constraint violations
- Log unexpected errors
"""

from datetime import datetime
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from api.contrib.dependencies import DatabaseDependency
from .schemas import (
    ExampleEntityIn,
    ExampleEntityOut,
    ExampleEntityUpdate,
    ExampleEntityList
)
from .models import ExampleEntityModel


# Create router instance
# This will be registered in api/routers.py
router = APIRouter()


@router.post(
    '/',
    summary='Create a new example entity',
    description='Creates a new example entity with the provided data',
    status_code=status.HTTP_201_CREATED,
    response_model=ExampleEntityOut
)
async def create_entity(
    db_session: DatabaseDependency,
    entity_in: ExampleEntityIn = Body(
        ...,
        description='Entity data to create'
    )
):
    """
    Create a new example entity
    
    Args:
        db_session: Database session (injected)
        entity_in: Input data for the new entity
        
    Returns:
        ExampleEntityOut: Created entity with id and created_at
        
    Raises:
        HTTPException 409: If entity already exists (duplicate)
        HTTPException 500: If database error occurs
        
    Example request body:
        {
            "name": "Example Item",
            "description": "This is a test",
            "value": 99.99,
            "is_active": true
        }
    """
    try:
        # Create output schema with UUID and timestamp
        entity_out = ExampleEntityOut(
            id=uuid4(),
            created_at=datetime.utcnow(),
            **entity_in.model_dump()
        )
        
        # Create database model from output schema
        entity_model = ExampleEntityModel(**entity_out.model_dump())
        
        # Add to database session
        db_session.add(entity_model)
        
        # Commit transaction
        await db_session.commit()
        
        # Refresh to get any database-generated values
        # await db_session.refresh(entity_model)
        
        return entity_out
        
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Entity already exists or constraint violation: {str(e)}'
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while creating the entity: {str(e)}'
        )


@router.get(
    '/',
    summary='List all example entities',
    description='Retrieves a paginated list of all example entities with optional filtering',
    status_code=status.HTTP_200_OK,
    response_model=Page[ExampleEntityOut],
)
async def get_all_entities(
    db_session: DatabaseDependency,
    name: Optional[str] = Query(
        None,
        description='Filter by name (case-insensitive partial match)',
        example='example'
    ),
    is_active: Optional[bool] = Query(
        None,
        description='Filter by active status'
    ),
) -> Page[ExampleEntityOut]:
    """
    Get all example entities with optional filters
    
    Args:
        db_session: Database session (injected)
        name: Optional name filter (partial match)
        is_active: Optional active status filter
        
    Returns:
        Page[ExampleEntityOut]: Paginated list of entities
        
    Example:
        GET /examples?name=test&is_active=true&page=1&size=10
    """
    # Start with base query
    query = select(ExampleEntityModel)
    
    # Apply filters if provided
    if name:
        query = query.filter(ExampleEntityModel.name.ilike(f'%{name}%'))
    
    if is_active is not None:
        query = query.filter(ExampleEntityModel.is_active == is_active)
    
    # Add ordering
    query = query.order_by(ExampleEntityModel.created_at.desc())
    
    # Execute query
    result = await db_session.execute(query)
    entities = result.scalars().all()
    
    # Convert to output schemas and paginate
    return paginate([
        ExampleEntityOut.model_validate(entity)
        for entity in entities
    ])


@router.get(
    '/{entity_id}',
    summary='Get example entity by ID',
    description='Retrieves a single example entity by its UUID',
    status_code=status.HTTP_200_OK,
    response_model=ExampleEntityOut
)
async def get_entity_by_id(
    entity_id: UUID4,
    db_session: DatabaseDependency
):
    """
    Get a single example entity by ID
    
    Args:
        entity_id: UUID of the entity
        db_session: Database session (injected)
        
    Returns:
        ExampleEntityOut: Entity data
        
    Raises:
        HTTPException 404: If entity not found
        
    Example:
        GET /examples/550e8400-e29b-41d4-a716-446655440000
    """
    # Query for entity by UUID
    result = await db_session.execute(
        select(ExampleEntityModel).filter_by(id=entity_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {entity_id} not found'
        )
    
    return ExampleEntityOut.model_validate(entity)


@router.patch(
    '/{entity_id}',
    summary='Update example entity',
    description='Updates an existing example entity with partial data',
    status_code=status.HTTP_200_OK,
    response_model=ExampleEntityOut
)
async def update_entity(
    entity_id: UUID4,
    db_session: DatabaseDependency,
    entity_update: ExampleEntityUpdate = Body(
        ...,
        description='Fields to update (all optional)'
    )
):
    """
    Update an existing example entity
    
    Args:
        entity_id: UUID of the entity to update
        db_session: Database session (injected)
        entity_update: Fields to update
        
    Returns:
        ExampleEntityOut: Updated entity data
        
    Raises:
        HTTPException 404: If entity not found
        HTTPException 500: If database error occurs
        
    Example request body:
        {
            "name": "Updated Name",
            "is_active": false
        }
    """
    # Get existing entity
    result = await db_session.execute(
        select(ExampleEntityModel).filter_by(id=entity_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {entity_id} not found'
        )
    
    try:
        # Update only provided fields
        update_data = entity_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(entity, field, value)
        
        # Commit changes
        await db_session.commit()
        await db_session.refresh(entity)
        
        return ExampleEntityOut.model_validate(entity)
        
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Update violates constraint: {str(e)}'
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while updating the entity: {str(e)}'
        )


@router.delete(
    '/{entity_id}',
    summary='Delete example entity',
    description='Deletes an example entity by its UUID',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_entity(
    entity_id: UUID4,
    db_session: DatabaseDependency
):
    """
    Delete an example entity
    
    Args:
        entity_id: UUID of the entity to delete
        db_session: Database session (injected)
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: If entity not found
        HTTPException 500: If database error occurs
        
    Example:
        DELETE /examples/550e8400-e29b-41d4-a716-446655440000
    """
    # Get existing entity
    result = await db_session.execute(
        select(ExampleEntityModel).filter_by(id=entity_id)
    )
    entity = result.scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Entity with id {entity_id} not found'
        )
    
    try:
        # Delete entity
        await db_session.delete(entity)
        await db_session.commit()
        
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while deleting the entity: {str(e)}'
        )


# Additional endpoint examples:

# Count entities
# @router.get('/count', response_model=dict)
# async def count_entities(db_session: DatabaseDependency):
#     """Get total count of entities"""
#     from sqlalchemy import func
#     result = await db_session.execute(
#         select(func.count()).select_from(ExampleEntityModel)
#     )
#     count = result.scalar()
#     return {'count': count}


# Bulk create
# @router.post('/bulk', response_model=list[ExampleEntityOut])
# async def bulk_create(
#     db_session: DatabaseDependency,
#     entities: list[ExampleEntityIn] = Body(...)
# ):
#     """Create multiple entities at once"""
#     created_entities = []
#     for entity_in in entities:
#         entity_out = ExampleEntityOut(
#             id=uuid4(),
#             created_at=datetime.utcnow(),
#             **entity_in.model_dump()
#         )
#         entity_model = ExampleEntityModel(**entity_out.model_dump())
#         db_session.add(entity_model)
#         created_entities.append(entity_out)
#     
#     await db_session.commit()
#     return created_entities


# Search endpoint
# @router.get('/search', response_model=Page[ExampleEntityOut])
# async def search_entities(
#     db_session: DatabaseDependency,
#     q: str = Query(..., description='Search query')
# ):
#     """Full-text search across multiple fields"""
#     query = select(ExampleEntityModel).filter(
#         or_(
#             ExampleEntityModel.name.ilike(f'%{q}%'),
#             ExampleEntityModel.description.ilike(f'%{q}%')
#         )
#     )
#     result = await db_session.execute(query)
#     entities = result.scalars().all()
#     return paginate([ExampleEntityOut.model_validate(e) for e in entities])
