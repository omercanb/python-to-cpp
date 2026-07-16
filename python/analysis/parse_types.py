from __future__ import annotations

import ast

from python.analysis.name_resolution import BindingTable
from python.analysis.ptypes.py_builtins import builtin_none, builtins_map
from python.analysis.py_types import (
    AnnotationError,
    ClassType,
    FunctionType,
    MethodType,
    PyType,
    TypeTable,
    create_list_type,
)
from python.analysis.scope import Scope
from python.errors import PyToCppError


def parse_method(
    class_type: ClassType,
    node: ast.FunctionDef,
    bindings: BindingTable,
    types: TypeTable,
) -> MethodType:

    argument_types, return_type = get_function_type(
        node, bindings, types, is_method=True
    )
    return MethodType(class_type, node.name, argument_types, return_type, node)


def parse_class_stub(
    node: ast.ClassDef, scope: Scope, node_scopes: dict[ast.AST, Scope]
) -> ClassType:
    return ClassType(node.name, None, [], {}, node, scope, node_scopes)


def parse_class_type(stub: ClassType, bindings: BindingTable, types: TypeTable):
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


def parse_function(
    node: ast.FunctionDef, bindings: BindingTable, types: TypeTable
) -> FunctionType:

    argument_types, return_type = get_function_type(
        node, bindings, types, is_method=False
    )
    return FunctionType(node.name, argument_types, return_type, node)


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


def type_of_annotation(
    annotation: ast.AST, bindings: BindingTable, types: TypeTable
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
            return base_type(*slice_types)
    raise PyToCppError(annotation, "Unkown annotation type")
