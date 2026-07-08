import ast
from collections import defaultdict
from functools import singledispatch
from types import MethodType
from typing import TYPE_CHECKING

from tabulate import tabulate

from py_types import BuiltinType, ClassType, FunctionType, MethodType, TypeTable

# Utility Functions


def print_indented(indent, *args, **kwargs):
    print(" " * indent, end="")
    print(*args, **kwargs)


def print_dict(d, indent):
    for k, v in d.items():
        print_indented(indent, f"{k}: {v}")


def get_node_name(node: ast.AST) -> str | None:
    name_fields = ["name", "id", "arg"]
    name = None
    for field in name_fields:
        name = getattr(node, field, None)
        if name is not None:
            break
    return name


# Scopes


def get_scope_identifier(scope) -> str:
    return f"{scope.typ.name} {scope.name or ''}"


def print_scope_structure(scope, indent=0):
    if indent == 0:
        print("Scope Structure")
    print(f"{" "*indent} {scope.typ.name.title()} {scope.name or ""}")
    for child in scope.children:
        child.print_scope_structure(indent + 4)


# Scope Maps


def print_scopes_by_line(node_scopes):
    print("Scopes By Line")
    prev_line = None
    for node, scope in node_scopes.items():
        cur_line = getattr(node, "lineno", None)
        if cur_line == None:
            continue
        if prev_line != cur_line:
            print(f'line {cur_line}: {scope.typ.name.title()} {scope.name or ""}')
        prev_line = cur_line


def print_scopes_of_all_symbols(node_scopes):
    print("Scopes of All Symbols")
    headers = [
        "Line",
        "Node",
        "Scope",
    ]
    data = defaultdict(list)
    for node, scope in node_scopes.items():
        line = getattr(node, "lineno", None)
        data["line"].append(line)

        name = get_node_name(node)
        data["node"].append(f'{type(node).__name__} {name or ""}')

        data["scope"].append(f'{scope.typ.name.title()} {scope.name or ""}')
    print(tabulate(data, headers))


# Name Resolution


def print_scope_rec(scope, indent=0):
    print_indented(indent, scope.typ, scope.name)
    print_indented(indent, "definitions {")
    print_dict(scope.definitions, indent)
    print_indented(indent, "}")
    if scope.nonlocal_vars:
        print_indented(indent, f"nonlocals: {scope.nonlocal_vars}")
    if scope.global_vars:
        print_indented(indent, f"globals: {scope.global_vars}")
    print_indented(indent, "child scopes {")
    for child in scope.children:
        child.print_tree(indent + 4)
    print_indented(indent, "}")


def print_scope(scope, indent=0):
    print_indented(indent, scope.typ, scope.name)
    print_indented(indent, "definitions {")
    print_dict(scope.definitions, indent)
    if scope.nonlocal_vars:
        print_indented(indent, f"nonlocals: {scope.nonlocal_vars}")
    if scope.global_vars:
        print_indented(indent, f"globals: {scope.global_vars}")
    print_indented(indent, "}")


# Class and Function Declarations


def print_type_table(types: TypeTable):
    s = "Classes and Functions\n\n"
    for node, typ in types.items():
        s += format_type(typ)
        s += "\n"
    print(s)


@singledispatch
def get_type_name(_) -> str:
    return ""


@get_type_name.register
def _(typ: FunctionType):
    return typ.name


@get_type_name.register
def _(typ: ClassType):
    return typ.name


@get_type_name.register
def _(typ: BuiltinType):
    if typ.builtin is None:
        return "None"
    return typ.builtin.__name__


@singledispatch
def format_type(_) -> str:
    return ""


@format_type.register
def _(fun: FunctionType):
    s = f"Function {fun.name}("

    s += ", ".join((get_type_name(typ) for typ in fun.argument_types))
    s += f") -> {get_type_name(fun.return_type)}"
    return s


@format_type.register
def _(fun: MethodType):
    s = f"{fun.name}("

    s += ", ".join((get_type_name(typ) for typ in fun.argument_types))
    s += f") -> {get_type_name(fun.return_type)}"
    return s


@format_type.register
def _(cls: ClassType):
    s = f"Class {cls.name}\n"
    for field, typ in cls.fields.items():
        s += f"    {field}: {get_type_name(typ)}\n"
    for method in cls.methods:
        s += f"    {format_type(method)}\n"
    return s
