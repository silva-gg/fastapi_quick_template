"""
Main FastAPI Application Entry Point

This file initializes the FastAPI application and includes all routers.
Customize the title, description, and version according to your project.
"""

from fastapi import FastAPI
from api.routers import api_router
from fastapi_pagination import add_pagination

# Create FastAPI application instance
# Customize these parameters for your project
app = FastAPI(
    title='FastAPI Template',
    description='A modern, asynchronous REST API template built with FastAPI',
    version='0.1.0',
    docs_url='/docs',  # Swagger UI
    redoc_url='/redoc',  # ReDoc
)

# Include all API routers
app.include_router(api_router)

# Add pagination support
add_pagination(app)


@app.get('/', tags=['Health'])
async def root():
    """
    Root endpoint - Health check
    
    Returns:
        dict: API status and version
    """
    return {
        'message': 'FastAPI Template is running!',
        'version': '0.1.0',
        'docs': '/docs'
    }


@app.get('/health', tags=['Health'])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        dict: Health status
    """
    return {'status': 'healthy'}


# Optional: Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    Add any initialization code here (e.g., database connections, cache warmup)
    """
    print("🚀 FastAPI Template started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    Add cleanup code here (e.g., close database connections, save state)
    """
    print("👋 FastAPI Template shutting down...")
