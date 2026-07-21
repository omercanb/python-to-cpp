from mypy.nodes import CallExpr, ComparisonExpr
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import (
    FloatExpr,
    IndexExpr,
    IntExpr,
    ListExpr,
    MemberExpr,
    NameExpr,
    OpExpr,
    StrExpr,
    UnaryExpr,
)
from mypy.types import Type
from mypy.visitor import ExpressionVisitor

from python.codegen.builtins import is_builtin_with_kwargs
from python.codegen.codegen_utils import list_of
from python.codegen.translation_utils import (
    should_translate_kwargs,
    translate_arguments_with_kwargs,
    translate_builtin_function_name_to_kwargs,
)


class ExpressionCodegen(ExpressionVisitor[str]):
    """Generate C++ code for expressions."""

    def __init__(self, types_dict: dict[MypyExpression, Type]):
        self.types = types_dict

    def visit_name_expr(self, o: NameExpr) -> str:
        return o.name

    def visit_member_expr(self, o: MemberExpr) -> str:
        """Handle attribute access considering whether the object will be a pointer or value"""
        # TODO: Handle attribute access
        obj = o.expr.accept(self)
        return f"{obj}.{o.name}"

    def visit_call_expr(self, o: CallExpr) -> str:
        callee = o.callee.accept(self)

        # Handle special case for builtins with kwargs (like print)
        if should_translate_kwargs(o):
            arguments = translate_arguments_with_kwargs(o, self)
            callee = translate_builtin_function_name_to_kwargs(o)
        else:
            arguments = [arg.accept(self) for arg in o.args]

        return f"{callee}({', '.join(arguments)})"

    def visit_op_expr(self, o: OpExpr) -> str:
        left = o.left.accept(self)
        right = o.right.accept(self)
        return f"({left} {o.op} {right})"

    def visit_unary_expr(self, o: UnaryExpr) -> str:
        operand = o.expr.accept(self)
        return f"{o.op}{operand}"

    def visit_index_expr(self, o: IndexExpr) -> str:
        base = o.base.accept(self)
        index = o.index.accept(self)
        return f"{base}[{index}]"

    def visit_comparison_expr(self, o: ComparisonExpr) -> str:
        # TODO: Generate comparison
        return "comparison"

    def visit_int_expr(self, o: IntExpr) -> str:
        return str(o.value)

    def visit_str_expr(self, o: StrExpr) -> str:
        return f'"{o.value}"'

    def visit_float_expr(self, o: FloatExpr) -> str:
        return str(o.value)

    def visit_list_expr(self, o: ListExpr) -> str:
        elements = [element.accept(self) for element in o.items]
        return list_of(elements)
