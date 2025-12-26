# Welcome to FastRouter

A simple and intuitive file-based router for FastAPI. This package allows you to define your API routes by structuring your files and directories, making your project more organized and easier to navigate.

[Get Started](./getting-started.md)

## How it Works

FastRouter uses **Static Analysis** (powered by Tree-sitter) to scan your `routes/` directory and map the file structure to your API endpoints. Unlike other routers, it doesn't need to execute your code to find routes, making it fast and safe.

## Features

### File-Based Routing
Create a `.py` file in your `routes` directory, and it will automatically become an endpoint.

- `routes/users.py` -> `/users`
- `routes/posts/all.py` -> `/posts/all`

### Dynamic Routes
For routes with path parameters, use square brackets `[]`.

- `routes/users/[id].py` -> `/users/{id}`
- `routes/posts/[id:int].py` -> `/users/{id:int}`

**Example:** `routes/users/[id].py`
```python
def get(id: str):
    """Get user by ID."""
    return {"user_id": id}
```

### Catch-all Routes
To match multiple path segments, use the catch-all syntax `[...]`.

- `routes/files/[...path].py` -> `/files/{path:path}`

**Example:** `routes/files/[...path].py`
```python
def get(path: str):
    """Serve files from a path."""
    return {"file_path": path}
```

### Index Routes
An `index.py` file within a directory serves as the root endpoint for that path.

- `routes/products/index.py` -> `/products`

### Lazy Loading
Modules are only loaded when they are first requested. This keeps your startup time near-instant, regardless of how many routes you have.

### Rich OpenAPI Metadata
Your docstrings are automatically parsed:
- The first line becomes the **Summary**.
- The rest becomes the **Description**.

---

FastRouter simplifies route management and keeps your codebase clean and scalable.
