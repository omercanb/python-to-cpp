from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass
from typing import TYPE_CHECKING

from errors import PyToCppError

if TYPE_CHECKING:
    from name_resolution import BindingTable
    from scope import Scope

type TypeTable = dict[ast.AST, FunctionType | ClassType]


class PyType:
    pass


@dataclass
class BuiltinType(PyType):
    builtin: type


builtins_map = {
    builtin_name: BuiltinType(getattr(builtins, builtin_name))
    for builtin_name in dir(builtins)
}


# A slice type like list[int] or dict[int, str]
@dataclass
class SliceType(PyType):
    base: PyType
    slice: list[PyType]


@dataclass
class FunctionType(PyType):
    name: str
    node: ast.FunctionDef
    argument_types: list[PyType]
    return_type: PyType

    def __init__(self, node: ast.FunctionDef, bindings: BindingTable, types: TypeTable):
        """Creates the function with just the name and the types will be filled out later"""
        self.name = node.name
        self.node = node
        self.argument_types, self.return_type = get_function_type(
            self.node, bindings, types, is_method=False
        )


class MethodType(PyType):
    class_type: ClassType
    name: str
    node: ast.FunctionDef
    argument_types: list[PyType]
    return_type: PyType

    def __init__(
        self,
        class_type: ClassType,
        node: ast.FunctionDef,
        bindings: BindingTable,
        types: TypeTable,
    ):
        """Creates the function with just the name and the types will be filled out later"""
        self.class_type = class_type
        self.name = node.name
        self.node = node
        self.add_type(bindings, types)

    def add_type(self, bindings: BindingTable, types: TypeTable):
        self.argument_types, self.return_type = get_function_type(
            self.node, bindings, types, is_method=True
        )


def get_function_type(
    node: ast.FunctionDef,
    bindings: BindingTable,
    types: TypeTable,
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


@dataclass
class ClassType(PyType):

    node: ast.ClassDef
    name: str
    constructor: MethodType | None
    methods: list[MethodType]
    fields: dict[str, PyType]

    def __init__(
        self, node: ast.ClassDef, scope: Scope, node_scopes: dict[ast.AST, Scope]
    ):
        """Creates the function with just the name and the types will be filled out later"""
        self.node = node
        self.name = node.name
        self.constructor = None
        self.methods = []
        self.fields = {}
        self.node_scopes = node_scopes
        self.scope = scope

    def add_type(self, bindings: BindingTable, types: TypeTable):
        for child in ast.walk(self.node):
            match child:
                case ast.FunctionDef():
                    # Check that we are not in a nested scope
                    if self.node_scopes[child] != self.scope:
                        continue
                    method = MethodType(self, child, bindings, types)
                    if method.name == "__init__":
                        assert self.constructor == None
                        self.constructor = method
                        self.set_fields_from_init(child, method)
                    else:
                        self.methods.append(method)

    def set_fields_from_init(self, node: ast.FunctionDef, init_method: MethodType):
        # Create a map of argument name to it's type in the annotation
        argument_type_map = {}
        for argument, argument_type in zip(
            # Skipping the first argument
            node.args.args[1:],
            init_method.argument_types,
        ):
            argument_type_map[argument.arg] = argument_type
        # Gets the first argument of the init method
        self_argument_name = node.args.args[0].arg
        for child in ast.walk(node):
            match child:
                # Matches self.x = y
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
                    if id == self_argument_name:
                        type = argument_type_map[argument_name]
                        self.fields[field_name] = type


def type_of_annotation(
    annotation: ast.AST, bindings: BindingTable, types: TypeTable
) -> PyType:
    match annotation:
        case ast.Constant():
            assert annotation.value == None
            return builtins_map["None"]
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
