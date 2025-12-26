# Contributing to FastRouter

First off, thank you for considering contributing to FastRouter! It's people like you who make FastRouter such a great tool.

## Development Setup

We use [uv](https://github.com/astral-sh/uv) for dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lftobs/FastRouter.git
   cd FastRouter
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Install pre-commit hooks (optional but recommended):**
   We use `ruff` for linting and formatting.

## Running Tests

We use `pytest` for testing. You can run the tests using the provided `Makefile`:

```bash
make test
```

Or directly via `uv`:

```bash
uv run pytest
```

## Code Style

We follow the standard Python code style and use `ruff` for linting and formatting. Before submitting a pull request, please ensure your code passes the linting checks:

```bash
uv run ruff check .
uv run ruff format .
```

## Submitting Changes

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they are well-tested.

3. **Commit your changes** with a descriptive commit message.

4. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** against the `main` branch of the original repository.

## Documentation

If you're making changes that affect the public API or add new features, please update the documentation in the `docs/` directory. You can preview the documentation locally:

```bash
uv run mkdocs serve
```

## License

By contributing to FastRouter, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
