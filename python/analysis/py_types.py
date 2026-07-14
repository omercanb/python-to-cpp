from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..errors import PyToCppError

if TYPE_CHECKING:
    from .name_resolution import BindingTable
    from .scope import Scope

type FunctionAndClassTypeTable = dict[ast.AST, FunctionType | ClassType]

type TypeTable = dict[ast.AST, PyType]


class PyType:
    pass


# Used for empty containers like []
class UnknownType(PyType):
    pass


@dataclass(frozen=True)
class BuiltinType(PyType):
    builtin: type


builtins_map = {
    builtin_name: BuiltinType(getattr(builtins, builtin_name))
    for builtin_name in dir(builtins)
}
builtin_int = builtins_map["int"]
builtin_float = builtins_map["float"]
builtin_bool = builtins_map["bool"]
builtin_str = builtins_map["str"]
builtin_none = builtins_map["None"]

unkown_type = UnknownType()


# A slice type like list[int] or dict[int, str]
@dataclass
class SliceType(PyType):
    base: PyType
    slice: list[PyType]


def parse_function(
    node: ast.FunctionDef, bindings: BindingTable, types: FunctionAndClassTypeTable
) -> FunctionType:

    argument_types, return_type = get_function_type(
        node, bindings, types, is_method=False
    )
    return FunctionType(node.name, argument_types, return_type, node)


@dataclass
class FunctionType(PyType):
    name: str
    argument_types: list[PyType]
    return_type: PyType
    node: ast.AST | None


def parse_method(
    class_type: ClassType,
    node: ast.FunctionDef,
    bindings: BindingTable,
    types: FunctionAndClassTypeTable,
) -> MethodType:

    argument_types, return_type = get_function_type(
        node, bindings, types, is_method=True
    )
    return MethodType(class_type, node.name, argument_types, return_type, node)


@dataclass
class MethodType(PyType):
    class_type: ClassType
    name: str
    argument_types: list[PyType]
    return_type: PyType
    node: ast.AST | None


def get_function_type(
    node: ast.FunctionDef,
    bindings: BindingTable,
    types: FunctionAndClassTypeTable,
    is_method=False,
) -> tuple[list[PyType], PyType]:
    args = node.args.args
    argument_types = []
    for arg in args:
        if is_method and arg == args[0]:  # self argument
            continue
        if arg.annotation is None:
            raise AnnotationError(arg, "Argument needs type annotation")
        argument_types.append(type_of_annotation(arg.annotation, bindings, types))
    if node.returns is None:
        if is_method:
            func_type = "Method"
        else:
            func_type = "Function"
        raise AnnotationError(node, f"{func_type} needs return type annotation")
    return_type = type_of_annotation(node.returns, bindings, types)
    return argument_types, return_type


def parse_class_stub(
    node: ast.ClassDef, scope: Scope, node_scopes: dict[ast.AST, Scope]
) -> ClassType:
    return ClassType(node.name, None, [], {}, node, scope, node_scopes)


def parse_class_type(
    stub: ClassType, bindings: BindingTable, types: FunctionAndClassTypeTable
):
    for child in ast.walk(stub.node):
        match child:
            case ast.FunctionDef():
                # Check that we are not in a nested scope
                if stub.node_scopes[child] != stub.scope:
                    continue
                method = parse_method(stub, child, bindings, types)
                if method.name == "__init__":
                    assert stub.constructor == None
                    stub.constructor = method
                    _parse_class_fields_from_init(stub, child, method)
                else:
                    stub.methods.append(method)


def _parse_class_fields_from_init(stub, node: ast.FunctionDef, init_method: MethodType):
    # Create a map of argument name to it's type in the annotation
    argument_type_map = {}
    for argument, argument_type in zip(
        # Skipping the first argument
        node.args.args[1:],
        init_method.argument_types,
    ):
        argument_type_map[argument.arg] = argument_type
    # Gets the first argument of the init method
    stub_argument_name = node.args.args[0].arg
    for child in ast.walk(node):
        match child:
            # Matches stub.x = y
            case ast.Assign(
                targets=[
                    ast.Attribute(
                        value=ast.Name(id=id, ctx=ast.Load()),
                        attr=field_name,
                        ctx=ast.Store(),
                    )
                ],
                value=ast.Name(id=argument_name, ctx=ast.Load()),
            ):
                if id == stub_argument_name:
                    type = argument_type_map[argument_name]
                    stub.fields[field_name] = type


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
builtin_len = FunctionType("len", [], builtin_none, None)
builtin_range = FunctionType("range", [], IteratorType(builtin_int), None)
builtin_funcs = {
    "print": builtin_print,
    "len": builtin_len,
    "range": builtin_range,
}


def is_object(type: PyType):
    return isinstance(type, ClassType)


def type_of_annotation(
    annotation: ast.AST, bindings: BindingTable, types: FunctionAndClassTypeTable
) -> PyType:
    match annotation:
        case ast.Subscript(value=ast.Name(id), slice=slice):
            slice_type = type_of_annotation(slice, bindings, types)
            if id == "list":
                return create_list_type(slice_type)
        case ast.Constant():
            assert annotation.value == None
            return builtin_none
        case ast.Name():
            if annotation in bindings:
                node = bindings[annotation].node
                if node is not None:
                    return types[node]
            if annotation.id in builtins_map:
                return builtins_map[annotation.id]
        case ast.Subscript():
            base_type = type_of_annotation(annotation.value, bindings, types)
            slice = annotation.slice
            if isinstance(slice, ast.Name):
                slice_types = [type_of_annotation(slice, bindings, types)]
            else:
                assert isinstance(slice, ast.Tuple)
                slice_types = [
                    type_of_annotation(element, bindings, types)
                    for element in slice.elts
                ]
            return SliceType(base_type, slice_types)
    raise PyToCppError(annotation, "Unkown annotation type")


class AnnotationError(PyToCppError):
    pass
