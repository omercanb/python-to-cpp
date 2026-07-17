from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from python.analysis.ptypes.py_builtins import (
    ContainerType,
    PyType,
    UnknownType,
    builtin_int,
    builtin_none,
    builtins_map,
)
from python.errors import PyToCppError

if TYPE_CHECKING:
    from .scope import Scope

type TypeTable = dict[ast.AST, PyType]


@dataclass
class AnnotationType(PyType):
    name: str


@dataclass
class FunctionType(PyType):
    name: str
    argument_types: list[PyType]
    return_type: PyType
    node: ast.AST | None


@dataclass
class MethodType(PyType):
    class_type: ClassType
    name: str
    argument_types: list[PyType]
    return_type: PyType
    node: ast.AST


@dataclass
class ClassType(PyType):
    name: str
    constructor: MethodType | None = None
    methods: list[MethodType] = field(default_factory=list)
    fields: dict[str, PyType] = field(default_factory=dict)
    node: ast.ClassDef | None = None
    scope: Scope | None = None
    node_scopes: dict[ast.AST, Scope] | None = None
    get_item_type: PyType | None = None


class BuiltinClassType(PyType):
    name: str
    methods: list[BuiltinMethodType]
    fields: dict[str, PyType]


class BuiltinMethodType(PyType):
    class_type: BuiltinClassType
    name: str
    argument_types: list[PyType]
    return_type: PyType


class RangeType(PyType):
    pass


@dataclass
class IteratorType(PyType):
    element_type: PyType


builtin_print = FunctionType("print", [], builtin_none, None)
builtin_len = FunctionType("len", [], builtin_int, None)
builtin_range = FunctionType("range", [], RangeType(), None)
builtin_funcs = {
    "print": builtin_print,
    "len": builtin_len,
    "range": builtin_range,
}


def is_object(type: PyType):
    return isinstance(type, ClassType)


class AnnotationError(PyToCppError):
    pass


def resolve_builtin(name: str) -> FunctionType:
    assert name in builtin_funcs
    return builtin_funcs[name]


def get_attribute_type(base_type: PyType, attribute: str) -> PyType:
    match base_type:
        case ClassType():
            return get_class_attribute_type(base_type, attribute)
        case ContainerType():
            return get_container_attribute_type(base_type, attribute)
        case _:
            raise NotImplementedError(f"Can't convert {base_type}")


def get_class_attribute_type(class_type: ClassType, attribute: str) -> PyType:
    typ = None
    for method in class_type.methods:
        if method.name == attribute:
            typ = method
            break
    if typ is None:
        typ = class_type.fields.get(attribute)
    if typ is None:
        raise PyToCppError(
            class_type.node, f"No field {attribute} on class {class_type.name}"
        )
    return typ


def get_container_attribute_type(
    continer_type: ContainerType, attribute: str
) -> PyType:
    """Returns a placeholder type since call return types for builtin containers are determined later"""
    return UnknownType()


def get_call_type(base_type):
    match base_type:
        case FunctionType():
            return base_type.return_type
        case MethodType():
            return base_type.return_type
        case ClassType():
            return base_type
        case _:
            raise NotImplementedError()


class ListType(BuiltinClassType):
    def __init__(self, element_type: PyType):
        self.name = "list"
        self.element_type = element_type
        methods = [
            ("append", element_type, builtin_none),
            ("pop", builtin_int, builtin_none),
        ]

    # def assign_methods(self, element_type: PyType):
    #     methods = [
    #         ("append", element_type, builtin_none),
    #         ("pop", builtin_int, builtin_none),
    #         ("extend", self, self),
    #         ("remove", element_type, builtin_none),
    #         ("pop", )
    #     ]
