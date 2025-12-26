import pytest
from pathlib import Path
from file_router.analyzer import StaticAnalyzer


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
