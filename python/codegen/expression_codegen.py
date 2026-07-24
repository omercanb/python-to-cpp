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
    SliceExpr,
    StrExpr,
    TupleExpr,
    UnaryExpr,
)
from mypy.types import TupleType, Type, UnionType, get_proper_type

from python.codegen.codegen_utils import list_of, pointer_to
from python.codegen.translation_utils import (
    call_method,
    is_truthy,
    member_access,
    should_translate_kwargs,
    should_wrap_call_in_pointer,
    translate_arguments_with_kwargs,
    translate_binary_expr,
    translate_bool_op,
    translate_builtin_function_name_to_kwargs,
    translate_comparison,
    translate_constructor,
    translate_constructor_special_cases,
    translate_lambda_parameters,
    translate_method_name,
    translate_parameters,
    translate_tuple_access,
)
from python.codegen.typegen import cpp_type_name, is_pointer
from python.visitor import Visitor


class ExpressionCodegen(Visitor[str]):
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
        obj = self.visit(o.expr)
        name = translate_method_name(o.name)
        return member_access(obj, self.types[o.expr], name)

    def visit_call_expr(self, o: CallExpr) -> str:
        callee = self.visit(o.callee)

        # Handle special case for builtins with kwargs (like print)
        if should_translate_kwargs(o):
            arguments = translate_arguments_with_kwargs(o, self)
            callee = translate_builtin_function_name_to_kwargs(o)
        else:
            arguments = [self.visit(arg) for arg in o.args]

        argument_list = ", ".join(arguments)
        special_case = translate_constructor_special_cases(o.callee)
        if special_case:
            callee = special_case

        if should_wrap_call_in_pointer(o.callee):
            # Spell out the element type: an argument-less list()/set()
            # gives the compiler nothing to deduce it from.
            return translate_constructor(self.types[o], ", ".join(arguments))
        return f"{callee}({', '.join(arguments)})"

    def visit_lambda_expr(self, o: LambdaExpr) -> str:
        arguments = translate_lambda_parameters(o)
        ret = o.body.body[-1]
        assert isinstance(ret, ReturnStmt)
        expr = ret.expr
        assert expr is not None
        body = self.visit(expr)
        return f"[]({', '.join(arguments)}) {{ return {body}; }}"

    def visit_op_expr(self, o: OpExpr) -> str:
        if o.op in ("and", "or"):
            result = get_proper_type(self.types[o])
            if isinstance(result, UnionType):
                assert len({cpp_type_name(i) for i in result.items}) == 1
            return translate_bool_op(o.op, self.visit(o.left), self.visit(o.right))
        left = self.visit(o.left)
        right = self.visit(o.right)
        return translate_binary_expr(o.op, left, right)

    def condition(self, o: MypyExpression) -> str:
        """
        Generate a C++ bool for an expression used as a condition.
        We explicitly convert 'and' and 'or' into && and ||
        """
        if isinstance(o, OpExpr) and o.op in ("and", "or"):
            cpp_op = "&&" if o.op == "and" else "||"
            return f"({self.condition(o.left)} {cpp_op} {self.condition(o.right)})"
        if isinstance(o, UnaryExpr) and o.op == "not":
            return f"(!{self.condition(o.expr)})"
        return is_truthy(self.visit(o))

    def visit_unary_expr(self, o: UnaryExpr) -> str:
        operand = self.visit(o.expr)
        if o.op == "not":
            return f"(!{is_truthy(operand)})"
        return f"({o.op}{operand})"

    def visit_index_expr(self, o: IndexExpr) -> str:
        base = self.visit(o.base)
        base_type = get_proper_type(self.types[o.base])
        if isinstance(base_type, TupleType):
            return translate_tuple_access(base_type, o, base)
        index = self.visit(o.index)
        return call_method(base, base_type, "__getitem__", index)

    def visit_slice_expr(self, o: SliceExpr) -> str:
        """The index of a[i:j:k]. An omitted bound is nullopt, not a default:
        only the container knows what a missing start or stop means."""
        bounds = [
            self.visit(bound) if bound is not None else "std::nullopt"
            for bound in (o.begin_index, o.end_index, o.stride)
        ]
        return f"slice({', '.join(bounds)})"

    def visit_set_expr(self, o: SetExpr) -> str:
        elements = [self.visit(item) for item in o.items]
        constructor = f"{{{', '.join(elements)}}}" if elements else ""
        return translate_constructor(self.types[o], constructor)

    def visit_dict_expr(self, o: DictExpr) -> str:
        pairs = []
        for key, value in o.items:
            assert key is not None
            pairs.append(f"{{{self.visit(key)}, {self.visit(value)}}}")
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
        elements = [self.visit(element) for element in o.items]
        if elements:
            constructor = f"{{{', '.join(elements)}}}"
        else:
            constructor = ""
        return translate_constructor(self.types[o], constructor)

    def visit_tuple_expr(self, o: TupleExpr) -> str:
        items = [self.visit(item) for item in o.items]
        if self.lvalue:
            return f"destructure({', '.join(items)})"
        else:
            return f"tuple({', '.join(items)})"
