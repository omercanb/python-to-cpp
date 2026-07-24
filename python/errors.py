"""Diagnostics for Python that the transpiler cannot translate.

Every diagnostic says what is unsupported and what to write instead, so the
message is actionable rather than just a refusal.
"""

from __future__ import annotations

from dataclasses import dataclass

from mypy.nodes import Context


@dataclass(frozen=True)
class Diagnostic:
    """One unsupported construct and the source span it occupies."""

    kind: str
    message: str
    hint: str
    line: int
    column: int
    end_line: int
    end_column: int

    @property
    def position(self) -> tuple[int, int]:
        return self.line, self.column


def diagnostic(node: Context, kind: str, message: str, hint: str) -> Diagnostic:
    """Build a diagnostic from any mypy node, which carries its own span."""
    end_line = node.end_line if node.end_line is not None else node.line
    end_column = node.end_column if node.end_column is not None else node.column + 1
    return Diagnostic(
        kind=kind,
        message=message,
        hint=hint,
        line=node.line,
        column=node.column,
        end_line=end_line,
        end_column=end_column,
    )


class UnsupportedProgram(Exception):
    """Every construct validation rejected, reported in one go."""

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        super().__init__(f"{len(diagnostics)} unsupported construct(s)")


def render(
    diagnostics: list[Diagnostic], source: str, path: str = "<source>"
) -> str:
    """Render diagnostics with the offending source line underlined."""
    lines = source.splitlines()
    return "\n".join(_render_one(d, lines, path) for d in diagnostics)


def _render_one(diagnostic: Diagnostic, lines: list[str], path: str) -> str:
    text = lines[diagnostic.line - 1] if diagnostic.line <= len(lines) else ""
    # A span running onto later lines is underlined to the end of the first.
    end = diagnostic.end_column if diagnostic.end_line == diagnostic.line else len(text)
    underline = " " * diagnostic.column + "^" * max(1, end - diagnostic.column)

    number = str(diagnostic.line)
    gutter = " " * len(number)
    # mypy columns are 0 based, editors and compilers count from 1.
    header = (
        f"{path}:{diagnostic.line}:{diagnostic.column + 1}: "
        f"error: {diagnostic.message}"
    )
    hint_lines = diagnostic.hint.splitlines()
    hint = "\n".join(
        [f"  help: {hint_lines[0]}"] + [f"          {l}" for l in hint_lines[1:]]
    )
    return (
        f"{header}\n"
        f"\n"
        f"  {number} | {text}\n"
        f"  {gutter} | {underline}\n"
        f"\n"
        f"{hint}\n"
    )
