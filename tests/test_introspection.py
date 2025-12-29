import types
import pytest
import fast_router


def test_submodule_not_shadowed():
    """Test that fast_router.fast_router submodule is accessible and not shadowed by function."""
    # The submodule should be accessible via getattr
    submodule = getattr(fast_router, "fast_router")

    # It should be a module object, not a function
    assert isinstance(submodule, types.ModuleType), (
        f"Expected fast_router.fast_router to be a module, but got {type(submodule)}"
    )


def test_direct_submodule_import():
    """Test that direct import of submodule works."""
    # This should import the module, not get a function
    import fast_router.fast_router as submodule_direct

    assert isinstance(submodule_direct, types.ModuleType), (
        f"Direct import should return module, got {type(submodule_direct)}"
    )


def test_create_router_function_exists():
    """Test that the new create_router function is available."""
    from fast_router import create_router

    assert callable(create_router), "create_router should be a callable function"
    assert hasattr(create_router, "__call__"), "create_router should be callable"


def test_old_function_name_not_exported():
    """Test that old fast_router function name is not exported (no shadowing)."""
    import fast_router

    # The old name should not be in the package namespace
    # (it's now only accessible via submodule import)
    assert "fast_router" not in dir(fast_router) or isinstance(
        getattr(fast_router, "fast_router", None), types.ModuleType
    ), "fast_router should be the submodule, not a function"


def test_create_router_functionality(tmp_path):
    """Test that create_router actually works."""
    from fast_router import create_router

    # Create a simple route file
    routes_dir = tmp_path / "routes"
    routes_dir.mkdir()
    route_file = routes_dir / "index.py"
    route_file.write_text("""
def get():
    return {"message": "hello"}
""")

    # Use create_router
    router = create_router(str(routes_dir))

    assert router is not None
    assert hasattr(router, "get_app"), "Router should have get_app method"

    # Verify the route was registered
    from fastapi.testclient import TestClient

    client = TestClient(router.get_app())
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


def test_function_via_submodule_import(tmp_path):
    """Test that the fast_router function is accessible via submodule import."""
    from fast_router.fast_router import fast_router as func

    # Create a simple route file
    routes_dir = tmp_path / "routes"
    routes_dir.mkdir()
    route_file = routes_dir / "test.py"
    route_file.write_text("""
def post():
    return {"status": "ok"}
""")

    # Use the function from submodule
    router = func(str(routes_dir))

    assert router is not None
    assert hasattr(router, "get_app")

    # Verify it works
    from fastapi.testclient import TestClient

    client = TestClient(router.get_app())
    response = client.post("/test")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_package_exports():
    """Test that __all__ exports are correct."""
    import fast_router

    # Check that expected items are in __all__
    assert "FastRouter" in fast_router.__all__
    assert "create_router" in fast_router.__all__
    # fast_router should NOT be in __all__ to prevent shadowing
    assert "fast_router" not in fast_router.__all__

    # Verify the exported items are actually accessible
    assert hasattr(fast_router, "FastRouter")
    assert hasattr(fast_router, "create_router")


def test_fastrouter_class_not_affected():
    """Test that FastRouter class is still accessible."""
    from fast_router import FastRouter

    assert isinstance(FastRouter, type), "FastRouter should be a class"

    # Should be able to instantiate it
    router = FastRouter("routes")
    assert router is not None
    assert hasattr(router, "scan_routes")
