## [0.4.0] - 2025-12-29
=======================
### 

#### Bug Fixes

- Fixed variable reference default values in lazy loading mechanism.

  Route handlers can now use module-level constants as default parameter values
  without causing validation errors. Previously, parameters like
  `def get(page_size: int = DEFAULT_PAGE_SIZE)` would fail with 422 errors.


```
<file_path>
file-based-router/changelog.d/changelog_template.jinja
</file_path>

<edit_description>
Create changelog template for towncrier
</edit_description># Changelog

All notable changes to FastRouter will be documented in this file.

## [0.3.0] - 2024-12-15

### 🚀 Major Update with Breaking Changes

This release includes comprehensive bug fixes, encoding support, and API improvements.

### ⚠️ Breaking Changes

- **Renamed convenience function**: `fast_router` → `create_router` to prevent module shadowing
  - **Migration**: Replace `from fast_router import fast_router` with `from fast_router import create_router`
  - **Rationale**: The old name shadowed the `fast_router.fast_router` submodule, breaking Python introspection tools, documentation generators, and type checkers
  - **Alternative**: Import from submodule: `from fast_router.fast_router import fast_router`
  - See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed migration instructions

### ✨ Added

- **PEP 263 Encoding Support**: StaticAnalyzer now properly detects and respects file encoding declarations
  - Supports Latin-1, ISO-8859-15, UTF-8 with BOM, and all Python-supported encodings
  - Added `tokenize.detect_encoding()` for automatic encoding detection
  - Fixed crashes when analyzing non-UTF-8 encoded route files
- **Comprehensive Test Suite**: Added 8 new introspection tests and 3 encoding tests
- **Documentation**:
  - Added `BUGFIX_MODULE_SHADOWING.md` - Technical details of module shadowing fix
  - Added `BUGFIX_ENCODING_SUPPORT.md` - PEP 263 encoding implementation details
  - Added `BUGFIX_VARIABLE_DEFAULTS.md` - Variable reference defaults fix documentation
  - Added `MIGRATION_GUIDE.md` - Step-by-step migration instructions
  - Added `CHANGELOG.md` - Version history documentation

### 🐛 Fixed

- **Variable Reference Default Values**: Fixed lazy loading mechanism to properly resolve default values that reference module-level variables
  - Example: `def get(page_size: int = DEFAULT_PAGE_SIZE)` now works correctly
  - Added fallback mechanism using `eval()` with module namespace
  - Added detection for variable references to trigger immediate loading when needed
- **Duplicate Error Logging**: Fixed error messages being logged twice during route scanning
  - Added handler check before logging (`if logger.hasHandlers()`)
  - Now logs errors only once to uvicorn logger
- **Module Shadowing**: Fixed `fast_router` function shadowing the `fast_router.fast_router` submodule
  - Python introspection now works correctly
  - Compatible with documentation generators (Sphinx, pdoc)
  - Compatible with type checkers (mypy, pyright)
  - Compatible with IDE introspection tools
- **Encoding Detection**: Fixed hardcoded UTF-8 decoding in StaticAnalyzer
  - Now respects PEP 263 encoding declarations
  - Handles files with non-UTF-8 characters correctly
  - All 12 hardcoded `.decode("utf-8")` calls now use detected encoding

### 🔧 Changed

- **Development Status**: Remains in "Beta" as API continues to mature
- **API Naming**: `create_router` is now the primary convenience function
- **Example Files**: Updated all examples to use `create_router`
- **Test Files**: Updated all tests to use new API

### 📊 Test Coverage

- **Total Tests**: 39 tests, all passing
  - 9 analyzer tests (including encoding tests)
  - 3 curl/API tests
  - 5 e2e router tests (including variable defaults)
  - 14 file router tests
  - 8 introspection tests (new)

### 🔗 Links

- [Migration Guide](MIGRATION_GUIDE.md)
- [Module Shadowing Fix Details](BUGFIX_MODULE_SHADOWING.md)
- [Encoding Support Details](BUGFIX_ENCODING_SUPPORT.md)
- [Variable Defaults Fix Details](BUGFIX_VARIABLE_DEFAULTS.md)

## [0.2.0] - 2024-06-20

### Changed
- **PEP 8 Naming Refactor**:
    - Renamed `FileBasedRouter` class to `FastRouter`.
    - Renamed package from `file_router` to `fast_router`.
- **Project Structure**: Finalized the move to `src/fast_router`.

## [0.1.0] - 2024-01-15

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