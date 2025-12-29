"""
FastAPI File-Based Router Demo Server

This server demonstrates the file-based routing system with support for:
- Static routes (index.py -> /)
- Dynamic routes ([id].py -> /{id})
- Typed routes ([id:int].py -> /{id:int})
- Slug routes ([slug:].py -> /{slug})
- Catch-all routes ([...path].py -> /{path:path})


Then visit http://localhost:8000 to see the demo in action.
"""

import uvicorn
from pathlib import Path
from fast_router import create_router

BASE_DIR = Path(__file__).resolve().parent
ROUTES_DIR = BASE_DIR / "routes"

router = create_router(str(ROUTES_DIR))
router.set_tag_metadata(
    "users", description="Operations with users and their profiles."
)
router.set_tag_metadata(
    "posts", description="Blog post management, including comments and raw processing."
)
router.set_tag_metadata("default", description="Root level endpoints.")
app = router.get_app()


def main():
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(ROUTES_DIR)],
        app_dir=str(BASE_DIR),
    )


if __name__ == "__main__":
    main()
