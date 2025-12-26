# Changelog

All notable changes to FastRouter will be documented in this file.

## [0.2.0] - 2025-12-26

### Changed
- **PEP 8 Naming Refactor**: 
    - Renamed `FileBasedRouter` class to `FastRouter`.
    - Renamed package from `file_router` to `fast_router`.
- **Project Structure**: Finalized the move to `src/fast_router`.

## [0.1.0] - 2025-12-26

### Added
- **Static Analysis**: Integrated Tree-sitter for route discovery without code execution.
- **Lazy Loading**: Implemented on-demand module loading for faster startup.
- **Side-Effect Isolation**: Top-level code in route files now only runs when the route is first accessed.
- **OpenAPI Metadata**: Automatic extraction of summaries and descriptions from docstrings.
- **Tag Metadata**: Added `set_tag_metadata` for documenting directories.
- **Parameter Validation**: Startup-time validation for path parameter names.
- **Smart Fallback**: Automatic detection of complex dependencies requiring immediate loading.

### Changed
- **Handler Syntax**: Switched from `APIRouter` to simple function-based handlers (`def get()`, `def post()`, etc.).
- **Dynamic Segments**: Improved regex-based parsing for `[id]`, `[id:int]`, `[slug:]`, and `[...path]`.
- **Project Structure**: Moved example code to a dedicated `example/` directory.

---

## Future Plans

- **Middleware Support**: Directory-level middleware (e.g., `_middleware.py`).
- **Dependency Injection**: Enhanced support for shared dependencies across directories.
- **WebSocket Support**: File-based routing for WebSockets.
- **Auto-Generation**: Tools to scaffold new route files.
- **Performance Monitoring**: Built-in metrics for route loading times.
