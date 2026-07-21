from mypy.nodes import CallExpr, ComparisonExpr
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import (
    FloatExpr,
    IndexExpr,
    IntExpr,
    LambdaExpr,
    ListExpr,
    Lvalue,
    MemberExpr,
    NameExpr,
    OpExpr,
    ReturnStmt,
    StrExpr,
    TupleExpr,
    UnaryExpr,
)
from mypy.types import Type
from mypy.visitor import ExpressionVisitor

from python.codegen.builtins import is_builtin_with_kwargs
from python.codegen.codegen_utils import list_of, pointer_to
from python.codegen.translation_utils import (
    is_pointer,
    should_translate_kwargs,
    translate_arguments_with_kwargs,
    translate_builtin_function_name_to_kwargs,
    translate_constructor,
    translate_lambda_parameters,
    translate_parameters,
)


class ExpressionCodegen(ExpressionVisitor[str]):
    """Generate C++ code for expressions."""

    def __init__(self, types_dict: dict[MypyExpression, Type]):
        self.types = types_dict
        # Keeps track of wether the current expression is an lvalue
        # Set from outside the class
        self.lvalue = False

    def visit_name_expr(self, o: NameExpr) -> str:
        return o.name

    def visit_member_expr(self, o: MemberExpr) -> str:
        """Handle attribute access considering whether the object will be a pointer or value"""
        # TODO: Handle attribute access
        obj = o.expr.accept(self)
        if is_pointer(self.types[o.expr]):
            return f"{obj}->{o.name}"
        else:
            return f"{obj}.{o.name}"

    def visit_call_expr(self, o: CallExpr) -> str:
        callee = o.callee.accept(self)

        # Handle special case for builtins with kwargs (like print)
        if should_translate_kwargs(o):
            arguments = translate_arguments_with_kwargs(o, self)
            callee = translate_builtin_function_name_to_kwargs(o)
        else:
            arguments = [arg.accept(self) for arg in o.args]

        call = f"{callee}({', '.join(arguments)})"
        if is_pointer(self.types[o]):
            return pointer_to(call)
        else:
            return call

    def visit_lambda_expr(self, o: LambdaExpr) -> str:
        arguments = translate_lambda_parameters(o)
        ret = o.body.body[-1]
        assert isinstance(ret, ReturnStmt)
        expr = ret.expr
        assert expr is not None
        body = expr.accept(self)
        return f"[=]({', '.join(arguments)}) {{ return {body}; }}"

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
        return f'"{repr(o.value)}"'

    def visit_float_expr(self, o: FloatExpr) -> str:
        return str(o.value)

    def visit_list_expr(self, o: ListExpr) -> str:
        assert is_pointer(self.types[o])
        elements = [element.accept(self) for element in o.items]
        if elements:
            constructor = f"{{{', '.join(elements)}}}"
        else:
            constructor = ""
        return translate_constructor(self.types[o], constructor)

    def visit_tuple_expr(self, o: TupleExpr) -> str:
        items = [item.accept(self) for item in o.items]
        if self.lvalue:
            return f"destructure({', '.join(items)})"
        else:
            return f"tuple({', '.join(items)})"
