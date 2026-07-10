"""
Resolve names (including type annotations) to their declarations or Builtins
"""

from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from errors import PyToCppError
from py_types import BuiltinType, builtins_map
from scope import ScopingNodeVisitor

if TYPE_CHECKING:
    from scope import Scope

type BindingTable = dict[ast.Name, Binding]


@dataclass
class Binding:
    node: ast.AST | None


class ResolutionError(PyToCppError):
    def __init__(self, node):
        message = "Name could not be found"
        super().__init__(node, message)


class NameResolver(ScopingNodeVisitor):
    def __init__(self, node_scopes):
        super().__init__(node_scopes)
        self.bindings: BindingTable = {}

    def resolve_builtin(self, name: str):
        return builtins_map.get(name, None)

    def bind_node(self, node: ast.Name, thing: Binding):
        assert node not in self.bindings
        self.bindings[node] = thing

    def visit_arg(self, node: ast.arg):
        if node.annotation is not None:
            assert isinstance(node.annotation, ast.Name)
            enclosing_scope = self.scope().enclosing
            assert enclosing_scope is not None
            self.resolve_name_load(node.annotation, enclosing_scope)

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
        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            _, declaration_node = result
            binding = Binding(declaration_node)
            self.bind_node(node, binding)
            return

    def resolve_name_load(self, node: ast.Name, scope: Scope):
        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            _, declaration_node = result
            binding = Binding(declaration_node)
            self.bind_node(node, binding)
            return

        builtin = self.resolve_builtin(node.id)
        if builtin is None:
            raise ResolutionError(node)
        else:
            # Resolves but we don't bind it here
            return None
