from typing import Optional

from mypy.nodes import CallExpr, ComparisonExpr
from mypy.nodes import Expression
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import FuncDef, LambdaExpr, MemberExpr, NameExpr
from mypy.types import CallableType, Instance, ProperType, Type, get_proper_type
from mypy.visitor import ExpressionVisitor, NodeVisitor

from python.codegen.builtins import (
    OP_MAP,
    get_kwarg_defaults,
    get_kwarg_order,
    is_builtin_with_kwargs,
)
from python.codegen.typegen import cpp_type


def get_function_type(func: FuncDef) -> CallableType:
    typ = get_proper_type(func.type)
    assert isinstance(typ, CallableType)
    return typ


def get_argument_names(func: FuncDef) -> list[str]:
    typ = get_function_type(func)
    args = typ.arg_names
    filtered_args: list[str] = []
    for arg in args:
        if arg is None:
            continue
        filtered_args.append(arg)
    return filtered_args


def generate_func_def(o: FuncDef):
    # get signature
    # create block (place for declarations)
    pass


def translate_func_signature(
    o: FuncDef, expr_translator: ExpressionVisitor[str]
) -> str:
    """Generate a C++ function signature"""
    func = get_function_type(o)
    return_type = cpp_type(func.ret_type)
    name = o.name
    arguments = translate_parameters(o, expr_translator)
    signature = f"{return_type} {name}({', '.join(arguments)})"
    return signature


def translate_parameters(
    o: FuncDef, expr_translator: ExpressionVisitor[str]
) -> list[str]:
    func = get_function_type(o)
    arguments: list[str] = []
    for argument, argument_type in zip(o.arguments, func.arg_types):
        if argument.variable.is_self:
            continue
        argument_name = argument.variable.name
        argument_type_cpp = cpp_type(argument_type)
        if argument.initializer:
            default = argument.initializer.accept(expr_translator)
            s = f"{argument_type_cpp} {argument_name} = {default}"
        else:
            s = f"{argument_type_cpp} {argument_name}"
        arguments.append(s)
    return arguments


def translate_lambda_parameters(o: LambdaExpr) -> list[str]:
    params = []
    for argument in o.arguments:
        name = argument.variable.name
        s = f"auto {name}"
        params.append(s)
    return params


def parse_arguments(
    call: CallExpr,
) -> tuple[list[MypyExpression], dict[str, MypyExpression]]:
    positional_args: list[MypyExpression] = []
    kwargs: dict[str, MypyExpression] = {}

    for i, arg in enumerate(call.args):
        arg_name = call.arg_names[i]
        if arg_name is None:
            positional_args.append(arg)
        else:
            kwargs[arg_name] = arg
    return positional_args, kwargs


def has_kwargs(call: CallExpr):
    positional, kwargs = parse_arguments(call)
    if kwargs:
        return True
    else:
        return False


def translate_arguments_with_kwargs(
    call: CallExpr,
    expr_translator: ExpressionVisitor[str],
) -> list[str]:
    """
    Reorder arguments for builtin functions by placing keyword arguments at the front.

    For print(a, b, sep=","), this transforms it to print(",", "\n", a, b)
    where the first two arguments are sep and end.
    """
    assert isinstance(call.callee, NameExpr)

    fullname = call.callee.fullname
    kwarg_names = get_kwarg_order(fullname)
    kwarg_defaults = get_kwarg_defaults(fullname)

    assert kwarg_names is not None, f"No kwarg order defined for {fullname}"
    assert kwarg_defaults is not None, f"No kwarg defaults defined for {fullname}"

    positional_args, kwargs = parse_arguments(call)

    new_args: list[str] = []

    # Add kwargs in the specified order with defaults
    for kwarg_name in kwarg_names:
        if kwarg_name in kwargs:
            new_args.append(kwargs[kwarg_name].accept(expr_translator))
        else:
            default = kwarg_defaults[kwarg_name]
            new_args.append(default.accept(expr_translator))

    # Add positional arguments
    for positional_arg in positional_args:
        new_args.append(positional_arg.accept(expr_translator))

    return new_args


def should_translate_kwargs(call: CallExpr):
    """Returns wether a call is builtin AND uses kwargs"""
    return (
        has_kwargs(call)
        and isinstance(call.callee, NameExpr)
        and is_builtin_with_kwargs(call.callee.fullname)
    )


def translate_builtin_function_name_to_kwargs(o: CallExpr) -> str:
    """Translates the short name of the function, eg: print -> _print_kwargs"""
    assert isinstance(o.callee, NameExpr)
    name = o.callee.name
    return f"_{name}_kwargs"


def translate_callee_special_cases(callee: Expression) -> Optional[str]:
    if not isinstance(callee, NameExpr):
        return
    # If it is a constructor
    if callee.name in ("int", "float"):
        return f"_{callee.name}"

    return


def is_pointer(t: Type):
    t = get_proper_type(t)
    if not isinstance(t, Instance):
        return False
    if t.type.fullname in ["builtins.list"]:
        return True
    return False


def translate_constructor(t: Type, constructor: str):
    typ = cpp_type(t)
    if is_pointer(t):
        return f"ptr(new {typ}({constructor}))"
    else:
        return f"{typ}({constructor})"


def translate_comparison(expr: ComparisonExpr, expr_translator: ExpressionVisitor[str]):
    """Translate a python comparison like a < b < c into a < b && b < c"""
    pairwise_comparisons = expr.pairwise()
    terms = []  # Individual comaprisons to be connected by 'and'
    for op, expr1, expr2 in pairwise_comparisons:
        expr1 = expr1.accept(expr_translator)
        expr2 = expr2.accept(expr_translator)
        terms.append(translate_binary_expr(op, expr1, expr2))
    full_comparison = " && ".join(terms)
    return f"({full_comparison})"


def translate_binary_expr(op: str, expr1: str, expr2: str):
    if op in OP_MAP:
        return f"{OP_MAP[op]}({expr1}, {expr2})"
    else:
        return f"({expr1} {op} {expr2})"
