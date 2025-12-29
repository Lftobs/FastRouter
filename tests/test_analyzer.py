import pytest
from pathlib import Path
from fast_router.analyzer import StaticAnalyzer


@pytest.fixture
def analyzer():
    return StaticAnalyzer()


def test_analyze_basic_methods(analyzer, tmp_path):
    content = """
def get(): return {"m": "get"}
def post(): return {"m": "post"}
def other(): pass
def _hello(): return {"m": "hello"}
"""
    f = tmp_path / "route.py"
    f.write_text(content)

    analysis = analyzer.analyze_file(f)
    handlers = analysis["handlers"]
    stray = analysis["stray_functions"]

    assert "GET" in handlers
    assert "POST" in handlers
    assert "OTHER" not in handlers
    assert "other" in stray
    assert "_hello" not in stray


def test_analyze_async_methods(analyzer, tmp_path):
    content = """
async def get(): return {"m": "get"}
def post(): return {"m": "post"}
"""
    f = tmp_path / "route.py"
    f.write_text(content)

    analysis = analyzer.analyze_file(f)
    handlers = analysis["handlers"]
    assert handlers["GET"]["is_async"] is True
    assert handlers["POST"]["is_async"] is False


def test_analyze_parameters(analyzer, tmp_path):
    content = """
def get(id: int, name, q: str = "test"):
    pass
"""
    f = tmp_path / "route.py"
    f.write_text(content)

    analysis = analyzer.analyze_file(f)
    handlers = analysis["handlers"]
    params = handlers["GET"]["params"]
    assert len(params) == 3
    assert params[0] == {"name": "id", "type": "int"}
    assert params[1] == {"name": "name", "type": None}
    assert params[2] == {"name": "q", "type": "str", "default": '"test"'}


def test_analyze_docstring(analyzer, tmp_path):
    content = """
def get():
    \"\"\"This is a docstring.\"\"\"
    return {}
"""
    f = tmp_path / "route.py"
    f.write_text(content)
    analysis = analyzer.analyze_file(f)
    assert analysis["handlers"]["GET"]["docstring"] == "This is a docstring."


def test_analyze_non_existent_file(analyzer):
    analysis = analyzer.analyze_file(Path("non_existent.py"))
    assert analysis["handlers"] == {}
    assert analysis["stray_functions"] == []


def test_analyze_malformed_file(analyzer, tmp_path):
    content = "def get(:"
    f = tmp_path / "route.py"
    f.write_text(content)

    analysis = analyzer.analyze_file(f)
    assert isinstance(analysis["handlers"], dict)
    assert isinstance(analysis["stray_functions"], list)


def test_analyzer_respects_latin1_encoding(analyzer, tmp_path):
    """Test that the analyzer respects PEP 263 encoding declarations."""
    route_file = tmp_path / "route.py"
    latin1_content = (
        b"# -*- coding: latin-1 -*-\n"
        b"def get():\n"
        b'    """\xc9t\xe9 docstring"""\n'
        b'    return {"status": "ok"}\n'
    )
    route_file.write_bytes(latin1_content)

    analysis = analyzer.analyze_file(route_file)

    assert "GET" in analysis["handlers"]
    handler = analysis["handlers"]["GET"]
    assert handler["name"] == "get"
    assert handler["docstring"] == "Été docstring"


def test_analyzer_respects_utf8_with_bom(analyzer, tmp_path):
    """Test that the analyzer handles UTF-8 with BOM."""
    route_file = tmp_path / "route.py"
    utf8_bom_content = (
        b"\xef\xbb\xbf"
        b"# -*- coding: utf-8 -*-\n"
        b"def post():\n"
        b'    """Caf\xc3\xa9 docstring"""\n'
        b'    return {"status": "ok"}\n'
    )
    route_file.write_bytes(utf8_bom_content)

    analysis = analyzer.analyze_file(route_file)

    assert "POST" in analysis["handlers"]
    handler = analysis["handlers"]["POST"]
    assert handler["docstring"] == "Café docstring"


def test_analyzer_with_iso_8859_15_encoding(analyzer, tmp_path):
    """Test that the analyzer handles ISO-8859-15 encoding."""
    route_file = tmp_path / "route.py"
    iso_content = (
        b"# -*- coding: iso-8859-15 -*-\n"
        b"def delete(price: int = 100):\n"
        b'    """Price in \xa4"""\n'
        b'    return {"price": price}\n'
    )
    route_file.write_bytes(iso_content)

    analysis = analyzer.analyze_file(route_file)

    assert "DELETE" in analysis["handlers"]
    handler = analysis["handlers"]["DELETE"]
    assert handler["name"] == "delete"
    assert len(handler["params"]) == 1
    assert handler["params"][0]["name"] == "price"
    assert handler["docstring"] == "Price in €"
