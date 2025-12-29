# Migration Guide: fast_router → create_router

## Overview

In version 0.3.0+, we've renamed the `fast_router` convenience function to `create_router` to prevent module shadowing and ensure compatibility with Python introspection tools, documentation generators, and type checkers.

## Quick Migration

### Simple Find & Replace

**Step 1:** Update your imports
```python
# Old (v0.2.x and earlier)
from fast_router import fast_router

# New (v0.3.0+)
from fast_router import create_router
```

**Step 2:** Update function calls
```python
# Old (v0.2.x and earlier)
router = fast_router("routes")

# New (v0.3.0+)
router = create_router("routes")
```

That's it! The function signature and behavior are identical.

## Why This Change?

The old name `fast_router` shadowed the `fast_router.fast_router` submodule, breaking Python's standard module introspection. This caused issues with:

- Documentation generators (Sphinx, pdoc)
- Type checkers (mypy, pyright)
- IDE introspection (PyCharm, VS Code)
- Any tool relying on `getattr()` or module inspection

The new name `create_router` is more descriptive and follows Python best practices.

## Migration Examples

### Basic Usage

```python
# Before
from fast_router import fast_router
router = fast_router("routes")
app = router.get_app()

# After
from fast_router import create_router
router = create_router("routes")
app = router.get_app()
```

### With Custom Configuration

```python
# Before
from fast_router import FastRouter
router = FastRouter("routes")
router.set_tag_metadata("users", description="User operations")
router.scan_routes()
app = router.get_app()

# After (no change needed for class-based usage)
from fast_router import FastRouter
router = FastRouter("routes")
router.set_tag_metadata("users", description="User operations")
router.scan_routes()
app = router.get_app()
```

### Uvicorn Integration

```python
# Before
from fast_router import fast_router
router = fast_router("routes")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router.get_app(), host="0.0.0.0", port=8000)

# After
from fast_router import create_router
router = create_router("routes")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router.get_app(), host="0.0.0.0", port=8000)
```

## Alternative: Keep Using Old Name

If you absolutely need to keep the old function name in your code (not recommended), you can import it from the submodule:

```python
from fast_router.fast_router import fast_router

# Works exactly as before
router = fast_router("routes")
```

Or create an alias:

```python
from fast_router import create_router as fast_router

# Use your preferred name
router = fast_router("routes")
```

## What's Not Changed

The following APIs remain **completely unchanged**:

✅ `FastRouter` class  
✅ `FastRouter.scan_routes()` method  
✅ `FastRouter.get_app()` method  
✅ `FastRouter.get_routes()` method  
✅ `FastRouter.set_tag_metadata()` method  
✅ Route file structure and conventions  
✅ Dynamic route patterns (`[id]`, `[id:int]`, `[slug:]`, `[...path]`)  
✅ HTTP method handlers (`get`, `post`, `put`, `delete`, etc.)  
✅ All existing functionality and behavior  

## Automated Migration Script

Here's a Python script to automatically update your codebase:

```python
#!/usr/bin/env python3
"""
Migrate from fast_router to create_router
"""
import re
from pathlib import Path

def migrate_file(file_path):
    """Update a single Python file."""
    content = file_path.read_text()
    
    # Pattern 1: from fast_router import fast_router
    pattern1 = r'from fast_router import fast_router\b'
    replacement1 = 'from fast_router import create_router'
    content = re.sub(pattern1, replacement1, content)
    
    # Pattern 2: fast_router( function calls
    pattern2 = r'\bfast_router\('
    replacement2 = 'create_router('
    content = re.sub(pattern2, replacement2, content)
    
    file_path.write_text(content)
    print(f"✓ Updated {file_path}")

def main():
    """Migrate all Python files in current directory."""
    for py_file in Path('.').rglob('*.py'):
        if 'venv' in str(py_file) or '.venv' in str(py_file):
            continue
        try:
            migrate_file(py_file)
        except Exception as e:
            print(f"✗ Error updating {py_file}: {e}")

if __name__ == "__main__":
    print("🔄 Migrating from fast_router to create_router...")
    main()
    print("✅ Migration complete!")
```

Save as `migrate.py` and run:
```bash
python migrate.py
```

## Testing After Migration

1. **Run your test suite:**
   ```bash
   pytest
   # or
   python -m pytest
   ```

2. **Verify your application starts:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

3. **Check for any remaining references:**
   ```bash
   grep -r "fast_router(" --include="*.py" .
   ```

## FAQ

### Q: Is this a breaking change?
**A:** Yes, but it's a simple rename. The migration is straightforward and the benefits (proper module introspection, tool compatibility) are significant.

### Q: Can I use both names during migration?
**A:** Yes, you can temporarily import both:
```python
from fast_router import create_router
from fast_router.fast_router import fast_router

# Use whichever you need during transition
```

### Q: Will the old name be supported in future versions?
**A:** No. The old name creates fundamental issues with Python's module system. However, you can always import it from the submodule if needed.

### Q: Do I need to update my route files?
**A:** No! Route files are unchanged. Only update the code where you create the router.

### Q: What if I'm using the `FastRouter` class directly?
**A:** No changes needed! The class-based API is unchanged:
```python
from fast_router import FastRouter  # Still works exactly the same
```

### Q: Are there any performance differences?
**A:** No. This is purely a naming change with zero performance impact.

### Q: What about type hints?
**A:** Type hints work the same way:
```python
from fast_router import FastRouter, create_router

def setup_router() -> FastRouter:
    return create_router("routes")
```

## Version Compatibility

| Version | `fast_router` Function | `create_router` Function | Recommendation |
|---------|----------------------|------------------------|----------------|
| < 0.3.0 | ✅ Available | ❌ Not Available | Use `fast_router` |
| ≥ 0.3.0 | ⚠️ Submodule only | ✅ Available | Use `create_router` |

## Getting Help

If you encounter issues during migration:

1. **Check the examples**: See `example/main.py` for updated usage
2. **Run the test suite**: `pytest tests/` to see working examples
3. **File an issue**: [GitHub Issues](https://github.com/yourusername/fast-router/issues)
4. **Read the docs**: Full documentation at [docs link]

## Summary Checklist

- [ ] Update imports: `from fast_router import create_router`
- [ ] Update function calls: `create_router("routes")`
- [ ] Run tests to verify everything works
- [ ] Update documentation/comments
- [ ] Search for any remaining references
- [ ] Commit changes

## Additional Resources

- [README.md](https://github.com/Lftobs/FastRouter/blob/main/README.md) - Updated usage examples
- [tests/test_introspection.py](https://github.com/Lftobs/FastRouter/blob/main/tests/test_introspection.py) - Working examples

---

**Need help?** Open an issue or check the examples directory for updated code samples.