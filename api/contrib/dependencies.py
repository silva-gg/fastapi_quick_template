"""
Shared Dependencies

This module provides FastAPI dependencies used across the application.
Dependencies are reusable components that can be injected into route handlers.

Instructions:
1. Use DatabaseDependency in your routes to get a database session
2. Use CurrentUser to get the authenticated user
3. Use RequireAdmin to ensure user has admin privileges
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.configs.database import get_session
from api.users.models import UserModel
from api.users.auth import decode_access_token


# Type alias for database session dependency
DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]

# HTTP Bearer token security
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: AsyncSession = Depends(get_session)
) -> UserModel:
    """
    Validate JWT token and return current user
    
    Args:
        credentials: HTTP authorization credentials
        db_session: Database session
        
    Returns:
        UserModel: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
        
    Usage:
        @router.get('/protected')
        async def protected_route(current_user: CurrentUser):
            return {"user": current_user.username}
    """
    token = credentials.credentials
    
    # Decode token
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    # Get user from database
    result = await db_session.execute(
        select(UserModel).filter_by(username=username)
    )
    user = result.scalars().first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user account'
        )
    
    return user


# Type alias for current user dependency
CurrentUser = Annotated[UserModel, Depends(get_current_user)]


async def require_admin(current_user: CurrentUser) -> UserModel:
    """
    Ensure current user has admin permissions
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserModel: Current user (if admin)
        
    Raises:
        HTTPException: If user is not an admin
        
    Usage:
        @router.delete('/admin/users/{id}')
        async def delete_user(admin: RequireAdmin, user_id: UUID4):
            # Only admins can access this endpoint
            pass
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin privileges required'
        )
    return current_user


# Type alias for admin user dependency
RequireAdmin = Annotated[UserModel, Depends(require_admin)]
