"""
Database Configuration

This module sets up the async database connection using SQLAlchemy.
It provides a session generator for dependency injection in FastAPI routes.

Instructions:
1. The database URL is loaded from settings (environment variables)
2. Use get_session() as a dependency in your route handlers
3. Configure engine parameters based on your needs (pool size, echo, etc.)

Example usage in a route:
    from api.contrib.dependencies import DatabaseDependency
    
    @router.get('/')
    async def my_route(db_session: DatabaseDependency):
        result = await db_session.execute(select(MyModel))
        return result.scalars().all()
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from api.configs.settings import settings


# Create async database engine
# echo=False: Disable SQL query logging (set to True for debugging)
# pool_size: Number of connections to maintain in the pool
# max_overflow: Maximum number of connections that can be created beyond pool_size
engine = create_async_engine(
    settings.DB_URL,
    echo=False,  # Set to True to log all SQL queries
    # pool_pre_ping=True,  # Verify connections before using them
    # pool_size=5,  # Number of connections in the pool
    # max_overflow=10,  # Additional connections beyond pool_size
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator that provides database sessions
    
    This function is used as a FastAPI dependency to inject database sessions
    into route handlers. The session is automatically closed after the request.
    
    Yields:
        AsyncSession: SQLAlchemy async session
        
    Example:
        @router.get('/items')
        async def get_items(db: AsyncSession = Depends(get_session)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with async_session() as session:
        yield session
