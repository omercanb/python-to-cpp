from __future__ import annotations

import ast

from python.analysis.name_resolution import BindingTable
from python.analysis.ptypes.py_builtins import UnknownType, builtin_none, builtins_map
from python.analysis.py_types import (
    AnnotationError,
    AnnotationType,
    ClassType,
    FunctionType,
    ListType,
    MethodType,
    Parameter,
    ParamKind,
    PyType,
    SignatureType,
    TypeTable,
)
from python.analysis.scope import Scope
from python.errors import PyToCppError
from python.utils import dump


def parse_function(
    node: ast.FunctionDef, bindings: BindingTable, types: TypeTable
) -> FunctionType:

    signature = get_function_type(node, bindings, types)
    return FunctionType(node.name, signature, node)


def parse_method(
    class_type: ClassType,
    node: ast.FunctionDef,
    bindings: BindingTable,
    types: TypeTable,
) -> MethodType:

    signature = get_function_type(node, bindings, types)
    return MethodType(class_type, node.name, signature, node)


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
) -> SignatureType:
    parameters = get_parameter_list(node.args, bindings, types)
    if node.returns is None:
        return_type = UnknownType()
    else:
        return_type = type_of_annotation(node.returns, bindings, types)
    return SignatureType(parameters, return_type)


def get_parameter_list(
    parameters: ast.arguments, bindings: BindingTable, types: TypeTable
):
    """Parses the parameter list into a more easy to use type"""
    defaults = _get_parameter_defaults(parameters)

    parameter_kinds: list[tuple[list[ast.arg], ParamKind]] = [
        (parameters.posonlyargs, ParamKind.positional_only),
        (parameters.args, ParamKind.positional_or_keyword),
        (parameters.kwonlyargs, ParamKind.keyword_only),
    ]
    if parameters.vararg is not None:
        parameter_kinds.append(
            ([parameters.vararg], ParamKind.variable_length_positional)
        )
    if parameters.kwarg is not None:
        parameter_kinds.append(([parameters.kwarg], ParamKind.variable_length_keyword))

    parsed_parameters = []
    for parameter_list, parameter_kind in parameter_kinds:
        for parameter in parameter_list:
            if parameter.annotation is None:
                parameter_type = None
            else:
                parameter_type = type_of_annotation(
                    parameter.annotation, bindings, types
                )
            default = defaults.get(parameter.arg)
            parsed_parameters.append(
                Parameter(parameter.arg, parameter_type, default, parameter_kind)
            )
    return parsed_parameters


def _get_parameter_defaults(parameters: ast.arguments) -> dict[str, ast.expr]:
    # Rules for parameter defaults
    # https://docs.python.org/3/library/ast.html#ast.arguments
    defaults = {}
    for parameter, default in zip(reversed(parameters.args), parameters.defaults):
        defaults[parameter.arg] = default
    for kw_parameter, default in zip(parameters.kwonlyargs, parameters.kw_defaults):
        if default is None:
            continue
        defaults[kw_parameter.arg] = default
    return defaults


def type_of_annotation(
    annotation: ast.expr, bindings: BindingTable, types: TypeTable
) -> PyType:
    match annotation:
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
            return type_of_container_annotation(annotation, bindings, types)
    raise PyToCppError(annotation, "Unkown annotation type")


def type_of_container_annotation(
    annotation: ast.Subscript, bindings: BindingTable, types: TypeTable
):
    if not isinstance(annotation.value, ast.Name):
        raise PyToCppError(annotation, "Can't convert annotation")
    match annotation.slice:
        case ast.Name() as name:
            elements = [type_of_annotation(name, bindings, types)]
        case ast.Tuple() as slice:
            elements = [
                type_of_annotation(element, bindings, types) for element in slice.elts
            ]
        case _:
            raise PyToCppError(annotation, "Can't convert annotation")
    match annotation.value.id:
        case "list":
            return ListType(elements[0])
    raise PyToCppError(annotation, "Can't convert annotation")
