import ast
import types
import typing
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp

from python.analysis import scope, symbol_declaration, type_inference, validate
from python.analysis.scope import ScopeType
from python.utils import build_and_run, dump

ANNOTATION_TYPES = {
    "int": int,
    "float": float,
    "bool": bool,
    "str": str,
}

includes = ["print.h", "list.h", "ptr.h"]


def main():
    file = "input.py"
    tree = ast.parse(open(file).read())

    print(dump(tree, indent=4))
    # validate.Validator().visit(tree)

    # scope.ScopeResolver().visit(tree)
    definer = symbols.SymbolDefiner()
    definer.visit(tree)
    definer.scope.print_tree()
    for scope in scope.ScopeTracker():
        scope.print_self()
    TestWalker(definer.scope).visit(tree)


class TestWalker(ast.NodeVisitor):
    def __init__(self, scope: scope.Scope):
        self.scope_tracker = scope.ScopeTracker(scope)

    def visit(self, node: ast.AST):
        cur_scope = self.scope_tracker.scope
        self.scope_tracker.update(node)
        new_scope = self.scope_tracker.scope
        if cur_scope != new_scope:
            if hasattr(node, "lineno"):
                print(node.lineno)
            print(ast.unparse(node))
            self.scope_tracker.scope.print_self()
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


main()
