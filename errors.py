import ast


class PyToCppError(Exception):
    def __init__(self, node: ast.AST, message: str):
        self.node = node
        self.message = message
        super().__init__(message)

    def _describe(self) -> str:
        node = self.node
        match node:
            case ast.Name():
                return f"name '{node.id}'"
            case ast.FunctionDef() | ast.AsyncFunctionDef():
                return f"function '{node.name}'"
            case ast.ClassDef():
                return f"class '{node.name}'"
            case ast.arg():
                return f"parameter '{node.arg}'"
            case ast.Attribute():
                return f"attribute '{node.attr}'"
            case ast.Constant():
                return f"'{node.value}'"
            case _:
                return type(node).__name__

    def __str__(self) -> str:
        loc = ""
        if hasattr(self.node, "lineno"):
            loc = f" (line {self.node.lineno})"
        return f"{self._describe()}{loc}: {self.message}"
