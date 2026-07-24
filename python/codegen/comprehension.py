"""Comprehension translation from MyPy AST to C++.

A comprehension is an expression, but the loops it needs are statements, so
each one is lifted into a function of its own and the expression becomes a
call to it. The generators reuse the for statement's loop headers, so
`[x for x in range(n)]` walks its range exactly the way `for x in range(n)`
does.

Adding another kind of comprehension means adding one STRUCTURES entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from mypy.nodes import (
    DictionaryComprehension,
    Expression,
    ListComprehension,
    NameExpr,
    SetComprehension,
    Var,
)

from python.codegen.for_loop import loop_header, write_loop
from python.codegen.translation_utils import translate_constructor
from python.codegen.typegen import cpp_type
from python.visitor import Traverser

if TYPE_CHECKING:
    from python.codegen.mypy_codegen import StatementCodegen

# A comprehension node carrying the loops, and either a `left_expr` or a
# key/value pair. Both shapes expose indices, sequences and condlists.
Comprehension = ListComprehension | SetComprehension | DictionaryComprehension


@dataclass(frozen=True)
class Structure:
    """How one kind of comprehension accumulates into its result."""

    # The parts evaluated per item, in the order the add method takes them.
    values: Callable[[object], list[Expression]]
    # The method that puts them into the result.
    add: str


STRUCTURES: dict[type, Structure] = {
    ListComprehension: Structure(values=lambda g: [g.left_expr], add="append"),
    SetComprehension: Structure(values=lambda g: [g.left_expr], add="add"),
    DictionaryComprehension: Structure(
        values=lambda g: [g.key, g.value], add="__setitem__"
    ),
}


def generator_of(node: Comprehension):
    """The node holding the for/if clauses.

    A dict comprehension is its own generator; the others wrap one.
    """
    return node.generator if hasattr(node, "generator") else node


class _Finder(Traverser):
    """Collects comprehensions, innermost first.

    Each walk goes through Traverser's own method rather than self.visit, which
    would dispatch straight back here and never descend. Alongside each one
    goes the indices of the comprehensions it sits inside, which it reads as
    ordinary variables and so has to be handed.
    """

    def __init__(self) -> None:
        self.found: list[tuple[Comprehension, set[str]]] = []
        self._enclosing: list[list[str]] = []

    def _record(self, o: Comprehension, walk: Callable) -> None:
        # Its own indices are bound inside it, so they are pushed only for the
        # walk of its children.
        enclosing = {name for level in self._enclosing for name in level}
        generator = generator_of(o)
        self._enclosing.append(
            [index.name for index in generator.indices if isinstance(index, NameExpr)]
        )
        walk(self, o)
        self._enclosing.pop()
        self.found.append((o, enclosing))

    def visit_list_comprehension(self, o: ListComprehension) -> None:
        self._record(o, Traverser.visit_list_comprehension)

    def visit_set_comprehension(self, o: SetComprehension) -> None:
        self._record(o, Traverser.visit_set_comprehension)

    def visit_dictionary_comprehension(self, o: DictionaryComprehension) -> None:
        self._record(o, Traverser.visit_dictionary_comprehension)


def find_comprehensions(node) -> list[tuple[Comprehension, set[str]]]:
    finder = _Finder()
    finder.visit(node)
    return finder.found


class _NameCollector(Traverser):
    def __init__(self) -> None:
        self.names: list[NameExpr] = []

    def visit_name_expr(self, o: NameExpr) -> None:
        self.names.append(o)


def captured_names(node: Comprehension, local: Callable[[str], bool]) -> list[NameExpr]:
    """The enclosing function's variables a comprehension reads.

    Its own loop indices are bound inside, and anything at file scope is
    already visible, so only the enclosing locals have to be passed in.
    """
    generator = generator_of(node)
    bound = {
        index.name for index in generator.indices if isinstance(index, NameExpr)
    }
    collector = _NameCollector()
    for part in [*generator.sequences, *STRUCTURES[type(node)].values(generator)]:
        collector.visit(part)
    for conditions in generator.condlists:
        for condition in conditions:
            collector.visit(condition)

    seen: dict[str, NameExpr] = {}
    for name in collector.names:
        if name.name in bound or name.name in seen:
            continue
        if isinstance(name.node, Var) and local(name.name):
            seen[name.name] = name
    return list(seen.values())


def translate_comprehension(
    codegen: StatementCodegen, node: Comprehension, name: str, captures: list[NameExpr]
) -> None:
    """Emit the function that builds one comprehension's result."""
    generator = generator_of(node)
    structure = STRUCTURES[type(node)]
    result_type = codegen.types[node]

    parameters = ", ".join(
        f"{cpp_type(codegen.types[capture])} {capture.name}" for capture in captures
    )
    codegen.emit(f"{cpp_type(result_type)} {name}({parameters}) {{")
    codegen.indent()

    result = codegen.temp_name("result")
    codegen.emit(f"{cpp_type(result_type)} {result} = {translate_constructor(result_type, '')};")
    for index in generator.indices:
        codegen.emit(codegen.translate_declaration(index.name, codegen.types[index]))

    def accumulate() -> None:
        values = ", ".join(
            codegen.get_expr(value) for value in structure.values(generator)
        )
        codegen.emit(f"{result}->{structure.add}({values});")

    write_generators(codegen, generator, 0, accumulate)

    codegen.emit(f"return {result};")
    codegen.unindent()
    codegen.emit("}")
    codegen.emit("")


def write_generators(
    codegen: StatementCodegen, generator, depth: int, accumulate: Callable[[], None]
) -> None:
    """Nest one loop per `for` clause, with its `if`s inside it."""
    if depth == len(generator.sequences):
        accumulate()
        return

    header = loop_header(
        codegen, generator.indices[depth], generator.sequences[depth]
    )

    def body() -> None:
        conditions = generator.condlists[depth]
        for condition in conditions:
            codegen.emit(f"if ({codegen.get_condition(condition)}) {{")
            codegen.indent()
        write_generators(codegen, generator, depth + 1, accumulate)
        for _ in conditions:
            codegen.unindent()
            codegen.emit("}")

    write_loop(codegen, header, body)
