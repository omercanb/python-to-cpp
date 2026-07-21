"""Builtin function definitions and utilities for code generation."""

from mypy.nodes import StrExpr

# Define builtin functions and their properties
BUILTINS = {
    "builtins.print": {
        "kwargs": ["sep", "end"],
        "defaults": {
            "sep": StrExpr(" "),
            "end": StrExpr("\\n"),
        },
    }
}


def get_kwarg_order(fullname: str) -> list[str]:
    """Get the order of kwargs for a builtin function."""
    return BUILTINS[fullname]["kwargs"]


def get_kwarg_defaults(fullname: str) -> dict[str, StrExpr]:
    """Get default values for a builtin function's kwargs."""
    return BUILTINS[fullname]["defaults"]


def is_builtin_with_kwargs(fullname: str) -> bool:
    """Check if a function is a registered builtin with kwargs."""
    return fullname in BUILTINS
