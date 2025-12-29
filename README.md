# FastRouter

A simple and intuitive file-based router for FastAPI. This package allows you to define your API routes by structuring your files and directories, making your project more organized and easier to navigate.
> [!NOTE]
> You can use this to fuck with your personal or a friends repo but do not push to production :)  

## 🚀 Features

- **Static Analysis**: Uses `tree-sitter` to discover routes without executing your code.
- **Lazy Loading**: Route modules are only imported when the first request hits the endpoint.
- **Side-Effect Isolation**: Startup is silent. Top-level code in route files only runs on demand.
- **Rich OpenAPI Integration**:
    - **Automatic Summaries**: The first line of your docstring becomes the route summary.
    - **Detailed Descriptions**: The rest of the docstring becomes the route description.
    - **Tag Metadata**: Configure directory-level documentation with `set_tag_metadata`.
- **Flexible Routing**:
    - **Static**: `index.py` → `/`
    - **Dynamic**: `[id].py` → `/{id}`
    - **Typed**: `[id:int].py` → `/{id:int}`
    - **Slug**: `[slug:].py` → `/{slug}`
    - **Catch-all**: `[...path].py` → `/{path:path}`
- **Full FastAPI Support**: Works with `Depends()`, Pydantic models, and all HTTP methods.

## 🛠️ Quick Start

### Installation

We recommend using [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
uv add fast-router
```

Or using pip:

```bash
pip install fast-router
```

### Basic Usage

#### 1. Create a `routes` directory
In your project's root directory, create a folder named `routes`.

```text
.
├── main.py
└── routes/
```

#### 2. Define your routes
Create Python files inside the `routes` directory. For example, to create a "Hello World" endpoint at the root (`/`), create `routes/index.py`:

```python
def get():
    """Welcome to FastRouter!"""
    return {"message": "Hello World"}
```

#### 3. Integrate with FastAPI
In your `main.py`, use the `create_router` helper:

```python
import uvicorn
from fast_router import create_router

# Initialize the router
router = create_router("routes")
app = router.get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### Running the Server

Run your application using `uv`:

```bash
PYTHONPATH=src uv run main.py
```

Now visit `http://127.0.0.1:8000/` to see your API in action, or `http://127.0.0.1:8000/docs` for the interactive documentation.

## 📂 Directory Structure

```text
routes/
├── index.py                 # GET /
├── users/
│   ├── index.py            # GET /users
│   └── [id:int].py        # GET /users/{id}
├── blog/
│   └── [slug:].py         # GET /blog/{slug}
└── files/
    └── [...path].py       # GET /files/{path:path}
```

## 📝 Route Handler Example

```python
from fastapi import Query

def get(id: int, q: str = Query(None)):
    """
    Get user by ID.
    
    This description will appear in the expanded section of the 
    OpenAPI documentation, while the first line is the summary.
    """
    return {"user_id": id, "query": q}
```

## ⚙️ Advanced Configuration

### Tag Metadata
You can customize the documentation for each directory (tag) in your router:

```python
from fast_router import create_router

router = create_router("routes")
router.set_tag_metadata(
    "users", 
    description="Operations with users and their profiles.",
    external_docs={"description": "User Guide", "url": "https://example.com/docs"}
)
app = router.get_app()
```

### Smart Fallback
The router is lazy by default. However, if it detects complex FastAPI features (like `Depends()` or Pydantic models) that require runtime introspection, it automatically falls back to immediate loading for that specific route to ensure 100% compatibility.

## 🧪 Running Tests

We use `pytest` for unit and E2E testing, managed via `uv`.

```bash
make test
```

## 📜 License

[MIT License](LICENSE)
