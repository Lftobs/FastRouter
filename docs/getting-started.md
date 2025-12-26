# Getting Started

This guide will walk you through setting up and using FastRouter in your project.

## Installation

We recommend using [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
uv add fast-router
```

Or using pip:

```bash
pip install fast-router
```

## Basic Usage

### 1. Create a `routes` directory
In your project's root directory, create a folder named `routes`.

```text
.
├── main.py
└── routes/
```

### 2. Define your routes
Create Python files inside the `routes` directory. For example, to create a "Hello World" endpoint at the root (`/`), create `routes/index.py`:

```python
def get():
    """Welcome to FastRouter!"""
    return {"message": "Hello World"}
```

### 3. Integrate with FastAPI
In your `main.py`, use the `file_router` helper:

```python
import uvicorn
from fastapi import FastAPI
from fast_router import fast_router

# Initialize the router
router = fast_router("routes")
app = router.get_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

## Running the Server

Run your application using `uv`:

```bash
PYTHONPATH=src uv run main.py
```

Now visit `http://127.0.0.1:8000/` to see your API in action, or `http://127.0.0.1:8000/docs` for the interactive documentation.
