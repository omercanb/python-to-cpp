"""Hand-rolled visitor bases for the mypy AST.

mypy's own visitor classes (``NodeVisitor``, ``ExpressionVisitor``,
``TraverserVisitor``) are mypyc traits. An interpreted subclass of a compiled
trait raises ``TypeError: interpreted classes cannot inherit from compiled
traits`` when instantiated (python/mypy#19456), so subclassing them forces the
pure-Python mypy wheel, which analyses a file about 4x slower than the compiled
one. Dispatching here instead of calling ``node.accept(visitor)`` keeps us on
the compiled wheel.
"""

from __future__ import annotations

import re
from typing import Generic, TypeVar

from mypy.nodes import (
    AssertStmt,
    AssignmentExpr,
    AssignmentStmt,
    Block,
    CallExpr,
    CastExpr,
    ClassDef,
    ComparisonExpr,
    ConditionalExpr,
    DelStmt,
    DictExpr,
    Expression,
    ForStmt,
    FuncDef,
    IfStmt,
    IndexExpr,
    LambdaExpr,
    ListExpr,
    MemberExpr,
    MypyFile,
    Node,
    OperatorAssignmentStmt,
    OpExpr,
    RaiseStmt,
    ReturnStmt,
    SetExpr,
    SliceExpr,
    StarExpr,
    TupleExpr,
    UnaryExpr,
    WhileStmt,
)

T = TypeVar("T")

# mypy names each visit_* after its node class in snake_case, bar these.
_IRREGULAR_NAMES = {
    "EllipsisExpr": "visit_ellipsis",
    "ParamSpecExpr": "visit_paramspec_expr",
    "NamedTupleExpr": "visit_namedtuple_expr",
    "TypedDictExpr": "visit_typeddict_expr",
    "PromoteExpr": "visit__promote_expr",
    "NewTypeExpr": "visit_newtype_expr",
}

_method_names: dict[type, str] = {}


def _method_name(node_type: type) -> str:
    name = _method_names.get(node_type)
    if name is None:
        class_name = node_type.__name__
        name = _IRREGULAR_NAMES.get(
            class_name,
            "visit_" + re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower(),
        )
        _method_names[node_type] = name
    return name


class Visitor(Generic[T]):
    """Dispatch a node to its visit_* method, in place of node.accept(self)."""

    def visit(self, node: Node) -> T:
        name = _method_name(type(node))
        method = getattr(self, name, None)
        if method is None:
            raise NotImplementedError(
                f"{type(self).__name__} has no {name}() for {type(node).__name__}"
            )
        return method(node)


class Traverser(Visitor[None]):
    """Walk every child of a node. Subclasses override what they care about."""

    def visit_mypy_file(self, o: MypyFile) -> None:
        for definition in o.defs:
            self.visit(definition)

    def visit_block(self, o: Block) -> None:
        for statement in o.body:
            self.visit(statement)

    def visit_func_def(self, o: FuncDef) -> None:
        for argument in o.arguments:
            if argument.initializer is not None:
                self.visit(argument.initializer)
        self.visit(o.body)

    def visit_class_def(self, o: ClassDef) -> None:
        self.visit(o.defs)

    def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
        for lvalue in o.lvalues:
            self.visit(lvalue)
        self.visit(o.rvalue)

    def visit_operator_assignment_stmt(self, o: OperatorAssignmentStmt) -> None:
        self.visit(o.lvalue)
        self.visit(o.rvalue)

    def visit_expression_stmt(self, o) -> None:
        self.visit(o.expr)

    def visit_return_stmt(self, o: ReturnStmt) -> None:
        if o.expr is not None:
            self.visit(o.expr)

    def visit_if_stmt(self, o: IfStmt) -> None:
        for condition in o.expr:
            self.visit(condition)
        for body in o.body:
            self.visit(body)
        if o.else_body is not None:
            self.visit(o.else_body)

    def visit_while_stmt(self, o: WhileStmt) -> None:
        self.visit(o.expr)
        self.visit(o.body)
        if o.else_body is not None:
            self.visit(o.else_body)

    def visit_for_stmt(self, o: ForStmt) -> None:
        self.visit(o.index)
        self.visit(o.expr)
        self.visit(o.body)
        if o.else_body is not None:
            self.visit(o.else_body)

    def visit_assert_stmt(self, o: AssertStmt) -> None:
        self.visit(o.expr)
        if o.msg is not None:
            self.visit(o.msg)

    def visit_del_stmt(self, o: DelStmt) -> None:
        self.visit(o.expr)

    def visit_raise_stmt(self, o: RaiseStmt) -> None:
        if o.expr is not None:
            self.visit(o.expr)
        if o.from_expr is not None:
            self.visit(o.from_expr)

    def visit_break_stmt(self, o) -> None:
        pass

    def visit_continue_stmt(self, o) -> None:
        pass

    def visit_pass_stmt(self, o) -> None:
        pass

    def visit_import(self, o) -> None:
        pass

    def visit_import_from(self, o) -> None:
        pass

    def visit_import_all(self, o) -> None:
        pass

    def visit_name_expr(self, o) -> None:
        pass

    def visit_int_expr(self, o) -> None:
        pass

    def visit_str_expr(self, o) -> None:
        pass

    def visit_bytes_expr(self, o) -> None:
        pass

    def visit_float_expr(self, o) -> None:
        pass

    def visit_complex_expr(self, o) -> None:
        pass

    def visit_ellipsis(self, o) -> None:
        pass

    def visit_var(self, o) -> None:
        pass

    def visit_temp_node(self, o) -> None:
        pass

    def visit_member_expr(self, o: MemberExpr) -> None:
        self.visit(o.expr)

    def visit_call_expr(self, o: CallExpr) -> None:
        self.visit(o.callee)
        for argument in o.args:
            self.visit(argument)

    def visit_op_expr(self, o: OpExpr) -> None:
        self.visit(o.left)
        self.visit(o.right)

    def visit_comparison_expr(self, o: ComparisonExpr) -> None:
        for operand in o.operands:
            self.visit(operand)

    def visit_unary_expr(self, o: UnaryExpr) -> None:
        self.visit(o.expr)

    def visit_index_expr(self, o: IndexExpr) -> None:
        self.visit(o.base)
        self.visit(o.index)

    def visit_slice_expr(self, o: SliceExpr) -> None:
        for part in (o.begin_index, o.end_index, o.stride):
            if part is not None:
                self.visit(part)

    def visit_list_expr(self, o: ListExpr) -> None:
        for item in o.items:
            self.visit(item)

    def visit_set_expr(self, o: SetExpr) -> None:
        for item in o.items:
            self.visit(item)

    def visit_tuple_expr(self, o: TupleExpr) -> None:
        for item in o.items:
            self.visit(item)

    def visit_dict_expr(self, o: DictExpr) -> None:
        for key, value in o.items:
            if key is not None:
                self.visit(key)
            self.visit(value)

    def visit_lambda_expr(self, o: LambdaExpr) -> None:
        self.visit(o.body)

    def visit_conditional_expr(self, o: ConditionalExpr) -> None:
        self.visit(o.cond)
        self.visit(o.if_expr)
        self.visit(o.else_expr)

    def visit_star_expr(self, o: StarExpr) -> None:
        self.visit(o.expr)

    def visit_assignment_expr(self, o: AssignmentExpr) -> None:
        self.visit(o.target)
        self.visit(o.value)

    def visit_cast_expr(self, o: CastExpr) -> None:
        self.visit(o.expr)
