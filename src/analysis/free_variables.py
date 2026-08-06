"""Free variable analysis for lifting comprehensions into standalone functions.

A comprehension's own indices are bound within it; anything else it reads
that resolves to a local (LDEF) rather than a global/builtin (GDEF) has to
come from the enclosing scope, and so has to be passed in as an argument
once the comprehension becomes its own function.
"""

from __future__ import annotations

from ast import Index
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from mypy.nodes import (
    LDEF,
    CallExpr,
    CastExpr,
    ComparisonExpr,
    ConditionalExpr,
    DictExpr,
    DictionaryComprehension,
    GeneratorExpr,
    IndexExpr,
    LambdaExpr,
    ListComprehension,
    ListExpr,
    Lvalue,
    MemberExpr,
    NameExpr,
    OpExpr,
    RefExpr,
    ReturnStmt,
    SetComprehension,
    SetExpr,
    SliceExpr,
    StarExpr,
    TupleExpr,
    UnaryExpr,
    Var,
)

from visitor import Visitor


@dataclass
class OrderedSet:
    data: dict[str, Any] = field(default_factory=dict)

    def add(self, item):
        self.data[item] = None

    def union(self, other: OrderedSet):
        self.data = dict(self.data, **other.data)

    def diff(self, other: OrderedSet):
        for item in other.data:
            self.data.pop(item, None)


@dataclass
class FreeBoundSet:
    free: OrderedSet = field(default_factory=OrderedSet)
    bound: OrderedSet = field(default_factory=OrderedSet)
    identifiers: dict[str, NameExpr] = field(default_factory=dict)

    def join(self, other: FreeBoundSet):
        """Joins the sets, giving precedence to the identifiers of self"""
        self.free.union(other.free)
        self.bound.union(other.bound)
        self.identifiers = dict(other.identifiers, **self.identifiers)

    def bind(self, other: FreeBoundSet):
        self.free.diff(other.bound)
        self.free.union(other.free)
        self.identifiers = dict(other.identifiers, **self.identifiers)


Comprehension = (
    GeneratorExpr
    | DictionaryComprehension
    | ListComprehension
    | SetComprehension
    | LambdaExpr
)


