# Getting Started

This guide will walk you through setting up and using the FastAPI File-Based Router in your project.

## Installation

First, install the package using pip:

```bash
pip install fastapi-file-based-router
```

## Basic Usage

1.  **Create a `routes` directory:** In your project's root directory, create a folder named `routes`.

    ```
    .
    ├── main.py
    └── routes/

    ```

2.  **Define your routes:** Create Python files inside the `routes` directory to define your API endpoints. For example, to create a simple "Hello World" endpoint at the root (`/`), create a file named `routes/index.py`:

```python
--8<-- "routes/index.py"
```

3.  **Integrate with FastAPI:** In your main application file (e.g., `main.py`), import and use the `FileRouter`.

    ```python
    # main.py
    from fastapi import FastAPI
    from file_router import FileRouter

    router = FileRouter("routes")
    app = router.get_app()

    if __name__ == 'main':
        uvicorn.run(
            "main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["routes"]
        )

    ```

Now, when you run your FastAPI application, the file-based router will automatically discover and register the routes from the `routes` directory. You can access your new endpoint at `http://127.0.0.1:8000/`.
