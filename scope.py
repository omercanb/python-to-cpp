import ast

from symbols import Scope, ScopeType


class ScopeResolver(ast.NodeVisitor):
    def __init__(self):
        self.scope = Scope(ScopeType.MODULE)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Inside a function, create a new scope
        self.scope = Scope(node.name, self.scope)
        self.generic_visit(node)
        self.scope = self.scope.enclosing

    def visit_AnnAssign(self, node: ast.AnnAssign):
        # Continue with defining assign target and resolving from here
        # Also handle for attribute and subscript
        # if isinstance(node.target, ast.Name):
        #     target = node.target.id
        # # Think back on how to handle attributes as targets
        # elif isinstance(node.target, ast.Attribute):
        #     target = node.target.value
        # else:
        #     assert False
        if isinstance(node.target, ast.Name):
            if self.scope.resolve(node.target.id):
                node.target.is_declaration = False
            else:
                node.target.is_declaration = True
                self.scope.define(node.target.id)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        assert len(node.targets) == 1
        target = node.targets[0]
        if isinstance(target, ast.Name):
            if self.scope.resolve(target.id):
                target.is_declaration = False
            else:
                target.is_declaration = True
                self.scope.define(target.id)
        self.generic_visit(node)
