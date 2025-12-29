import ast
import tokenize
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
from pathlib import Path
from typing import Dict, List, Any


class StaticAnalyzer:
    def __init__(self):
        self.language = Language(tspython.language())
        self.parser = Parser(self.language)

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a python file and extract HTTP method handlers and stray functions.
        Returns a dict with:
        - 'handlers': Dict[str, Dict] (HTTP method -> handler info)
        - 'stray_functions': List[str] (names of functions that are not handlers or private)
        """
        if not file_path.exists():
            return {"handlers": {}, "stray_functions": []}

        # Detect file encoding per PEP 263
        with open(file_path, "rb") as f:
            encoding, _ = tokenize.detect_encoding(f.readline)

        content = file_path.read_bytes()
        tree = self.parser.parse(content)
        root_node = tree.root_node

        handlers = {}
        stray_functions = []
        methods = {"get", "post", "put", "delete", "patch", "head", "options"}

        for child in root_node.children:
            if child.type == "function_definition":
                if child.has_error:
                    continue
                is_async = any(c.type == "async" for c in child.children)

                name_node = child.child_by_field_name("name")
                if name_node:
                    func_name = content[
                        name_node.start_byte : name_node.end_byte
                    ].decode(encoding)

                    if func_name.lower() in methods:
                        params_node = child.child_by_field_name("parameters")
                        params = self._parse_parameters(params_node, content, encoding)

                        body = child.child_by_field_name("body")
                        docstring = None
                        if body and body.children:
                            for stmt in body.children:
                                if stmt.type == "expression_statement":
                                    expr = stmt.children[0]
                                    if expr.type == "string":
                                        try:
                                            docstring = ast.literal_eval(
                                                content[
                                                    expr.start_byte : expr.end_byte
                                                ].decode(encoding)
                                            )
                                        except Exception:
                                            docstring = (
                                                content[expr.start_byte : expr.end_byte]
                                                .decode(encoding)
                                                .strip("\"'")
                                            )
                                    break
                                elif stmt.type not in ["comment"]:
                                    break

                        handlers[func_name.upper()] = {
                            "name": func_name,
                            "params": params,
                            "is_async": is_async,
                            "docstring": docstring,
                        }
                    elif not func_name.startswith("_"):
                        stray_functions.append(func_name)

        return {"handlers": handlers, "stray_functions": stray_functions}

    def _parse_parameters(
        self, params_node, content: bytes, encoding: str = "utf-8"
    ) -> List[Dict[str, Any]]:
        """
        Parse function parameters to extract names and type hints.
        Example:
        def handler(a: int, b: str = "hello") -> int:
            return a + len(b)

        returns:
        [
            {
                "name": "a",
                "type": "int",
                "default": None
            },
            {
                "name": "b",
                "type": "str",
                "default": "hello"
            }
        ]
        """
        params = []
        if not params_node:
            return params

        for child in params_node.children:
            if child.type in ["(", ")", ","]:
                continue

            param_info = {}

            if child.type == "typed_parameter":
                for sub in child.children:
                    if sub.type == "identifier":
                        param_info["name"] = content[
                            sub.start_byte : sub.end_byte
                        ].decode(encoding)
                    elif sub.type == "type":
                        param_info["type"] = content[
                            sub.start_byte : sub.end_byte
                        ].decode(encoding)

            elif child.type == "identifier":
                param_info["name"] = content[child.start_byte : child.end_byte].decode(
                    encoding
                )
                param_info["type"] = None

            elif child.type == "default_parameter":
                name_node = child.child_by_field_name("name")
                value_node = child.child_by_field_name("value")
                if name_node:
                    param_info["name"] = content[
                        name_node.start_byte : name_node.end_byte
                    ].decode(encoding)
                    param_info["type"] = None
                if value_node:
                    param_info["default"] = content[
                        value_node.start_byte : value_node.end_byte
                    ].decode(encoding)

            elif child.type == "typed_default_parameter":
                name_node = child.child_by_field_name("name")
                type_node = child.child_by_field_name("type")
                value_node = child.child_by_field_name("value")
                if name_node:
                    param_info["name"] = content[
                        name_node.start_byte : name_node.end_byte
                    ].decode(encoding)
                if type_node:
                    param_info["type"] = content[
                        type_node.start_byte : type_node.end_byte
                    ].decode(encoding)
                if value_node:
                    param_info["default"] = content[
                        value_node.start_byte : value_node.end_byte
                    ].decode(encoding)

            if param_info.get("name") and param_info["name"] not in ["self", "cls"]:
                params.append(param_info)

        return params
