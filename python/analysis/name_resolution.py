"""Resolve names (including type annotations) to their declarations or Builtins"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING

from python.analysis.ptypes.py_builtins import builtins_map
from python.analysis.scope import ScopingNodeVisitor
from python.errors import PyToCppError

if TYPE_CHECKING:
    from .scope import Scope

type BindingTable = dict[ast.Name, Binding]


@dataclass
class Binding:
    node: ast.AST
    is_annotation: bool = False


class NameType(Enum):
    reference = auto()
    declaration = auto()
    builtin = auto()
    annotation = auto()


def get_declaration(node: ast.Name, bindings: BindingTable) -> ast.AST:
    assert node in bindings
    return bindings[node].node


def get_name_type(node: ast.Name, bindings: BindingTable):
    binding = bindings.get(node)
    if binding is not None:
        # If the node has a binding but it points to itself thats a declaration and the type is still unkown
        if binding.is_annotation:
            return NameType.annotation
        if binding.node == node:
            return NameType.declaration
        else:
            return NameType.reference
    else:
        return NameType.builtin


def is_declaration(node: ast.Name, bindings: BindingTable):
    # If the node has a binding but it points to itself thats a declaration and the type is still unkown
    binding = bindings.get(node)
    if binding is None:
        return False
    if binding.node == node:
        return True
    else:
        return False


class ResolutionError(PyToCppError):
    def __init__(self, node):
        message = "Name could not be found"
        super().__init__(node, message)


class NameResolver(ScopingNodeVisitor):

    def __init__(self, node_scopes):
        super().__init__(node_scopes)
        self.bindings: BindingTable = {}
        self.annotations: set[ast.expr] = set()

    def resolve_builtin(self, name: str):
        return builtins_map.get(name, None)

    def bind_node(self, node: ast.Name, other_node: ast.AST):
        assert node not in self.bindings
        self.bindings[node] = Binding(other_node)

    def node_is_annotation(self, node: ast.Name):
        self.bindings[node] = Binding(node, True)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.visit(node.target)
        if node.value:
            self.visit(node.value)
        self.annotations.add(node.annotation)

    def visit_arg(self, node: ast.arg):
        if node.annotation:
            self.annotations.add(node.annotation)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.returns:
            self.annotations.add(node.returns)
        self.visit(node.args)
        self.visit(node.body)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.resolve_name_load(node, self.scope())
        elif isinstance(node.ctx, ast.Store):
            self.resolve_name_store(node, self.scope())
        # Del and other contexts: ignored for now

    def visit_AugAssign(self, node: ast.AugAssign):
        self.visit(node.value)
        if isinstance(node.target, ast.Name):
            self.resolve_name_store(node.target, self.scope())
        else:
            self.visit(node.target)

    def resolve_name_store(self, node: ast.Name, scope: Scope):
        # Check if trying to assign to a builtin
        if node.id in builtins_map:
            raise PyToCppError(node, f"cannot assign to builtin '{node.id}'")

        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            _, declaration_node = result
            self.bind_node(node, declaration_node)
            return

        # Name doesn't exist yet - it's a new declaration
        self.bind_node(node, node)

    def resolve_name_load(self, node: ast.Name, scope: Scope):
        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            _, declaration_node = result
            self.bind_node(node, declaration_node)
            return

        builtin = self.resolve_builtin(node.id)
        if builtin is None:
            raise ResolutionError(node)
