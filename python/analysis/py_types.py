from __future__ import annotations

import ast
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

from python.analysis.ptypes.py_builtins import (
    BuiltinType,
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
    text: str

    def __init__(self, annotation: ast.expr):
        self.text = ast.unparse(annotation)


class ParamKind(Enum):
    positional_only = auto()  # before /
    positional_or_keyword = auto()
    variable_length_positional = auto()  # *args
    keyword_only = auto()  # after *
    variable_length_keyword = auto()  # **kwargs


@dataclass
class Parameter:
    name: str
    type: PyType | None
    default: ast.expr | None = None
    kind: ParamKind = ParamKind.positional_or_keyword


@dataclass
class SignatureType:
    parameters: list[Parameter]
    return_type: PyType


@dataclass
class FunctionType(PyType):
    name: str
    signature: SignatureType
    node: ast.AST


@dataclass
class MethodType(PyType):
    class_type: ClassType
    name: str
    signature: SignatureType
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


# We currently have no use for parameters of builtins
# _UNSET = object()
#
#
# @dataclass
# class BuiltinParameter:
#     name: str
# type: PyType
#     default: object = _UNSET
#     kind: ParamKind = ParamKind.positional_or_keyword


@dataclass
class BuiltinSignature:
    # We don't check for parameters of builtins
    return_type: PyType


@dataclass
class BuiltinFunctionType(BuiltinType):
    name: str
    signature: BuiltinSignature


@dataclass
class BuiltinMethodType(PyType):
    name: str
    class_type: BuiltinClassType
    signature: BuiltinSignature


@dataclass
class BuiltinClassType(PyType):
    name: str
    methods: list[BuiltinMethodType]
    fields: dict[str, PyType]


class RangeType(PyType):
    pass


@dataclass
class IteratorType(PyType):
    element_type: PyType


builtin_print = BuiltinFunctionType("print", BuiltinSignature(builtin_none))
builtin_len = BuiltinFunctionType("len", BuiltinSignature(builtin_int))
builtin_range = BuiltinFunctionType("range", BuiltinSignature(RangeType()))

builtin_funcs = {
    "print": builtin_print,
    "len": builtin_len,
    "range": builtin_range,
}


def is_object(type: PyType):
    return isinstance(type, ClassType)


class AnnotationError(PyToCppError):
    pass


def resolve_builtin(name: str) -> BuiltinFunctionType:
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
            return base_type.signature.return_type
        case MethodType():
            return base_type.signature.return_type
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
