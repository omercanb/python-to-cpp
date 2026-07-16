from __future__ import annotations

import ast

from python.analysis.name_resolution import BindingTable
from python.analysis.parse_types import (
    parse_class_stub,
    parse_class_type,
    parse_function,
    type_of_annotation,
)
from python.analysis.py_types import ClassType, TypeTable
from python.analysis.scope import ScopeType, ScopingNodeVisitor


# We have to take a two pass approach to first declare the names of the classes as ptypes
class FunctionAndClassTypeAnnotator(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable, types: TypeTable):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types = types

    def visit_FunctionDef(self, node: ast.FunctionDef):
        scope = self.scope_tracker.node_scopes[node]
        if scope.typ == ScopeType.CLASS:
            return
        self.types[node] = parse_function(node, self.bindings, self.types)
        self.visit(node.body)

    def visit_ClassDef(self, node: ast.ClassDef):
        class_type = self.types[node]
        assert isinstance(class_type, ClassType)
        parse_class_type(class_type, self.bindings, self.types)
        self.visit(node.body)


class ClassTypeDeclarer(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types: TypeTable = {}

    def visit_ClassDef(self, node: ast.ClassDef):
        scope = None
        for stmt in node.body:
            scope = self.node_scopes().get(stmt)
            if scope is not None:
                break
        assert scope is not None
        self.types[node] = parse_class_stub(node, scope, self.node_scopes())
        self.visit(node.body)


# class TypeAnnotator(ScopingNodeVisitor):
#     """Extract and store types from annotations (before inference)"""
#
#     def __init__(self, node_scopes, bindings: BindingTable, types: TypeTable):
#         super().__init__(node_scopes)
#         self.bindings = bindings
#         self.types = types
#
#     def bind_type(self, node: ast.AST, annotation: ast.Name | ast.Subscript):
#         self.types[node]
#
#
#     def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
#         """Handle annotated assignments: x: int = 5"""
#         self.types[node.target] = type_of_annotation(
#             node.annotation, self.bindings, self.types
#         )
#         pass
#
#     def visit_arg(self, node: ast.arg) -> None:
#         """Handle function parameter annotations"""
#         pass
#
#     def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
#         """Handle function return type annotations"""
#         pass
#
#     def visit_ClassDef(self, node: ast.ClassDef) -> None:
#         """Handle class definitions with annotations"""
#         pass
