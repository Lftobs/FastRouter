# Internal API Reference

This page documents the internal classes and methods used by FastRouter. This is useful if you want to extend the router or understand its inner workings.

## `FileBasedRouter`

The main class responsible for scanning the directory and registering routes with FastAPI.

### Methods

#### `__init__(routes_dir: str = "routes", app: FastAPI = None)`
Initializes the router.
- `routes_dir`: The directory to scan for route files.
- `app`: An optional existing FastAPI instance. If not provided, a new one is created.

#### `scan_routes()`
Scans the `routes_dir` and registers all discovered routes. This method uses the `StaticAnalyzer` for discovery.

#### `set_tag_metadata(name: str, description: str = None, external_docs: Dict[str, str] = None)`
Sets metadata for a specific tag (directory).
- `name`: The name of the tag (usually the directory name).
- `description`: A description for the tag.
- `external_docs`: A dictionary with `description` and `url`.

#### `get_app() -> FastAPI`
Returns the FastAPI application instance with all routes registered.

#### `get_routes() -> List[Dict[str, Any]]`
Returns a list of all registered routes and their metadata.

---

## `StaticAnalyzer`

The class responsible for parsing Python files using Tree-sitter.

### Methods

#### `analyze_file(file_path: Path) -> Dict[str, Any]`
Parses a Python file and extracts route information.
- **Returns**: A dictionary containing:
    - `handlers`: A map of HTTP methods to handler info (name, params, docstring).
    - `stray_functions`: A list of function names that don't match HTTP methods and aren't private (don't start with `_`).

### Handler Info Structure
The `handlers` dictionary contains:
- `name`: The original function name.
- `params`: A list of parameter dictionaries (name, type, default).
- `docstring`: The raw docstring extracted from the function.
