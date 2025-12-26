# Request Body Handling

FastRouter handles request bodies through **FastAPI's dependency injection system**. Because the router preserves your function signatures, FastAPI can automatically handle:

- **JSON Request Bodies** (Pydantic models)
- **Query Parameters** 
- **Headers**
- **Form Data**
- **Raw Request Access**

## How It Works

FastRouter uses static analysis to find your functions, but it doesn't change how FastAPI works. When a request comes in, FastAPI sees your function exactly as you wrote it.

## Examples

### 1. JSON Request Body (Pydantic Models)

```python
# routes/users/index.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

def post(user_data: UserCreate):
    """Create a new user."""
    return {"user": user_data.dict()}
```

**Usage**: `POST /users` with JSON body `{"name": "John", "email": "john@example.com"}`

### 2. Path Parameters + Request Body

```python
# routes/users/[id:int].py
from pydantic import BaseModel

class UserUpdate(BaseModel):
    name: str = None

def put(id: int, user_data: UserUpdate):
    """Update user by ID."""
    return {"id": id, "updated_data": user_data}
```

**Usage**: `PUT /users/123` with JSON body

### 3. Query Parameters + Headers

```python
# routes/posts.py
from fastapi import Query, Header
from typing import Optional

def get(
    limit: int = Query(10),
    authorization: Optional[str] = Header(None)
):
    """Get posts with pagination and auth check."""
    return {"limit": limit, "has_auth": authorization is not None}
```

**Usage**: `GET /posts?limit=5` with `Authorization` header

### 4. Multiple Body Parts

```python
from fastapi import Body

def put(
    post_data: dict = Body(...),
    comments: list = Body([]),
):
    """Update post and comments in one request."""
    return {"post": post_data, "comments": comments}
```

### 5. Raw Request Access

```python
from fastapi import Request

async def patch(request: Request):
    """Handle raw request for custom processing."""
    body = await request.body()
    return {"body_size": len(body)}
```

## Supported Parameter Types

| Type | Example | Usage |
|------|---------|-------|
| **Path** | `id: int` | From URL: `/users/{id}` |
| **JSON Body** | `user: UserModel` | From request body |
| **Query** | `limit: int = Query(10)` | From URL: `?limit=10` |
| **Header** | `auth: str = Header(None)` | From HTTP headers |
| **Form** | `name: str = Form(...)` | From form data |
| **Raw** | `request: Request` | Full request access |

FastRouter automatically handles all FastAPI parameter types while adding file-based routing capabilities! 🚀