class _FreeVariableCollector(Visitor[FreeBoundSet]):

    def visit_generator_expr(self, o: GeneratorExpr) -> FreeBoundSet:
        return self.comprehension(o)

    def visit_list_comprehension(self, o: ListComprehension) -> FreeBoundSet:
        return self.comprehension(o.generator)

    def visit_set_comprehension(self, o: SetComprehension) -> FreeBoundSet:
        return self.comprehension(o.generator)

    def visit_dictionary_comprehension(
        self, o: DictionaryComprehension
    ) -> FreeBoundSet:
        return self.comprehension(o)

    def comprehension(self, o: GeneratorExpr | DictionaryComprehension) -> FreeBoundSet:
        """
        Pattern: [e1 for target1 in iter1 if cond1 for target2 in iter2 if cond2]
        iter1 is computed in the enclosing set
        later iters are computed in the enclosing sets (don't need to be explicitly handled)
        targets bind the names that they have but don't bind to any names used in iter1
        Note: the walrus operator inside a list comprehension is not allowed
        A comprehension binds nothing to the outer scope
        """
        if isinstance(o, GeneratorExpr):
            left_expr_set = self.visit(o.left_expr)
        else:
            left_expr_set = self.visit(o.key)
            left_expr_set.join(self.visit(o.value))

        target_sets = FreeBoundSet()
        for index_target in o.indices:
            target_sets.join(self.analyze_target(index_target))

        first_iter_set = self.visit(o.sequences[0])
        rest_iter_sets = FreeBoundSet()
        for iter_set in o.sequences[1:]:
            rest_iter_sets.join(self.visit(iter_set))

        cond_sets = FreeBoundSet()
        for condlist in o.condlists:
            for cond in condlist:
                cond_sets.join(self.visit(cond))

        result_set = FreeBoundSet()
        result_set.join(left_expr_set)
        result_set.join(rest_iter_sets)
        result_set.join(cond_sets)
        result_set.bind(target_sets)
        first_iter_set.join(result_set)
        result_set = first_iter_set

        return result_set

    def visit_lambda_expr(self, o: LambdaExpr) -> FreeBoundSet:
        ret = o.body.body[-1]
        assert isinstance(ret, ReturnStmt) and ret.expr is not None
        body_set = self.visit(ret.expr)

        params = FreeBoundSet()
        for argument in o.arguments:
            params.bound.add(argument.variable.name)
        body_set.bind(params)
        # Note: defaults of lambda parameters are evaluated in the enclosing scope
        defaults_set = FreeBoundSet()
        for argument in o.arguments:
            if argument.initializer is not None:
                defaults_set.join(self.visit(argument.initializer))
        defaults_set.join(body_set)

        return defaults_set

    def visit_name_expr(self, o: NameExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        if o.kind != LDEF:
            return s
        s.free.add(o.name)
        s.identifiers[o.name] = o
        return s

    def visit_int_expr(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_str_expr(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_bytes_expr(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_float_expr(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_complex_expr(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_ellipsis(self, o) -> FreeBoundSet:
        return FreeBoundSet()

    def visit_member_expr(self, o: MemberExpr) -> FreeBoundSet:
        return self.visit(o.expr)

    def visit_call_expr(self, o: CallExpr) -> FreeBoundSet:
        s = self.visit(o.callee)
        for argument in o.args:
            s.join(self.visit(argument))
        return s

    def visit_op_expr(self, o: OpExpr) -> FreeBoundSet:
        s = self.visit(o.left)
        s.join(self.visit(o.right))
        return s

    def visit_comparison_expr(self, o: ComparisonExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for operand in o.operands:
            s.join(self.visit(operand))
        return s

    def visit_unary_expr(self, o: UnaryExpr) -> FreeBoundSet:
        return self.visit(o.expr)

    def visit_index_expr(self, o: IndexExpr) -> FreeBoundSet:
        s = self.visit(o.base)
        s.join(self.visit(o.index))
        return s

    def visit_slice_expr(self, o: SliceExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for part in (o.begin_index, o.end_index, o.stride):
            if part is not None:
                s.join(self.visit(part))
        return s

    def visit_list_expr(self, o: ListExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for item in o.items:
            s.join(self.visit(item))
        return s

    def visit_set_expr(self, o: SetExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for item in o.items:
            s.join(self.visit(item))
        return s

    def visit_tuple_expr(self, o: TupleExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for item in o.items:
            s.join(self.visit(item))
        return s

    def visit_dict_expr(self, o: DictExpr) -> FreeBoundSet:
        s = FreeBoundSet()
        for key, value in o.items:
            if key is not None:
                s.join(self.visit(key))
            s.join(self.visit(value))
        return s

    def visit_conditional_expr(self, o: ConditionalExpr) -> FreeBoundSet:
        s = self.visit(o.cond)
        s.join(self.visit(o.if_expr))
        s.join(self.visit(o.else_expr))
        return s

    def analyze_target(self, node: Lvalue, ctx_store=True) -> FreeBoundSet:
        if isinstance(node, NameExpr):
            s = FreeBoundSet()
            if node.kind != LDEF:
                return s
            if ctx_store:
                s.bound.add(node.name)
            else:
                s.free.add(node.name)
            s.identifiers[node.name] = node
            return s
        elif isinstance(node, MemberExpr):
            return self.analyze_target(node.expr, ctx_store=False)
        elif isinstance(node, IndexExpr):
            base_set = self.analyze_target(node.base, ctx_store=False)
            index_set = self.analyze_target(node.index, ctx_store=False)
            base_set.join(index_set)
            return base_set
        elif isinstance(node, TupleExpr):
            s = FreeBoundSet()
            for item in node.items:
                item_set = self.analyze_target(item, ctx_store)
                s.join(item_set)
            return s
        else:
            assert False, "Not a possible lvalue target"


def get_free_variables(comprehension: Comprehension) -> list[NameExpr]:
    """The enclosing scope's variables a comprehension reads, in first-use order."""
    collector = _FreeVariableCollector()
    s = collector.visit(comprehension)
    free_vars = []
    for f in s.free.data:
        free_vars.append(s.identifiers[f])
    return free_vars
