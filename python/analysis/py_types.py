from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from python.analysis.ptypes.py_builtins import (
    PyType,
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
    node: ast.AST | None


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


@dataclass
class ListType(ClassType):
    element_type: PyType = builtin_int


def create_list_type(element_type: PyType) -> ListType:
    list_type = ListType("list", element_type=element_type, get_item_type=element_type)
    methods = list_methods(element_type, list_type)
    list_type.methods = methods
    return list_type


def list_methods(element_type, list_type_instance) -> list[MethodType]:
    T = element_type
    none = builtins_map["None"]

    def method(name, argument_types, return_type):
        return MethodType(list_type_instance, name, argument_types, return_type, None)

    return [
        method("append", [T], none),
        method("extend", [list_type_instance], none),
        method("insert", [builtin_int, T], none),
        method("remove", [T], none),
        method("pop", [], T),
        method("index", [T], builtin_int),
        method("count", [T], builtin_int),
        method("clear", [], none),
        method("copy", [], list_type_instance),
        method("reverse", [], none),
        method("sort", [], none),
    ]


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
