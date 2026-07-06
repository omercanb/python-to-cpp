"""
Resolve names (including type annotations) to their declarations or Builtins
"""

import ast

import py_builtins
import symbols
from errors import PyToCppError


class ResolutionError(PyToCppError):
    def __init__(self, node):
        message = "Name could not be found"
        super().__init__(node, message)


class NameResolver(symbols.ScopingNodeVisitor):
    def __init__(self, scope):
        super().__init__(scope)
        self.resolutions: dict[ast.Name, ast.AST | py_builtins.Builtin] = {}

    def resolve_builtin(self, name: str):
        return py_builtins.builtins_map.get(name, None)

    def resolve_to(self, node: ast.Name, thing):
        assert node not in self.resolutions
        self.resolutions[node] = thing

    def print_resolutions(self):
        for name, resolution in self.resolutions.items():
            s = f"resolution: line {name.lineno} '{name.id}' resolves to "
            if isinstance(resolution, ast.AST):
                s += f"{resolution}"
                if hasattr(resolution, "lineno"):
                    s += f"on line {resolution.lineno}"
            else:
                s += f"builtin {resolution}"
            print(s)

    def visit_Name(self, node: ast.Name):
        # Load contexts are assigns
        if not isinstance(node.ctx, ast.Load):
            return
        result = self.scope().resolve(node.id)
        if result is not None:
            symbol_type, declaration_node = result
            self.resolve_to(node, declaration_node)
            return
        # The name could be a builtin or be undefined
        builtin = self.resolve_builtin(node.id)
        if builtin is not None:
            self.resolve_to(node, builtin)
            return
        else:
            raise ResolutionError(node)
