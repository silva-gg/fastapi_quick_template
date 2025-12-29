# HTTP Basic Authentication Guide

This guide explains how to use HTTP Basic Authentication with the API - the simplest way to authenticate!

## What is Basic Authentication?

HTTP Basic Authentication is a simple authentication scheme built into HTTP. You just send your username and password with each request - no tokens to manage!

**Simple!** Just: `curl -u username:password http://localhost:8000/examples`

## Why Basic Auth is Perfect for This Template

**Dead Simple:**
- ✅ No token management
- ✅ Works everywhere (curl, browsers, scripts)
- ✅ No extra API calls needed
- ✅ Perfect for getting started quickly

**When to Use:**
- 🎯 Scripts and automation (Python, Bash, PowerShell)
- 🎯 Command-line tools
- 🎯 Internal APIs
- 🎯 Development and testing
- 🎯 Quick prototypes

## Quick Start (30 seconds)

### 1. Register

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### 2. Use it!

```bash
# That's it! Now just add -u username:password to any request
curl -u john:SecurePass123! http://localhost:8000/examples
```

**You can use email instead of username too:**
```bash
curl -u john@example.com:SecurePass123! http://localhost:8000/examples
```

## Examples

### Create Something

```bash
curl -u john:SecurePass123! \
  -X POST http://localhost:8000/examples \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Item",
    "value": 99.99,
    "is_active": true
  }'
```

### List Everything

```bash
curl -u john:SecurePass123! http://localhost:8000/examples
```

### Update Something

```bash
curl -u john:SecurePass123! \
  -X PATCH http://localhost:8000/examples/YOUR-ID-HERE \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

### Delete Something

```bash
curl -u john:SecurePass123! \
  -X DELETE http://localhost:8000/examples/YOUR-ID-HERE
```

## Using in Your Code

### Python (requests)

```python
import requests

# Super simple!
response = requests.get(
    'http://localhost:8000/examples',
    auth=('john', 'SecurePass123!')
)
print(response.json())
```

### Python (httpx) - async

```python
import httpx

async with httpx.AsyncClient(
    auth=('john', 'SecurePass123!')
) as client:
    response = await client.get('http://localhost:8000/examples')
    print(response.json())
```

### JavaScript/Node.js

```javascript
// Using fetch
const username = 'john';
const password = 'SecurePass123!';
const auth = btoa(`${username}:${password}`);

fetch('http://localhost:8000/examples', {
  headers: {
    'Authorization': `Basic ${auth}`
  }
})
.then(r => r.json())
.then(data => console.log(data));
```

### PowerShell

```powershell
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("john:SecurePass123!"))
Invoke-RestMethod -Uri "http://localhost:8000/examples" `
  -Headers @{Authorization = "Basic $cred"}
```

## Testing with Swagger

1. Go to http://localhost:8000/docs
2. Click any protected endpoint
3. Click "Try it out"
4. Enter username and password when prompted
5. Test away!

## Protecting Your Endpoints

### Simple Protection

```python
from api.contrib.dependencies import CurrentUserBasic

@router.get('/my-endpoint')
async def my_endpoint(current_user: CurrentUserBasic):
    # Only authenticated users can access this
    return {"message": f"Hello {current_user.username}!"}
```

### Admin Only

```python
from api.contrib.dependencies import RequireAdminBasic

@router.delete('/admin/dangerous-stuff')
async def admin_only(admin: RequireAdminBasic):
    # Only admins can access this
    return {"message": "Admin access granted"}
```

## Complete Python Script Example

```python
#!/usr/bin/env python3
"""
Simple API client using Basic Auth
"""
import requests
import sys

BASE_URL = "http://localhost:8000"
USERNAME = "john"
PASSWORD = "SecurePass123!"

class APIClient:
    def __init__(self):
        self.auth = (USERNAME, PASSWORD)
    
    def create_item(self, name, value):
        response = requests.post(
            f"{BASE_URL}/examples",
            auth=self.auth,
            json={"name": name, "value": value, "is_active": True}
        )
        return response.json()
    
    def list_items(self):
        response = requests.get(
            f"{BASE_URL}/examples",
            auth=self.auth
        )
        return response.json()
    
    def delete_item(self, item_id):
        response = requests.delete(
            f"{BASE_URL}/examples/{item_id}",
            auth=self.auth
        )
        return response.status_code == 204

if __name__ == "__main__":
    client = APIClient()
    
    # Create item
    item = client.create_item("Test Item", 99.99)
    print(f"Created: {item}")
    
    # List items
    items = client.list_items()
    print(f"Total items: {items['total']}")
```

## Security Notes

### Development (localhost)
✅ Basic Auth is perfect - simple and secure enough

### Production
⚠️ **Use HTTPS!** Basic Auth sends credentials with every request
- Set up SSL/TLS certificate
- Use nginx or similar as reverse proxy
- Consider rate limiting

### Quick Security Checklist
- [ ] HTTPS in production (mandatory!)
- [ ] Strong passwords
- [ ] Rate limiting to prevent brute force
- [ ] Monitor failed login attempts
- [ ] Use environment variables for credentials

## Also Available: JWT Auth

If you need stateless tokens (for web/mobile apps), JWT auth is also included:

```python
# Login to get token
response = requests.post('http://localhost:8000/auth/login',
    json={"username": "john", "password": "SecurePass123!"})
token = response.json()['access_token']

# Use token
response = requests.get('http://localhost:8000/examples',
    headers={'Authorization': f'Bearer {token}'})
```

See [AUTHENTICATION.md](AUTHENTICATION.md) for JWT details.

## When to Use What?

| Use Case | Use This |
|----------|----------|
| Scripts & CLI tools | ✅ Basic Auth |
| Internal APIs | ✅ Basic Auth |
| Quick prototypes | ✅ Basic Auth |
| Web applications | JWT Token |
| Mobile apps | JWT Token |
| Need token refresh | JWT Token |

## Common Issues

### 401 Unauthorized
- Check username/password are correct
- Verify account is active
- Use email OR username (not both)

### 403 Forbidden
- User doesn't have required permissions
- For admin routes, user needs `is_superuser = true`

## Tips

**Store credentials securely:**
```python
import os
username = os.getenv('API_USERNAME')
password = os.getenv('API_PASSWORD')
```

**Test quickly with curl:**
```bash
# Save credentials
export API_USER="john:SecurePass123!"

# Use them
curl -u $API_USER http://localhost:8000/examples
```

**Debug auth issues:**
```bash
# See the Authorization header being sent
curl -v -u john:SecurePass123! http://localhost:8000/examples 2>&1 | grep Authorization
```

---

**That's it!** Basic Auth keeps things simple and gets you building features fast. 🚀
