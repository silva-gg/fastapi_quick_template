"""
API Router Configuration

This file aggregates all entity routers and registers them with the main API router.
Add your new entity routers here following the pattern shown in the example.

Instructions:
1. Import your entity controller's router
2. Include it in the api_router with appropriate prefix and tags
3. The prefix should be plural (e.g., '/users', '/products')
4. Tags are used for grouping in the API documentation
"""

from fastapi import APIRouter
from api.users.controller import router as users_router
from api.example_entity.controller import router as example_entity_router

# Create main API router
api_router = APIRouter()

# Register authentication/user router
api_router.include_router(
    users_router,
    prefix='/auth',
    tags=['authentication']
)

# Register entity routers
# Pattern: api_router.include_router(your_router, prefix='/your-entities', tags=['your-entities'])

api_router.include_router(
    example_entity_router, 
    prefix='/examples', 
    tags=['examples']
)

# Add more routers here as you create new entities:
# 
# from api.products.controller import router as products_router
# api_router.include_router(products_router, prefix='/products', tags=['products'])
