# FastRouter

A powerful, high-performance file-based routing system for FastAPI. It automatically maps your directory structure to API routes using **Static Analysis** and **Lazy Loading**.

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

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the demo server:**
   ```bash
   PYTHONPATH=src uv run example/main.py
   ```

3. **Explore the API:**
   - Interactive Docs: http://localhost:8000/docs
   - Home: http://localhost:8000/

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
from fast_router import fast_router

router = fast_router("routes")
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

MIT License
