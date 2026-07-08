"""
Resolve names (including type annotations) to their declarations or Builtins
"""

from __future__ import annotations

import ast
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

    def print_bindings(self):
        for name, binding in self.bindings.items():
            s = f"binding: line {name.lineno} '{name.id}' resolves to "
            if binding.node is not None:
                s += f"{binding.node}"
                if hasattr(binding.node, "lineno"):
                    s += f" on line {binding.node.lineno}"
            else:
                s += f"builtin {binding}"
            print(s)

    def visit_arg(self, node: ast.arg):
        if node.annotation is not None:
            assert isinstance(node.annotation, ast.Name)
            enclosing_scope = self.scope().enclosing
            assert enclosing_scope is not None
            self.resolve_name(node.annotation, enclosing_scope)

    def visit_Name(self, node: ast.Name):
        self.resolve_name(node, self.scope())

    def resolve_name(self, node: ast.Name, scope: Scope):
        # Only load contexts need resolution
        if not isinstance(node.ctx, ast.Load):
            return
        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            _, declaration_node = result
            binding = Binding(declaration_node)
            self.bind_node(node, binding)
            return
        # The name could be a builtin or be undefined
        # TODO for now we have removed resolving to builtins here
        # But if it can't resolve to a builtin we throw an error
        # builtin = self.resolve_builtin(node.id)
        # if builtin is not None:
        #     binding = Binding(builtin)
        #     self.bind_node(node, binding)
        #     return
        # raise ResolutionError(node)

        builtin = self.resolve_builtin(node.id)
        if builtin is None:
            raise ResolutionError(node)
        else:
            # Resolves but we don't bind it here
            return None
