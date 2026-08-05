"""Strips a leading docstring statement from the module top level and from every function/method body."""

from mypy.nodes import ExpressionStmt, FuncDef, MypyFile, Node, Statement, StrExpr

from python.transform.tree_transformer import Transformer


def _is_docstring(statement: Statement) -> bool:
    return isinstance(statement, ExpressionStmt) and isinstance(statement.expr, StrExpr)


class DocstringRemover(Transformer):
    def visit_mypy_file(self, o: MypyFile) -> Node:
        if o.defs and _is_docstring(o.defs[0]):
            o.defs = o.defs[1:]
        return super().visit_mypy_file(o)

    def visit_func_def(self, o: FuncDef) -> Node:
        if o.body.body and _is_docstring(o.body.body[0]):
            o.body.body = o.body.body[1:]
        return super().visit_func_def(o)
