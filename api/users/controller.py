"""
User Authentication Controller

Provides endpoints for user registration, login, and management.
"""

from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, paginate

from api.contrib.dependencies import DatabaseDependency, CurrentUser, RequireAdmin
from api.configs.settings import settings
from .schemas import (
    UserCreate,
    UserLogin,
    UserOut,
    UserUpdate,
    Token
)
from .models import UserModel
from .auth import hash_password, verify_password, create_access_token


router = APIRouter()


@router.post(
    '/register',
    summary='Register a new user',
    description='Create a new user account with username, email, and password',
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut
)
async def register(
    db_session: DatabaseDependency,
    user_in: UserCreate = Body(
        ...,
        description='User registration data'
    )
):
    """
    Register a new user
    
    Args:
        db_session: Database session (injected)
        user_in: User registration data
        
    Returns:
        UserOut: Created user information (without password)
        
    Raises:
        HTTPException 409: If username or email already exists
        HTTPException 500: If database error occurs
        
    Example request:
        POST /auth/register
        {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
    """
    try:
        # Check if username already exists
        result = await db_session.execute(
            select(UserModel).filter_by(username=user_in.username)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Username already exists'
            )
        
        # Check if email already exists
        result = await db_session.execute(
            select(UserModel).filter_by(email=user_in.email)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email already registered'
            )
        
        # Create user with hashed password
        user_model = UserModel(
            id=uuid4(),
            username=user_in.username,
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            is_active=True,
            is_superuser=False,
            created_at=datetime.utcnow()
        )
        
        db_session.add(user_model)
        await db_session.commit()
        await db_session.refresh(user_model)
        
        return UserOut.model_validate(user_model)
        
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username or email already exists'
        )
    except HTTPException:
        raise
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred during registration: {str(e)}'
        )


@router.post(
    '/login',
    summary='User login',
    description='Authenticate user and return JWT access token',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
async def login(
    db_session: DatabaseDependency,
    credentials: UserLogin = Body(
        ...,
        description='Login credentials'
    )
):
    """
    Authenticate user and return JWT token
    
    Args:
        db_session: Database session (injected)
        credentials: Username/email and password
        
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException 401: If credentials are invalid
        
    Example request:
        POST /auth/login
        {
            "username": "johndoe",
            "password": "SecurePass123!"
        }
        
    Example response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIs...",
            "token_type": "bearer"
        }
    """
    # Find user by username or email
    result = await db_session.execute(
        select(UserModel).filter(
            (UserModel.username == credentials.username) |
            (UserModel.email == credentials.username)
        )
    )
    user = result.scalars().first()
    
    # Validate user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User account is inactive'
        )
    
    # Create access token
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type='bearer')


@router.get(
    '/me',
    summary='Get current user',
    description='Get information about the currently authenticated user',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def get_current_user_info(current_user: CurrentUser):
    """
    Get current authenticated user information
    
    Args:
        current_user: Current user (from JWT token)
        
    Returns:
        UserOut: Current user information
        
    Example:
        GET /auth/me
        Authorization: Bearer <your_jwt_token>
    """
    return UserOut.model_validate(current_user)


@router.patch(
    '/me',
    summary='Update current user',
    description='Update information for the currently authenticated user',
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
async def update_current_user(
    db_session: DatabaseDependency,
    current_user: CurrentUser,
    user_update: UserUpdate = Body(
        ...,
        description='Fields to update'
    )
):
    """
    Update current user information
    
    Args:
        db_session: Database session (injected)
        current_user: Current user (from JWT token)
        user_update: Fields to update
        
    Returns:
        UserOut: Updated user information
        
    Example request:
        PATCH /auth/me
        Authorization: Bearer <your_jwt_token>
        {
            "email": "newemail@example.com",
            "password": "NewSecurePass123!"
        }
    """
    try:
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Hash password if updating
        if 'password' in update_data:
            update_data['hashed_password'] = hash_password(update_data.pop('password'))
        
        # Update fields
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        await db_session.commit()
        await db_session.refresh(current_user)
        
        return UserOut.model_validate(current_user)
        
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already in use'
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred while updating user: {str(e)}'
        )


@router.get(
    '/users',
    summary='List all users (Admin only)',
    description='Get a paginated list of all users - requires admin privileges',
    status_code=status.HTTP_200_OK,
    response_model=Page[UserOut]
)
async def list_users(
    db_session: DatabaseDependency,
    admin: RequireAdmin,
    username: Optional[str] = Query(None, description='Filter by username'),
    email: Optional[str] = Query(None, description='Filter by email'),
    is_active: Optional[bool] = Query(None, description='Filter by active status')
):
    """
    List all users (Admin only)
    
    Args:
        db_session: Database session (injected)
        admin: Current admin user (validated)
        username: Optional username filter
        email: Optional email filter
        is_active: Optional active status filter
        
    Returns:
        Page[UserOut]: Paginated list of users
        
    Example:
        GET /auth/users?is_active=true&page=1&size=10
        Authorization: Bearer <admin_jwt_token>
    """
    query = select(UserModel)
    
    if username:
        query = query.filter(UserModel.username.ilike(f'%{username}%'))
    
    if email:
        query = query.filter(UserModel.email.ilike(f'%{email}%'))
    
    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)
    
    query = query.order_by(UserModel.created_at.desc())
    
    result = await db_session.execute(query)
    users = result.scalars().all()
    
    return paginate([UserOut.model_validate(user) for user in users])


@router.delete(
    '/users/{user_id}',
    summary='Delete user (Admin only)',
    description='Delete a user account - requires admin privileges',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: UUID4,
    db_session: DatabaseDependency,
    admin: RequireAdmin
):
    """
    Delete a user (Admin only)
    
    Args:
        user_id: UUID of user to delete
        db_session: Database session (injected)
        admin: Current admin user (validated)
        
    Raises:
        HTTPException 404: If user not found
        HTTPException 403: If trying to delete yourself
        
    Example:
        DELETE /auth/users/550e8400-e29b-41d4-a716-446655440000
        Authorization: Bearer <admin_jwt_token>
    """
    # Prevent admin from deleting themselves
    if user_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot delete your own account'
        )
    
    result = await db_session.execute(
        select(UserModel).filter_by(id=user_id)
    )
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    await db_session.delete(user)
    await db_session.commit()
