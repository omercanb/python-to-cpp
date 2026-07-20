"""Test that function signatures are correctly translated to C++."""

import pytest
from mypy.nodes import FuncDef

from main import mypy_pipeline_source
from python.codegen.declarations import generate_func_signature
from python.codegen.mypy_codegen import ExpressionCodegen

# Test Python functions with various signatures
test_code = """
def simple(x: int) -> int:
    return x + 1

def with_defaults(a: int, b: str = "hello", c: float = 3.14) -> str:
    return b

def multiple_params(x: int, y: float, z: bool) -> str:
    return "result"

def no_return() -> None:
    pass

def returns_list(items: list[int]) -> list[str]:
    return ["a", "b"]

def returns_dict(d: dict[str, int]) -> dict[int, str]:
    return {1: "one"}

def no_params() -> int:
    return 42

def with_optional(x: int | None) -> str:
    return "ok"
"""

signatures = {
    "simple": "int simple(int x)",
    "with_defaults": 'std::string with_defaults(int a, std::string b = "hello", double c = 3.14)',
    "multiple_params": "std::string multiple_params(int x, double y, bool z)",
    "no_return": "void no_return()",
    "returns_list": "ptr<list<std::string>> returns_list(ptr<list<int>> items)",
    "returns_dict": "ptr<dict<int, std::string>> returns_dict(ptr<dict<std::string, int>> d)",
    "no_params": "int no_params()",
    "with_optional": "std::string with_optional(std::optional<int> x)",
}


class TestFunctionSignatures:
    """Test C++ function signature generation."""

    @classmethod
    def setup_class(cls):
        result = mypy_pipeline_source(test_code)
        cls.tree = result.tree
        cls.types = result.types

    def generate_signature(self, func_name: str) -> str:
        """Generate C++ signature for a function."""
        sym = self.tree.names.get(func_name)
        assert sym and isinstance(sym.node, FuncDef)
        signature = generate_func_signature(sym.node, ExpressionCodegen(self.types))
        return signature

    @pytest.mark.parametrize("func_name,expected_sig", signatures.items())
    def test_signature(self, func_name, expected_sig):
        """Test function signature."""
        sig = self.generate_signature(func_name)
        assert (
            sig == expected_sig
        ), f"Mismatch for {func_name}:\nGot:      {sig}\nExpected: {expected_sig}"
