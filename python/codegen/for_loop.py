"""For loop translation from MyPy AST to C++."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mypy.nodes import CallExpr
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import ForStmt, IntExpr, NameExpr, OpExpr

if TYPE_CHECKING:
    from python.codegen.mypy_codegen import StatementCodegen


def translate_for_stmt(codegen: StatementCodegen, for_stmt: ForStmt) -> None:
    """Translate a MyPy ForStmt to C++ code."""
    # Match on the iterator expression type
    if isinstance(for_stmt.expr, CallExpr) and isinstance(
        for_stmt.expr.callee, NameExpr
    ):
        func_name = for_stmt.expr.callee.name

        # for i in range(len(list))
        if (
            func_name == "range"
            and len(for_stmt.expr.args) == 1
            and isinstance(for_stmt.expr.args[0], CallExpr)
            and isinstance(for_stmt.expr.args[0].callee, NameExpr)
            and for_stmt.expr.args[0].callee.name == "len"
        ):
            inner_iterable = for_stmt.expr.args[0].args[0]
            translate_for_range_len(codegen, for_stmt, inner_iterable)
            return

        # for i in range(...)
        if func_name == "range":
            translate_for_range(codegen, for_stmt)
            return

    # for i in iterable (generic)
    translate_for_generic(codegen, for_stmt)


def translate_for_range_len(
    codegen: StatementCodegen, for_stmt: ForStmt, inner_iterable: MypyExpression
) -> None:
    """Translate: for i in range(len(list))"""
    assert isinstance(for_stmt.index, NameExpr)
    target = for_stmt.index.name
    inner_iter_expr = codegen.get_expr(inner_iterable)
    for_line = (
        f"for (size_t {target} = 0; {target} < len({inner_iter_expr}); ++{target})"
    )
    write_for(codegen, for_line, for_stmt.body)


def _extract_int_constant(expr: MypyExpression) -> int | None:
    """Extract compile-time int from a literal, incl. unary +/-."""
    if isinstance(expr, IntExpr):
        return expr.value
    if isinstance(expr, OpExpr):
        # Handle unary minus: -5
        if expr.op == "-" and isinstance(expr.left, IntExpr):
            return -expr.left.value
        if expr.op == "+" and isinstance(expr.left, IntExpr):
            return expr.left.value
    return None


def translate_for_range(codegen: StatementCodegen, for_stmt: ForStmt) -> None:
    """Translate: for i in range(stop) or range(start, stop) or range(start, stop, step)"""
    assert isinstance(for_stmt.expr, CallExpr)
    call = for_stmt.expr
    args = call.args

    if len(args) in (1, 2):
        translate_for_range_no_step(codegen, for_stmt, args)
        return

    if len(args) == 3:
        step = _extract_int_constant(args[2])
        if step is not None:
            translate_for_range_constant_step(codegen, for_stmt, args, step)
        else:
            translate_for_range_unknown_step(codegen, for_stmt, args)
        return

    # Fallback to generic
    translate_for_generic(codegen, for_stmt)


def translate_for_range_no_step(
    codegen: StatementCodegen, for_stmt: ForStmt, args: list[MypyExpression]
) -> None:
    """Translate: for i in range(stop) or range(start, stop)"""
    assert isinstance(for_stmt.index, NameExpr)
    target = for_stmt.index.name

    if len(args) == 1:
        stop = codegen.get_expr(args[0])
        for_line = f"for (_int {target} = 0; {target} < {stop}; ++{target})"
    else:  # len(args) == 2
        start = codegen.get_expr(args[0])
        stop = codegen.get_expr(args[1])
        for_line = f"for (_int {target} = {start}; {target} < {stop}; ++{target})"

    write_for(codegen, for_line, for_stmt.body)


def translate_for_range_constant_step(
    codegen: StatementCodegen, for_stmt: ForStmt, args: list[MypyExpression], step: int
) -> None:
    """Translate: for i in range(start, stop, constant_step)"""
    assert isinstance(for_stmt.index, NameExpr)
    target = for_stmt.index.name
    start = codegen.get_expr(args[0])
    stop = codegen.get_expr(args[1])

    if step > 0:
        for_line = (
            f"for (_int {target} = {start}; {target} < {stop}; {target} += {step})"
        )
    else:
        for_line = (
            f"for (_int {target} = {start}; {target} > {stop}; {target} += {step})"
        )

    write_for(codegen, for_line, for_stmt.body)


def translate_for_range_unknown_step(
    codegen: StatementCodegen, for_stmt: ForStmt, args: list[MypyExpression]
) -> None:
    """Translate: for i in range(start, stop, dynamic_step)"""
    assert isinstance(for_stmt.index, NameExpr)
    target = for_stmt.index.name
    start = codegen.get_expr(args[0])
    stop = codegen.get_expr(args[1])
    step = codegen.get_expr(args[2])

    for_line = f"for (_int {target} = {start};; {target} += {step})"
    first_line = f"if (({step} > 0 && {target} >= {stop}) || ({step} < 0 && {target} <= {stop})) break;"
    write_for(codegen, for_line, for_stmt.body, first_line)


def translate_for_generic(codegen: StatementCodegen, for_stmt: ForStmt) -> None:
    """Translate: for var in iterable (generic iterator protocol)"""
    target = codegen.get_expr(for_stmt.index, lvalue=True)
    iterable = codegen.get_expr(for_stmt.expr)
    iter_var = f"__iter"

    codegen.emit(f"for (auto {iter_var} = iter({iterable}); !{iter_var}.done();) {{")
    codegen.indent()
    codegen.emit(f"{target} = next({iter_var});")
    for stmt in for_stmt.body.body:
        codegen.visit(stmt)
    codegen.unindent()
    codegen.emit("}")


def write_for(
    codegen: StatementCodegen,
    for_init: str,
    body,
    first_loop_line: str | None = None,
) -> None:
    """Write a C++ for loop with optional first line inside the loop."""
    codegen.emit(f"{for_init} {{")
    codegen.indent()
    if first_loop_line:
        codegen.emit(first_loop_line)
    for stmt in body.body:
        codegen.visit(stmt)
    codegen.unindent()
    codegen.emit("}")
