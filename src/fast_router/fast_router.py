"""
Module: file_router.py
This module implements a file-based router for FastAPI, allowing dynamic route registration based on file structure.
It supports static, dynamic, typed, slug, and catch-all routes, along with custom tagging functionality.
"""

import re
import ast
import inspect
import logging
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any, Callable
from fastapi import FastAPI

from .analyzer import StaticAnalyzer


class FastRouter:
    """
    Main class for the file-based router.
    This class handles:
    - Scanning the routes directory
    - Converting file paths to route patterns
    - Loading route modules
    - Extracting route handlers
    - Registering routes with FastAPI
    - Custom tag assignment for routes
    - Providing access to registered routes and the FastAPI app instance
    """

    def __init__(self, routes_dir: str = "routes"):
        self.routes_dir = Path(routes_dir)
        self.app = FastAPI()
        self.analyzer = StaticAnalyzer()
        self._routes: List[Dict[str, Any]] = []
        self._custom_tags: Dict[str, str] = {}
        self._module_cache: Dict[Path, Any] = {}
        self._tag_metadata: List[Dict[str, Any]] = []

    def set_tag_metadata(
        self, name: str, description: str = None, external_docs: Dict[str, str] = None
    ):
        """Set metadata for a tag (directory)."""
        tag_info = {"name": name}
        if description:
            tag_info["description"] = description
        if external_docs:
            tag_info["externalDocs"] = external_docs

        for i, existing in enumerate(self._tag_metadata):
            if existing["name"] == name:
                self._tag_metadata[i] = tag_info
                break
        else:
            self._tag_metadata.append(tag_info)

        self.app.openapi_tags = self._tag_metadata

    def _generate_tag_from_route(self, route_pattern: str, file_path: Path) -> str:
        """
        Generate a tag for the route based on the route pattern.

        Priority:
        1. Specific file path custom tag if set
        2. Directory-level custom tag if set
        3. First path segment (e.g., /users/1 -> "users")
        4. "default" for root routes
        """
        file_path_str = str(file_path)

        if file_path_str in self._custom_tags:
            return self._custom_tags[file_path_str]

        current_path = file_path.parent
        while current_path != self.routes_dir.parent:
            dir_path_str = str(current_path)
            if dir_path_str in self._custom_tags:
                return self._custom_tags[dir_path_str]
            current_path = current_path.parent

        parts = [
            part
            for part in route_pattern.split("/")
            if part and not part.startswith("{")
        ]

        if parts:
            return parts[0]
        else:
            return "default"

    def set_custom_tag(self, path: str, tag: str):
        """
        Set a custom tag for a specific route file or directory.

        Examples:
        - router.set_custom_tag("routes/users/[id].py", "user-details") # Specific file
        - router.set_custom_tag("routes/users", "user-management")      # All files in directory
        """
        self._custom_tags[path] = tag

    def _parse_dynamic_segment(self, segment: str) -> Tuple[str, str, bool]:
        """
        Parse dynamic route segments using regex.
        Returns: (param_name, param_type, is_catch_all)
        """

        pattern = r"^\[(?P<catchall>\.\.\.)?(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)(?::(?P<type>[a-zA-Z_][a-zA-Z0-9_]*)?)?\]$"
        match = re.match(pattern, segment)

        if not match:
            return None, None, False

        groups = match.groupdict()
        param_name = groups["name"]
        param_type = groups["type"] or "str"
        is_catch_all = groups["catchall"] == "..."

        return param_name, param_type, is_catch_all

    def _convert_file_path_to_route(
        self, file_path: Path
    ) -> Tuple[List[str], Dict[str, Any]]:
        """
        Convert file path to FastAPI route patterns and extract parameters.
        Returns a list of patterns to support optional catch-all routes.
        """

        rel_path = file_path.relative_to(self.routes_dir)

        path_parts = list(rel_path.parts[:-1]) + [rel_path.stem]

        if path_parts[-1] == "index":
            path_parts = path_parts[:-1]

        route_pattern = ""
        params = {}

        for part in path_parts:
            param_name, param_type, is_catch_all = self._parse_dynamic_segment(part)

            if param_name:
                if is_catch_all:
                    route_pattern += f"/{{{param_name}:path}}"
                else:
                    if param_type == "int":
                        route_pattern += f"/{{{param_name}:int}}"
                    else:
                        route_pattern += f"/{{{param_name}}}"

                params[param_name] = {"type": param_type, "is_catch_all": is_catch_all}
            else:
                route_pattern += f"/{part}"

        if not route_pattern:
            route_pattern = "/"
        elif not route_pattern.startswith("/"):
            route_pattern = "/" + route_pattern

        return [route_pattern], params

    def _get_or_load_module(self, file_path: Path):
        """Get a module from cache or load it."""
        if file_path not in self._module_cache:
            self._module_cache[file_path] = self._load_route_module(file_path)
        return self._module_cache[file_path]

    def _load_route_module(self, file_path: Path):
        """Load a Python module from file path."""
        module_name = f"route_{file_path.stem}_{hash(str(file_path))}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _extract_route_handlers(
        self, module, route_pattern: str, params: Dict[str, Any]
    ):
        """Extract HTTP method handlers from a route module."""
        handlers = {}

        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

        for method in methods:
            handler_name = method.lower()
            if hasattr(module, handler_name):
                handler = getattr(module, handler_name)
                if callable(handler):
                    handlers[method] = handler

        return handlers

    def _create_route_wrapper(self, handler: Callable, params: Dict[str, Any]):
        """Create a wrapper function that properly handles path parameters."""
        sig = inspect.signature(handler)

        if not params:
            # create simple wrapper that preserves signature if not path parameters
            # this allows fastapi to handle request bodies, query params, headers, etc.
            if inspect.iscoroutinefunction(handler):

                async def simple_wrapper(*args, **kwargs):
                    return await handler(*args, **kwargs)
            else:

                def simple_wrapper(*args, **kwargs):
                    return handler(*args, **kwargs)

            # preserve the original signature for fastapi dependency injection
            simple_wrapper.__signature__ = sig
            return simple_wrapper

        original_params = list(sig.parameters.values())
        path_param_names = set(params.keys())

        # build new signature preserving non-path parameters as-is
        new_params = []

        for param_name, param_info in params.items():
            if param_info["type"] == "int":
                param_type = int
            else:
                param_type = str

            new_params.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type,
                )
            )

        for param in original_params:
            if param.name not in path_param_names:
                new_params.append(param)

        # wrapper function to preserve fastapi's dependency injection
        if inspect.iscoroutinefunction(handler):

            async def param_wrapper(*args, **kwargs):
                return await handler(*args, **kwargs)
        else:

            def param_wrapper(*args, **kwargs):
                return handler(*args, **kwargs)

        # Set the correct signature for FastAPI
        new_sig = inspect.Signature(new_params)
        param_wrapper.__signature__ = new_sig

        return param_wrapper

    def _create_lazy_wrapper(
        self,
        file_path: Path,
        handler_name: str,
        static_info: Dict[str, Any],
        path_params: Dict[str, Any],
    ):
        """Create a lazy wrapper that loads the module only when called."""

        new_params = []
        path_param_names = set(path_params.keys())

        for param_name, param_info in path_params.items():
            param_type = int if param_info["type"] == "int" else str
            new_params.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type,
                )
            )

        for p in static_info["params"]:
            if p["name"] in path_param_names:
                continue

            param_type = Any
            if p.get("type"):
                type_map = {
                    "int": int,
                    "str": str,
                    "float": float,
                    "bool": bool,
                    "dict": dict,
                    "list": list,
                }
                param_type = type_map.get(p["type"], Any)

            default = inspect.Parameter.empty
            if "default" in p:
                try:
                    # First try to evaluate as a literal (strings, numbers, etc.)
                    default = ast.literal_eval(p["default"])
                except Exception:
                    # If that fails, it might be a variable reference
                    # Load the module to resolve the variable
                    try:
                        module = self._get_or_load_module(file_path)
                        # Try to get the value from the module's namespace
                        default = eval(p["default"], module.__dict__)
                    except Exception:
                        # If we still can't resolve it, leave it as empty
                        pass

            new_params.append(
                inspect.Parameter(
                    p["name"],
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=param_type,
                    default=default,
                )
            )

        if static_info["is_async"]:

            async def lazy_wrapper(*args, **kwargs):
                module = self._get_or_load_module(file_path)
                handler = getattr(module, handler_name)
                if inspect.iscoroutinefunction(handler):
                    return await handler(*args, **kwargs)
                return handler(*args, **kwargs)
        else:

            def lazy_wrapper(*args, **kwargs):
                module = self._get_or_load_module(file_path)
                handler = getattr(module, handler_name)
                return handler(*args, **kwargs)

        lazy_wrapper.__signature__ = inspect.Signature(new_params)
        lazy_wrapper.__doc__ = static_info.get("docstring")
        return lazy_wrapper

    def scan_routes(self):
        """Scan the routes directory and register all route files."""
        if not self.routes_dir.exists():
            raise FileNotFoundError(f"Routes directory '{self.routes_dir}' not found")

        for file_path in self.routes_dir.rglob("*.py"):
            if file_path.name.startswith("__"):
                continue

            try:
                route_patterns, params = self._convert_file_path_to_route(file_path)

                analysis = self.analyzer.analyze_file(file_path)
                static_handlers = analysis["handlers"]
                stray_functions = analysis["stray_functions"]

                if not static_handlers:
                    continue

                if stray_functions:
                    logger = logging.getLogger("uvicorn.error")
                    if logger.hasHandlers():
                        for func_name in stray_functions:
                            logger.warning(
                                "Function '%s' in %s is not a recognized HTTP method handler",
                                func_name,
                                file_path.name,
                            )

                # register each handler
                for method, info in static_handlers.items():
                    handler_name = info["name"]

                    needs_immediate_load = False
                    for p in info["params"]:
                        # for complex default value (e.g. Depends, Body, Query)
                        if "default" in p and (
                            "(" in p["default"] or "[" in p["default"]
                        ):
                            needs_immediate_load = True
                            break
                        if "default" in p:
                            try:
                                ast.literal_eval(p["default"])  # ok if literal
                            except (ValueError, SyntaxError):
                                needs_immediate_load = True
                                break
                        # for complex type hint (e.g. pydantic model, list[int])
                        if p.get("type") and p["type"] not in [
                            "int",
                            "str",
                            "float",
                            "bool",
                            "dict",
                            "list",
                        ]:
                            needs_immediate_load = True
                            break

                    if needs_immediate_load:
                        module = self._get_or_load_module(file_path)
                        handler = getattr(module, handler_name)
                        wrapped_handler = self._create_route_wrapper(handler, params)
                    else:
                        wrapped_handler = self._create_lazy_wrapper(
                            file_path, handler_name, info, params
                        )

                    tag = self._generate_tag_from_route(route_patterns[0], file_path)

                    docstring = info.get("docstring")
                    summary = None
                    description = None
                    if docstring:
                        docstring = inspect.cleandoc(docstring)
                        lines = docstring.split("\n")
                        summary = lines[0].strip() if lines else None
                        if len(lines) > 1:
                            description = "\n".join(lines[1:]).strip()
                        else:
                            description = summary

                    for route_pattern in route_patterns:
                        self.app.add_api_route(
                            route_pattern,
                            wrapped_handler,
                            methods=[method],
                            name=f"{method.lower()}_{file_path.stem}",
                            tags=[tag],
                            summary=summary,
                            description=description,
                        )

                self._routes.append(
                    {
                        "patterns": route_patterns,
                        "file_path": str(file_path),
                        "params": params,
                        "methods": list(static_handlers.keys()),
                        "tag": tag,
                    }
                )

            except Exception as e:
                logger = logging.getLogger("uvicorn.error")
                if logger.hasHandlers():
                    logger.error(f"Error loading route {file_path}: {e}")
                continue

    def get_routes(self) -> List[Dict[str, Any]]:
        """Get information about all registered routes."""
        return self._routes.copy()

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app


def fast_router(routes_dir: str = "routes") -> FastRouter:
    """Create and configure a fast file-based router."""
    router = FastRouter(routes_dir)
    router.scan_routes()
    return router
