"""Test that function signatures are correctly translated to C++."""

import pytest
from mypy.nodes import ClassDef, FuncDef, TypeInfo

from main import mypy_pipeline_source
from python.codegen.translation_utils import translate_func_signature
from python.codegen.expression_codegen import ExpressionCodegen

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

def with_object(x: B) -> B:
    return B()

class B:
    pass

class A:
    def method(self, other: int) -> int:
        return 1
"""

function_signatures = {
    "simple": "_int simple(_int x)",
    "with_defaults": 'std::string with_defaults(_int a, std::string b = "hello", _float c = 3.14)',
    "multiple_params": "std::string multiple_params(_int x, _float y, bool z)",
    "no_return": "void no_return()",
    "returns_list": "ptr<list<std::string>> returns_list(ptr<list<_int>> items)",
    "returns_dict": "ptr<dict<_int, std::string>> returns_dict(ptr<dict<std::string, _int>> d)",
    "no_params": "_int no_params()",
    "with_optional": "std::string with_optional(std::optional<_int> x)",
    "with_object": "ptr<B> with_object(ptr<B> x)",
}

class_name = "A"
method_signatures = {"method": "_int method(_int other)"}


class TestFunctionSignatures:
    """Test C++ function signature generation."""

    @classmethod
    def setup_class(cls):
        result = mypy_pipeline_source(test_code)
        cls.tree = result.tree
        cls.types = result.types
        cls.expr_translator = ExpressionCodegen(result.types)

    def generate_function_signature(self, func_name: str) -> str:
        """Generate C++ signature for a function."""
        sym = self.tree.names.get(func_name)
        assert sym and isinstance(sym.node, FuncDef)
        signature = translate_func_signature(sym.node, self.expr_translator)
        return signature

    def generate_method_signature(self, method_name: str, class_name: str) -> str:
        class_info = self.tree.names.get(class_name)
        assert class_info and isinstance(class_info.node, TypeInfo)
        method = class_info.node.names[method_name].node
        assert isinstance(method, FuncDef)
        signature = translate_func_signature(method, self.expr_translator)
        return signature

    @pytest.mark.parametrize("func_name,expected_sig", function_signatures.items())
    def test_func_signature(self, func_name, expected_sig):
        """Test function signature."""
        sig = self.generate_function_signature(func_name)
        assert (
            sig == expected_sig
        ), f"Mismatch for {func_name}:\nGot:      {sig}\nExpected: {expected_sig}"

    @pytest.mark.parametrize("func_name,expected_sig", method_signatures.items())
    def test_method_signature(self, func_name, expected_sig):
        """Test method signature."""
        sig = self.generate_method_signature(func_name, class_name)
        assert (
            sig == expected_sig
        ), f"Mismatch for {func_name}:\nGot:      {sig}\nExpected: {expected_sig}"
