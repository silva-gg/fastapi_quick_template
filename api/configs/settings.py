"""
Application Settings

This module handles application configuration using Pydantic Settings.
Environment variables are automatically loaded from .env file.

Instructions:
1. Create a .env file in the root directory
2. Add your configuration variables (see .env.example)
3. Access settings using: from api.configs.settings import settings

Example .env file:
    DB_URL=postgresql+asyncpg://user:password@localhost/dbname
    APP_NAME=My API
    DEBUG=True
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    Attributes:
        DB_URL: Database connection URL (PostgreSQL with asyncpg driver)
        APP_NAME: Application name
        DEBUG: Debug mode flag
    """
    
    # Database Configuration
    DB_URL: str = Field(
        default='postgresql+asyncpg://api_user:api_password@localhost/api_database',
        description='Database connection URL'
    )
    
    # Application Configuration
    APP_NAME: str = Field(
        default='FastAPI Template',
        description='Application name'
    )
    
    DEBUG: bool = Field(
        default=False,
        description='Debug mode'
    )
    
    # JWT Authentication Configuration
    SECRET_KEY: str = Field(
        default='your-secret-key-change-this-in-production-use-openssl-rand-hex-32',
        description='Secret key for JWT token generation (CHANGE IN PRODUCTION!)'
    )
    
    ALGORITHM: str = Field(
        default='HS256',
        description='JWT algorithm'
    )
    
    ACCESS_TOKEN_EXPIRE_DAYS: int = Field(
        default=30,
        description='JWT token expiration in days'
    )
    
    # Add more configuration fields as needed:
    # API_KEY: str = Field(default='', description='API Key')
    # CORS_ORIGINS: list[str] = Field(default=['*'], description='CORS allowed origins')
    
    class Config:
        """Pydantic configuration"""
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


# Create settings instance
# This will automatically load values from environment variables
settings = Settings()
