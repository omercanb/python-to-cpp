import ast

class Scope:
    name: str
    enclosing: 'Scope'
    declarations = set()
    def __init__(self, name: str, enclosing: 'Scope'):
        self.name = name
        self.enclosing = enclosing

    def define(self, name):
        self.declarations.add(name)

    def resolve(self, name):
        if name in self.declarations:
            return True
        elif self.enclosing:
            return self.enclosing.resolve(name)
        else:
            return False


class ScopeResolver(ast.NodeVisitor):
    def __init__(self):
        self.scope = Scope("global", None)

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



