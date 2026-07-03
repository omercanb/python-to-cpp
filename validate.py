import ast
import sys

from utils import dump

"""
Validate the constructs used in the program and give error messages
This makes it so the later steps will not have to continuosly assert that certain cases don't hold
"""


class Validator(ast.NodeVisitor):
    def error(self, node: ast.AST, message):
        print(f"Error: {message}")
        if hasattr(node, "lineno"):
            print(f"line: {node.lineno}")
        print(f"{ast.unparse(node)}")
        sys.exit(1)

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) > 1:
            self.error(node, "Multiple targets on the LHS of assing is not allowed")
