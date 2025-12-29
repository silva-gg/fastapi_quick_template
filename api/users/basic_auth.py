"""
Basic Authentication Module

Provides HTTP Basic Authentication as a simpler alternative to JWT tokens.
Useful for scripts, API clients, and internal tools.
"""

from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.configs.database import get_session
from api.users.models import UserModel
from api.users.auth import verify_password


# HTTP Basic security scheme
basic_security = HTTPBasic()


async def get_current_user_basic(
    credentials: HTTPBasicCredentials = Depends(basic_security),
    db_session: AsyncSession = Depends(get_session)
) -> UserModel:
    """
    Authenticate user using HTTP Basic Authentication
    
    Args:
        credentials: HTTP Basic credentials (username:password)
        db_session: Database session
        
    Returns:
        UserModel: Authenticated user
        
    Raises:
        HTTPException: If credentials are invalid
        
    Usage:
        @router.get('/protected')
        async def protected_route(current_user: CurrentUserBasic):
            return {"user": current_user.username}
    
    Example request:
        curl -u username:password http://localhost:8000/api/endpoint
    """
    # Find user by username or email
    result = await db_session.execute(
        select(UserModel).filter(
            (UserModel.username == credentials.username) |
            (UserModel.email == credentials.username)
        )
    )
    user = result.scalars().first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'}
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Inactive user account'
        )
    
    return user


async def require_admin_basic(
    current_user: UserModel = Depends(get_current_user_basic)
) -> UserModel:
    """
    Require admin privileges with Basic Auth
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserModel: Current user (if admin)
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin privileges required'
        )
    return current_user
