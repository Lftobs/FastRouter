# Advanced Features

FastRouter is designed for performance and developer experience. Here are some of the advanced features that set it apart.

## Static Analysis (Tree-sitter)

FastRouter uses **Static Analysis** to discover your routes. Instead of importing every file in your `routes/` directory at startup, it uses [Tree-sitter](https://tree-sitter.github.io/tree-sitter/) to parse the source code and identify:
- Which HTTP methods are implemented (`get`, `post`, etc.).
- The function signatures (parameters, type hints, defaults).
- Docstrings for OpenAPI documentation.

### Why Static Analysis?
- **Speed**: Startup is nearly instantaneous, even with hundreds of routes.
- **Safety**: We don't execute any top-level code in your route files during discovery.
- **Validation**: We can detect "stray" functions that don't match HTTP methods and warn you.

## Lazy Loading

By default, FastRouter is **Lazy**. It doesn't import your route modules until the first request hits that specific endpoint.

### Side-Effect Isolation
Because of lazy loading, any top-level code in your route files (like database connections or heavy model loading) won't run until it's actually needed.

### Smart Fallback
If a route uses complex FastAPI features that require runtime introspection (like `Depends()`, `Body()`, or custom Pydantic models), FastRouter automatically detects this and falls back to **Immediate Loading** for that specific route to ensure full compatibility.

## Rich OpenAPI Metadata

FastRouter automatically enhances your Swagger UI (`/docs`) using your Python docstrings.

### Summaries & Descriptions
- **Summary**: The first line of your function docstring.
- **Description**: Everything after the first line.

```python
def get(id: int):
    """
    Get a user by their ID.
    
    This part will appear in the expanded description section.
    You can use **Markdown** here!
    """
    return {"id": id}
```

### Tag Metadata
You can customize the documentation for entire directories (tags) using `set_tag_metadata`:

```python
from fast_router import fast_router

router = fast_router("routes")
router.set_tag_metadata(
    "users", 
    description="Operations with users and their profiles.",
    external_docs={"description": "User Guide", "url": "https://example.com/docs"}
)
```

## Parameter Validation
FastRouter validates your dynamic segment names. If you use a parameter in a filename (like `[id].py`) but forget to include it in your function signature (`def get():`), FastRouter will raise a clear error at startup.

