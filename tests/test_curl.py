import pytest
from fast_router import create_router
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    router = create_router("example/routes")
    return TestClient(router.get_app())


@pytest.mark.parametrize(
    "test_case",
    [
        {
            "name": "POST /users with JSON body",
            "method": "POST",
            "url": "/users",
            "json": {"name": "Test User", "email": "test@example.com"},
        },
        {
            "name": "GET /posts with query params",
            "method": "GET",
            "url": "/posts",
            "params": {"limit": 5, "published_only": True},
        },
        {
            "name": "POST /posts with complex body",
            "method": "POST",
            "url": "/posts",
            "json": {
                "title": "Test Post",
                "content": "Test content",
                "tags": ["test"],
                "published": True,
            },
            "headers": {"Authorization": "Bearer test-token"},
        },
    ],
    ids=lambda x: x["name"],
)
def test_api_endpoints(client, test_case):
    response = client.request(
        method=test_case["method"],
        url=test_case["url"],
        json=test_case.get("json"),
        params=test_case.get("params"),
        headers=test_case.get("headers"),
    )
    assert response.status_code == 200, (
        f"Test '{test_case['name']}' failed: {response.text}"
    )
