"""Debug utilities for printing for loop information from MyPy AST."""

from mypy.nodes import ForStmt, NameExpr, CallExpr, MemberExpr
from mypy.nodes import Expression as MypyExpression


def print_for_stmt(for_stmt: ForStmt) -> str:
    """Pretty-print a ForStmt node with its important fields.

    Returns a formatted string showing:
    - Target (loop variable)
    - Iterator expression
    - Index type
    - Inferred item type
    - Inferred iterator type
    """
    lines = []
    lines.append("ForStmt {")

    # Target (loop variable)
    target_str = format_expr(for_stmt.index)
    lines.append(f"  target: {target_str}")

    # Iterator/iterable expression
    iter_str = format_expr(for_stmt.expr)
    lines.append(f"  iter: {iter_str}")

    # Index type
    if for_stmt.index_type:
        lines.append(f"  index_type: {for_stmt.index_type}")

    # Inferred item type
    if for_stmt.inferred_item_type:
        lines.append(f"  item_type: {for_stmt.inferred_item_type}")

    # Inferred iterator type
    if for_stmt.inferred_iterator_type:
        lines.append(f"  iterator_type: {for_stmt.inferred_iterator_type}")

    lines.append("}")
    return "\n".join(lines)


def format_expr(expr: MypyExpression) -> str:
    """Format a MyPy expression for readable output."""
    if isinstance(expr, NameExpr):
        return f"Name({expr.name})"
    elif isinstance(expr, CallExpr):
        func_str = format_expr(expr.callee)
        args_str = ", ".join(format_expr(arg) for arg in expr.args)
        return f"{func_str}({args_str})"
    elif isinstance(expr, MemberExpr):
        obj_str = format_expr(expr.expr)
        return f"{obj_str}.{expr.name}"
    else:
        return expr.__class__.__name__
