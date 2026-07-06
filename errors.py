import ast


class PyToCppError(Exception):
    def __init__(self, node: ast.AST, message: str):
        self.node = node
        self.message = message

    def __str__(self):
        return f"Error: On {self.node}, {self.message}"
