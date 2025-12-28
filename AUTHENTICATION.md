# Authentication Guide

This guide explains how to use the built-in authentication system.

## Overview

The template includes a complete JWT-based authentication system with:
- User registration with password validation
- Secure login with bcrypt password hashing
- JWT token generation and validation
- Protected routes using dependencies
- Admin-only routes
- User profile management

## Quick Start

### 1. Register a User

**Endpoint:** `POST /auth/register`

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-12-28T10:00:00"
}
```

### 2. Login

**Endpoint:** `POST /auth/login`

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Note:** You can use either username or email in the `username` field.

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Expiration:** 30 days (configurable in settings)

### 3. Use the Token

Include the token in the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Using curl:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Using Swagger UI:**
1. Click the "Authorize" button (🔒 icon)
2. Enter: `Bearer YOUR_TOKEN_HERE`
3. Click "Authorize"
4. Now all protected endpoints will use your token

## Protected Routes

### Require Authentication

Any route that needs authentication uses the `CurrentUser` dependency:

```python
from api.contrib.dependencies import CurrentUser

@router.get('/profile')
async def get_profile(current_user: CurrentUser):
    return {"user": current_user.username}
```

### Require Admin

For admin-only routes, use the `RequireAdmin` dependency:

```python
from api.contrib.dependencies import RequireAdmin

@router.delete('/admin/delete-all')
async def dangerous_operation(admin: RequireAdmin):
    # Only superusers can access this
    return {"message": "Done"}
```

## User Management Endpoints

### Get Current User

**Endpoint:** `GET /auth/me`  
**Authentication:** Required

Returns information about the currently logged-in user.

### Update Current User

**Endpoint:** `PATCH /auth/me`  
**Authentication:** Required

```json
{
  "email": "newemail@example.com",
  "password": "NewPassword123!"
}
```

All fields are optional. Password will be hashed automatically.

### List All Users (Admin Only)

**Endpoint:** `GET /auth/users`  
**Authentication:** Required (Admin)

Query parameters:
- `username` - Filter by username
- `email` - Filter by email  
- `is_active` - Filter by active status
- `page` - Page number
- `size` - Items per page

### Delete User (Admin Only)

**Endpoint:** `DELETE /auth/users/{user_id}`  
**Authentication:** Required (Admin)

Deletes a user by UUID. Admins cannot delete themselves.

## How It Works

### Password Hashing

Passwords are hashed using bcrypt before storage:

```python
from api.users.auth import hash_password

hashed = hash_password("MyPassword123")
# Stored in database
```

### Token Generation

JWT tokens are created with user information:

```python
from api.users.auth import create_access_token

token = create_access_token({"sub": "johndoe"})
```

Token contains:
- `sub`: Username
- `exp`: Expiration timestamp

### Token Validation

When a request arrives with a token:

1. Extract token from Authorization header
2. Decode and validate JWT
3. Extract username from token
4. Load user from database
5. Verify user is active
6. Inject user into route handler

## Security Best Practices

### In Development

1. Use the default SECRET_KEY (already set)
2. Tokens expire in 30 days
3. Test with both regular users and admins

### In Production

1. **Change SECRET_KEY!** Generate with:
   ```bash
   openssl rand -hex 32
   ```
   
2. Set in environment variable:
   ```env
   SECRET_KEY=your-generated-key-here
   ```

3. Consider shorter token expiration:
   ```env
   ACCESS_TOKEN_EXPIRE_DAYS=7
   ```

4. Use HTTPS only
5. Enable rate limiting
6. Monitor failed login attempts
7. Implement password reset flow

## Creating Your First Admin

### Option 1: During Registration

Manually update the database:

```sql
UPDATE users SET is_superuser = true WHERE username = 'johndoe';
```

### Option 2: In Code

Create a setup script:

```python
# create_admin.py
import asyncio
from api.configs.database import async_session
from api.users.models import UserModel
from api.users.auth import hash_password
from uuid import uuid4
from datetime import datetime

async def create_admin():
    async with async_session() as session:
        admin = UserModel(
            id=uuid4(),
            username="admin",
            email="admin@example.com",
            hashed_password=hash_password("AdminPass123!"),
            is_active=True,
            is_superuser=True,
            created_at=datetime.utcnow()
        )
        session.add(admin)
        await session.commit()
        print("Admin created!")

asyncio.run(create_admin())
```

Run with: `python create_admin.py`

## Common Issues

### Token Invalid or Expired

**Problem:** Getting 401 Unauthorized  
**Solution:** Login again to get a new token

### Wrong Password Format

**Problem:** Password validation error  
**Solution:** Ensure password has uppercase, lowercase, and digit

### Cannot Access Admin Route

**Problem:** Getting 403 Forbidden  
**Solution:** Your user needs `is_superuser = true` in database

### Token Not Recognized

**Problem:** Token format error  
**Solution:** Include "Bearer " prefix:
```
Authorization: Bearer eyJhbGc...
```

## Examples

### Complete Registration Flow

```bash
# 1. Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "SecurePass123!"
  }'

# 2. Login
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "SecurePass123!"
  }' | jq -r '.access_token')

# 3. Get profile
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 4. Create protected resource
curl -X POST "http://localhost:8000/examples" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Item",
    "value": 99.99,
    "is_active": true
  }'
```

### Python Client Example

```python
import httpx

BASE_URL = "http://localhost:8000"

# Register
response = httpx.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "SecurePass123!"
    }
)
user = response.json()

# Login
response = httpx.post(
    f"{BASE_URL}/auth/login",
    json={
        "username": "bob",
        "password": "SecurePass123!"
    }
)
token = response.json()["access_token"]

# Make authenticated request
headers = {"Authorization": f"Bearer {token}"}
response = httpx.get(f"{BASE_URL}/auth/me", headers=headers)
print(response.json())
```

## Customization

### Change Token Expiration

In `.env`:
```env
ACCESS_TOKEN_EXPIRE_DAYS=7
```

### Change JWT Algorithm

In `.env`:
```env
ALGORITHM=HS512
```

### Add More User Fields

1. Add fields to `UserModel` in `api/users/models.py`
2. Add fields to `UserBase` schema in `api/users/schemas.py`
3. Create migration: `alembic revision --autogenerate -m "Add user fields"`
4. Apply: `alembic upgrade head`

### Custom Password Validation

Edit the `password_strength` validator in `api/users/schemas.py`:

```python
@field_validator('password')
@classmethod
def password_strength(cls, v: str) -> str:
    # Add your custom rules
    if len(v) < 12:
        raise ValueError('Password must be at least 12 characters')
    return v
```

## Next Steps

- Implement password reset flow
- Add email verification
- Implement refresh tokens
- Add OAuth2 social login
- Add two-factor authentication
- Implement session management
- Add login attempt tracking
