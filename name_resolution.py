"""
Resolve names (including type annotations) to their declarations or Builtins
"""

import ast
from dataclasses import dataclass
from pprint import pp

from errors import PyToCppError
from py_types import BuiltinType, ClassType, FunctionType, PyType, builtins_map
from scope import Scope, ScopingNodeVisitor

type BindingTable = dict[ast.Name, Binding]


@dataclass
class Binding:
    node: ast.AST | None
    type: PyType


class ResolutionError(PyToCppError):
    def __init__(self, node):
        message = "Name could not be found"
        super().__init__(node, message)


class NameResolver(ScopingNodeVisitor):
    def __init__(
        self,
        scope: Scope,
        node_scopes,
        declared_types: dict[ast.AST, FunctionType | ClassType],
    ):
        super().__init__(scope, node_scopes)
        self.bindings: BindingTable = {}
        self.declared_types = declared_types
        for k, v in declared_types.items():
            print(f"{k.name}: {repr(v)}")

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
            self.resolve_name(node.annotation, self.scope().enclosing)

    def visit_Name(self, node: ast.Name):
        self.resolve_name(node, self.scope())

    def resolve_name(self, node: ast.Name, scope: Scope):
        # Only load contexts need resolution
        if not isinstance(node.ctx, ast.Load):
            return
        result = scope.resolve(node.id)
        # The name is user declared
        if result is not None:
            symbol_type, declaration_node = result
            typ = self.declared_types.get(declaration_node)
            binding = Binding(declaration_node, typ)
            self.bind_node(node, binding)
            return
        # The name could be a builtin or be undefined
        builtin = self.resolve_builtin(node.id)
        if builtin is not None:
            binding = Binding(None, builtin)
            self.bind_node(node, binding)
            return
        pp(node.id)
        scope.print_self()
        raise ResolutionError(node)
