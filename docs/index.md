# Welcome to FastRouter

A simple and intuitive file-based router for FastAPI. This package allows you to define your API routes by structuring your files and directories, making your project more organized and easier to navigate.

[Get Started](./getting-started.md)

## How it Works

The router automatically scans a specified directory (by default, `routes/`) and maps the file structure to your API endpoints. This means you can create new routes simply by adding new Python files.

## Features

### File-Based Routing
Create a `.py` file in your `routes` directory, and it will automatically become an endpoint.

- `routes/users.py` -> `/users`
- `routes/posts/all.py` -> `/posts/all`

### Dynamic Routes
For routes with path parameters, use square brackets `[]`. The parameter name inside the brackets will be available in your path operation function.

- `routes/users/[id].py` -> `/users/{id}`

**Example:** `routes/users/[id].py`
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{id}")
def get_user(id: str):
    return {"user_id": id}
```

### Catch-all Routes
To match multiple path segments, use the catch-all syntax `[...]`. This is useful for serving files or creating proxy endpoints.

- `routes/files/[...path].py` -> `/files/{path:path}`

**Example:** `routes/files/[...path].py`
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/files/{path:path}")
def read_file(path: str):
    return {"file_path": path}
```

### Index Routes
An `index.py` file within a directory serves as the root endpoint for that path.

- `routes/products/index.py` -> `/products`

**Example:** `routes/products/index.py`
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
def list_products():
    return ["Laptop", "Mouse", "Keyboard"]
```

This approach simplifies route management and keeps your codebase clean and scalable.
