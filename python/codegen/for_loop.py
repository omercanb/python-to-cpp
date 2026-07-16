from __future__ import annotations

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python.codegen.codegen import CppTranslator


def match_for(self: CppTranslator, node: ast.For):
    if isinstance(node.target, ast.Name):
        self.test_declare_name(node.target)
    match node.iter:
        # for i in range(len(list))
        case ast.Call(
            func=ast.Name(), args=[ast.Call(func=ast.Name(), args=[inner_object])]
        ) as call if (
            isinstance(call.func, ast.Name)
            and isinstance(call.args[0], ast.Call)
            and isinstance(call.args[0].func, ast.Name)
            and call.func.id == "range"
            and call.args[0].func.id == "len"
        ):
            for_range_len(self, node, inner_object)
        # for i in range(number)
        case ast.Call(func=ast.Name()) as call if (
            isinstance(call.func, ast.Name) and call.func.id == "range"
        ):
            for_range(self, node)
        # for i in list
        case _:
            for_generic(self, node)


def for_range_len(self: CppTranslator, node: ast.For, inner_iterable: ast.expr):
    assert isinstance(node.target, ast.Name)
    target = self.visit(node.target)
    for_line = f"for (size_t {target} = 0; {target} < len({self.visit(inner_iterable)}); ++{target})"
    write_for(self, for_line, node.body)


def _const_int(node: ast.expr) -> int | None:
    """Extract a compile-time int from a literal, incl. unary +/-."""
    match node:
        case ast.Constant(value=int() as v) if not isinstance(v, bool):
            return v
        case ast.UnaryOp(
            op=ast.USub(), operand=ast.Constant(value=int() as v)
        ) if not isinstance(v, bool):
            return -v
        case ast.UnaryOp(
            op=ast.UAdd(), operand=ast.Constant(value=int() as v)
        ) if not isinstance(v, bool):
            return v
        case _:
            return None


def for_range(self: CppTranslator, node: ast.For) -> None:
    call = node.iter
    assert isinstance(call, ast.Call)

    args = call.args
    if len(args) in (1, 2):
        for_range_no_step(self, node)
        return

    if len(args) == 3:
        step = _const_int(args[2])
        if step is not None:
            for_range_constant_step(self, node, step)
        else:
            for_range_unkown_step(self, node)
        return

    for_generic(self, node)


def for_range_no_step(self: CppTranslator, node: ast.For):
    target = self.visit(node.target)
    assert isinstance(node.iter, ast.Call)
    step_args = node.iter.args
    if len(step_args) == 1:
        start = 0
        stop = step_args[0]
        for_line = f"for (int {target} = 0; {target} < {self.visit(stop)}; ++{target})"
    else:  # len(step_args) == 2:
        start, stop = step_args
        for_line = f"for (int {target} = {self.visit(start)}; {target} < {self.visit(stop)}; ++{target})"
    write_for(self, for_line, node.body)


def for_range_constant_step(self: CppTranslator, node: ast.For, step: int):
    target = self.visit(node.target)
    # We use the constant step to generate a < or > sign on the for condition
    assert isinstance(node.iter, ast.Call)
    start, stop = node.iter.args[:2]
    start = self.visit(start)
    stop = self.visit(stop)
    if step > 0:
        for_line = (
            f"for (int {target} = {start}; {target} < {stop}; {target} += {step})"
        )
    else:
        for_line = (
            f"for (int {target} = {start}; {target} > {stop}; {target} += {step})"
        )
    write_for(self, for_line, node.body)


def for_range_unkown_step(self: CppTranslator, node: ast.For):
    assert isinstance(node.iter, ast.Call)
    target = self.visit(node.target)
    start, stop, step = node.iter.args
    start = self.visit(start)
    stop = self.visit(stop)
    step = self.visit(step)
    for_line = f"for (int {target} = {start};; {target} += {step})"
    first_line = f"if (({step} > 0 && {target} >= {stop}) || ({step} < 0 && {target} <= {stop})) break;"
    write_for(self, for_line, node.body, first_line)


def for_generic(self: CppTranslator, node: ast.For):
    target = self.visit(node.target)
    iterable = self.visit(node.iter)
    assert isinstance(node.target, ast.Name)
    var = f"{node.target.id}__iter"
    for_line = f"for (auto {var} = iter({iterable}); !{var}.done();)"
    self.stmt(f"{for_line} {{")
    self.indent()
    self.stmt(f"{target} = next({var});")
    for child in node.body:
        self.visit(child)
    self.unindent()
    self.stmt("}")


def write_for(
    self: CppTranslator,
    for_init: str,
    body: list[ast.stmt],
    first_loop_line: str | None = None,
):
    self.stmt(f"{for_init} {{")
    self.indent()
    if first_loop_line:
        self.stmt(first_loop_line)
    for child in body:
        self.visit(child)
    self.unindent()
    self.stmt("}")
