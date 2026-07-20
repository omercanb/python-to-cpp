"""Codegen for functions and classes"""

from mypy.nodes import FuncDef
from mypy.types import CallableType, get_proper_type
from mypy.visitor import ExpressionVisitor

from python.codegen.mypy_codegen import cpp_type


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


def generate_func_signature(o: FuncDef, expr_translator: ExpressionVisitor[str]) -> str:
    """Generate a C++ function signature"""
    func = get_function_type(o)
    return_type = cpp_type(func.ret_type)
    name = o.name
    arguments = generate_arguments(o, expr_translator)
    signature = f"{return_type} {name}({', '.join(arguments)})"
    return signature


def generate_arguments(
    o: FuncDef, expr_translator: ExpressionVisitor[str]
) -> list[str]:
    func = get_function_type(o)
    arguments: list[str] = []
    for argument, argument_type in zip(o.arguments, func.arg_types):
        argument_name = argument.variable.name
        argument_type_cpp = cpp_type(argument_type)
        if argument.initializer:
            default = argument.initializer.accept(expr_translator)
            s = f"{argument_type_cpp} {argument_name} = {default}"
        else:
            s = f"{argument_type_cpp} {argument_name}"
        arguments.append(s)
    return arguments
