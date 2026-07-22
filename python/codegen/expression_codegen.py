from mypy.nodes import CallExpr, ComparisonExpr, DictExpr
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
    SetExpr,
    StrExpr,
    TupleExpr,
    UnaryExpr,
)
from mypy.types import Type
from mypy.visitor import ExpressionVisitor

from python.codegen.codegen_utils import list_of, pointer_to
from python.codegen.translation_utils import (
    call_method,
    is_truthy,
    member_access,
    should_translate_kwargs,
    should_wrap_call_in_pointer,
    translate_arguments_with_kwargs,
    translate_binary_expr,
    translate_builtin_function_name_to_kwargs,
    translate_comparison,
    translate_constructor,
    translate_constructor_special_cases,
    translate_lambda_parameters,
    translate_method_name,
    translate_parameters,
)
from python.codegen.typegen import is_pointer


class ExpressionCodegen(ExpressionVisitor[str]):
    """Generate C++ code for expressions."""

    def __init__(self, types_dict: dict[MypyExpression, Type]):
        self.types = types_dict
        # Keeps track of wether the current expression is an lvalue
        # Set from outside the class
        self.lvalue = False

    def visit_name_expr(self, o: NameExpr) -> str:
        if o.fullname == "builtins.True":
            return "true"
        if o.fullname == "builtins.False":
            return "false"
        return o.name

    def visit_member_expr(self, o: MemberExpr) -> str:
        """Handle attribute access considering whether the object will be a pointer or value"""
        # TODO: Handle attribute access
        obj = o.expr.accept(self)
        name = translate_method_name(o.name)
        return member_access(obj, self.types[o.expr], name)

    def visit_call_expr(self, o: CallExpr) -> str:
        callee = o.callee.accept(self)

        # Handle special case for builtins with kwargs (like print)
        if should_translate_kwargs(o):
            arguments = translate_arguments_with_kwargs(o, self)
            callee = translate_builtin_function_name_to_kwargs(o)
        else:
            arguments = [arg.accept(self) for arg in o.args]

        argument_list = ", ".join(arguments)
        special_case = translate_constructor_special_cases(o.callee)
        if special_case:
            callee = special_case

        call = f"{callee}({', '.join(arguments)})"
        if should_wrap_call_in_pointer(o.callee):
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
        return f"[]({', '.join(arguments)}) {{ return {body}; }}"

    def visit_op_expr(self, o: OpExpr) -> str:
        left = o.left.accept(self)
        right = o.right.accept(self)
        return translate_binary_expr(o.op, left, right)

    def visit_unary_expr(self, o: UnaryExpr) -> str:
        operand = o.expr.accept(self)
        if o.op == "not":
            return f"!{is_truthy(operand)}"
        return f"{o.op}{operand}"

    def visit_index_expr(self, o: IndexExpr) -> str:
        base = o.base.accept(self)
        index = o.index.accept(self)
        return call_method(base, self.types[o.base], "__getitem__", index)

    def visit_set_expr(self, o: SetExpr) -> str:
        elements = [item.accept(self) for item in o.items]
        constructor = f"{{{', '.join(elements)}}}" if elements else ""
        return translate_constructor(self.types[o], constructor)

    def visit_dict_expr(self, o: DictExpr) -> str:
        pairs = []
        for key, value in o.items:
            assert key is not None, "dict unpacking (**) is not supported"
            pairs.append(f"{{{key.accept(self)}, {value.accept(self)}}}")
        constructor = f"{{{', '.join(pairs)}}}" if pairs else ""
        return translate_constructor(self.types[o], constructor)

    def visit_comparison_expr(self, o: ComparisonExpr) -> str:
        return translate_comparison(o, self)

    def visit_int_expr(self, o: IntExpr) -> str:
        return f"{str(o.value)}LL"

    def visit_str_expr(self, o: StrExpr) -> str:
        # Wrapped in str(...) so literals carry the string methods, like
        # Python. repr() escapes newlines; its quotes are stripped.
        return f'str("{repr(o.value)[1:-1]}")'

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
