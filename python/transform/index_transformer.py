"""Rewrites subscript reads and writes into explicit dunder-method calls.

`a[i]` becomes `a.__getitem__(i)`, `a[i] = v` becomes `a.__setitem__(i, v)`,
and a slice index `a[i:j:k]` becomes `a.__getitem__(slice(i, j, k))`, with a
missing bound passed as `None` (mypy has no dedicated node for it - `None`
is just a NameExpr named "None" with fullname "builtins.None").

Tuple indexing is left untouched: cpp/tuple.h has no runtime
__getitem__/__setitem__, only a compile-time get<N>() template method, so it
needs a real IndexExpr for codegen's translate_tuple_access. This is the one
case that isn't a validation concern - a plain `pair[0]` is legal Python, it
just needs a different lowering strategy than every other subscript.

analyse() runs validate() before this pass, so anything validate.py rejects
(slice assignment, a negative index other than -1, ...) can never reach here
in the first place - this pass doesn't need to leave those shapes alone for
some later check to catch, since there is no later check.
"""

from mypy.nodes import (
    ArgKind,
    AssignmentStmt,
    CallExpr,
    Expression,
    ExpressionStmt,
    IndexExpr,
    MemberExpr,
    NameExpr,
    Node,
    OperatorAssignmentStmt,
    SliceExpr,
)
from mypy.types import TupleType, Type, get_proper_type

from python.transform.tree_transformer import Transformer


def _none_expr() -> NameExpr:
    none = NameExpr("None")
    none.fullname = "builtins.None"
    return none


def _method_call(base: Expression, name: str, args: list[Expression]) -> CallExpr:
    return CallExpr(
        MemberExpr(base, name), args, [ArgKind.ARG_POS for _ in args], [None] * len(args)
    )


class IndexTransformer(Transformer):
    def __init__(self, types: dict[Expression, Type]):
        super().__init__()
        self.types = types

    def _is_tuple(self, base: Expression) -> bool:
        return isinstance(get_proper_type(self.types.get(base)), TupleType)

    def _slice_call(self, o: SliceExpr) -> CallExpr:
        bounds = [
            self.visit(bound) if bound is not None else _none_expr()
            for bound in (o.begin_index, o.end_index, o.stride)
        ]
        return CallExpr(NameExpr("slice"), bounds, [ArgKind.ARG_POS] * 3, [None] * 3)

    def visit_index_expr(self, o: IndexExpr) -> Node:
        o.base = self.visit(o.base)
        if self._is_tuple(o.base):
            o.index = self.visit(o.index)
            return o
        if isinstance(o.index, SliceExpr):
            index_arg: Expression = self._slice_call(o.index)
        else:
            index_arg = self.visit(o.index)
        result = _method_call(o.base, "__getitem__", [index_arg])
        self.types[result] = self.types[o]
        return result

    def visit_assignment_stmt(self, o: AssignmentStmt) -> Node:
        o.rvalue = self.visit(o.rvalue)
        if len(o.lvalues) == 1 and isinstance(o.lvalues[0], IndexExpr):
            target = o.lvalues[0]
            target.base = self.visit(target.base)
            if not self._is_tuple(target.base):
                index = self.visit(target.index)
                call = _method_call(target.base, "__setitem__", [index, o.rvalue])
                return ExpressionStmt(call)
            target.index = self.visit(target.index)
            return o
        o.lvalues = [self.visit(lvalue) for lvalue in o.lvalues]
        return o

    def visit_operator_assignment_stmt(self, o: OperatorAssignmentStmt) -> Node:
        # a[i] += v isn't implemented anywhere in codegen today; just make
        # sure a nested index (a[i][j] += v) still gets rewritten safely
        # without turning the outer target itself into an unassignable call.
        o.rvalue = self.visit(o.rvalue)
        if isinstance(o.lvalue, IndexExpr):
            o.lvalue.base = self.visit(o.lvalue.base)
            o.lvalue.index = self.visit(o.lvalue.index)
            return o
        o.lvalue = self.visit(o.lvalue)
        return o
