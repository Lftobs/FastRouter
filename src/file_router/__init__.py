from .fast_router import FileBasedRouter, FileRouter

# Alias for convenience as used in main.py and tests
file_router = FileRouter

__all__ = ["FileBasedRouter", "FileRouter", "file_router"]
