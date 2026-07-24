"""Class translation from MyPy AST to C++.

A class becomes a plain C++ class, held behind ptr like the other containers,
and its methods stay methods. Nothing special happens for the dunders: the
runtime already dispatches to __str__, __len__ and __bool__ by name, so a
user's class satisfies those protocols the same way list and dict do.

The C++ constructor does no work of its own. It forwards to the __init__ the
user wrote, which is emitted as an ordinary method alongside the rest.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import ClassDef, FuncDef, Var
from mypy.types import Type

from python.codegen.translation_utils import translate_parameters

if TYPE_CHECKING:
    from python.codegen.mypy_codegen import StatementCodegen

INIT = "__init__"


def translate_class_def(codegen: StatementCodegen, class_def: ClassDef) -> None:
    """Emit a C++ class for a Python one."""
    codegen.emit(f"class {class_def.name} {{")
    codegen.emit("  public:")
    codegen.indent()

    write_attributes(codegen, class_def)
    write_constructor(codegen, class_def)
    for method in methods(class_def):
        codegen.visit(method)

    codegen.unindent()
    codegen.emit("};")
    codegen.emit("")


def attributes(class_def: ClassDef) -> list[tuple[str, Type]]:
    """The instance attributes, annotated in the body or assigned in __init__.

    mypy has already inferred the assigned ones, so both arrive here alike.
    """
    return [
        (name, symbol.type)
        for name, symbol in class_def.info.names.items()
        if isinstance(symbol.node, Var) and symbol.type is not None
    ]


def methods(class_def: ClassDef) -> list[FuncDef]:
    """The methods, in the order they were written."""
    return [
        statement
        for statement in class_def.defs.body
        if isinstance(statement, FuncDef)
    ]


def write_attributes(codegen: StatementCodegen, class_def: ClassDef) -> None:
    declared = attributes(class_def)
    for name, attribute_type in declared:
        codegen.emit(codegen.translate_declaration(name, attribute_type))
    if declared:
        codegen.emit("")


def write_constructor(codegen: StatementCodegen, class_def: ClassDef) -> None:
    """A constructor that only forwards to __init__.

    Without an __init__ none is emitted, leaving C++'s implicit default.
    """
    init = next((method for method in methods(class_def) if method.name == INIT), None)
    if init is None:
        return

    parameters = translate_parameters(init, codegen.expr_codegen)
    arguments = [
        argument.variable.name
        for argument in init.arguments
        if not argument.variable.is_self
    ]
    codegen.emit(
        f"{class_def.name}({', '.join(parameters)}) "
        f"{{ {INIT}({', '.join(arguments)}); }}"
    )
    codegen.emit("")
