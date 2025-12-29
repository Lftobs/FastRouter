import pytest
import shutil
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from fast_router import FastRouter


class TestRouterE2E:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.temp_dir = tempfile.mkdtemp()
        self.routes_dir = Path(self.temp_dir) / "routes"
        self.routes_dir.mkdir()
        yield
        shutil.rmtree(self.temp_dir)

    def create_route(self, path: str, content: str):
        f = self.routes_dir / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)

    def test_full_flow(self):
        self.create_route("index.py", "def get(): return {'msg': 'home'}")
        self.create_route(
            "users/[id:int].py", "def get(id: int): return {'user_id': id}"
        )
        self.create_route(
            "blog/[...path].py", "def get(path: str): return {'path': path}"
        )

        router = FastRouter(str(self.routes_dir))
        router.scan_routes()
        app = router.get_app()
        client = TestClient(app)

        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"msg": "home"}

        resp = client.get("/users/42")
        assert resp.status_code == 200
        assert resp.json() == {"user_id": 42}

        resp = client.get("/users/abc")
        assert resp.status_code in [404, 422]

        resp = client.get("/blog/some/deep/path")
        assert resp.status_code == 200
        assert resp.json() == {"path": "some/deep/path"}

    def test_side_effect_isolation(self, capsys):
        self.create_route(
            "side_effect.py",
            """
print("SIDE_EFFECT_EXECUTED")
def get(): return {"ok": True}
""",
        )
        router = FastRouter(str(self.routes_dir))
        router.scan_routes()

        captured = capsys.readouterr()
        assert "SIDE_EFFECT_EXECUTED" not in captured.out

        client = TestClient(router.get_app())
        resp = client.get("/side_effect")

        assert resp.status_code == 200
        captured = capsys.readouterr()
        assert "SIDE_EFFECT_EXECUTED" in captured.out

    def test_async_handler_e2e(self):
        self.create_route(
            "async_route.py",
            """
import asyncio
async def get():
    await asyncio.sleep(0.01)
    return {"async": True}
""",
        )
        router = FastRouter(str(self.routes_dir))
        router.scan_routes()
        client = TestClient(router.get_app())

        resp = client.get("/async_route")
        assert resp.status_code == 200
        assert resp.json() == {"async": True}

    def test_variable_default_values(self):
        """Test that default values referencing module variables work correctly."""
        self.create_route(
            "items.py",
            """
DEFAULT_PAGE_SIZE = 20
DEFAULT_SORT = "asc"

def get(page_size: int = DEFAULT_PAGE_SIZE, sort: str = DEFAULT_SORT):
    return {"page_size": page_size, "sort": sort}
""",
        )
        router = FastRouter(str(self.routes_dir))
        router.scan_routes()
        client = TestClient(router.get_app())

        resp = client.get("/items")
        assert resp.status_code == 200
        assert resp.json() == {"page_size": 20, "sort": "asc"}

        resp = client.get("/items?page_size=50")
        assert resp.status_code == 200
        assert resp.json() == {"page_size": 50, "sort": "asc"}

        resp = client.get("/items?page_size=10&sort=desc")
        assert resp.status_code == 200
        assert resp.json() == {"page_size": 10, "sort": "desc"}
