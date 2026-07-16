from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Mapping

from python.formatting import *

if TYPE_CHECKING:
    from .analysis.py_types import PyType


def build_and_run(translated: str, src="main.cpp", exe="main", std="c++17"):
    """Write `translated` to a .cpp file, compile with g++, run it, print output."""
    # 1. write the source
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    # 2. compile:  g++ main.cpp -o main
    compile_proc = subprocess.run(
        ["g++", "-ggdb", f"-std={std}", f"-Icpp", src, "-o", exe],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        print("--- compile FAILED ---")
        print(compile_proc.stderr)
        return  # stop: no binary to run
    if compile_proc.stderr:  # warnings still compile
        print("--- compiler warnings ---")
        print(compile_proc.stderr)

    # 3. run ./main and print its output
    run_proc = subprocess.run(["stdbuf", "-oL", f"./{exe}"])
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")


def build_and_run_capture(
    translated: str, src="main.cpp", exe="main", std="c++17"
) -> subprocess.CompletedProcess:
    """Write `translated` to a .cpp file, compile with g++, run it, print output."""
    # 1. write the source
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    # 2. compile:  g++ main.cpp -o main
    compile_proc = subprocess.run(
        ["g++", "-ggdb", f"-std={std}", f"-Icpp", src, "-o", exe],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        print("--- compile FAILED ---")
        print(compile_proc.stderr)
        raise ValueError("Compile error")
    if compile_proc.stderr:  # warnings still compile
        print("--- compiler warnings ---")
        print(compile_proc.stderr)

    # 3. run ./main and print its output
    run_proc = subprocess.run(
        ["stdbuf", "-oL", f"./{exe}"], capture_output=True, text=True
    )
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")
    return run_proc


# The dump function from the ast library, modified to print types if available
def dump(
    node,
    annotate_fields=True,
    include_attributes=False,
    *,
    indent=None,
    show_empty=False,
    types: Mapping[ast.AST, PyType] = {},
):
    """
    Return a formatted dump of the tree in node.  This is mainly useful for
    debugging purposes.  If annotate_fields is true (by default),
    the returned string will show the names and the values for fields.
    If annotate_fields is false, the result string will be more compact by
    omitting unambiguous field names.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    include_attributes can be set to true.  If indent is a non-negative
    integer or string, then the tree will be pretty-printed with that indent
    level. None (the default) selects the single line representation.
    If show_empty is False, then empty lists and fields that are None
    will be omitted from the output for better readability.
    """

    def _format(node, level=0):
        if indent is not None:
            level += 1
            prefix = "\n" + indent * level
            sep = ",\n" + indent * level
        else:
            prefix = ""
            sep = ", "
        if isinstance(node, ast.AST):
            cls = type(node)
            args = []
            args_buffer = []
            allsimple = True
            keywords = annotate_fields
            for name in node._fields:
                try:
                    value = getattr(node, name)
                except AttributeError:
                    keywords = True
                    continue
                if value is None and getattr(cls, name, ...) is None:
                    keywords = True
                    continue
                if not show_empty:
                    if value == []:
                        field_type = cls._field_types.get(name, object)
                        if getattr(field_type, "__origin__", ...) is list:
                            if not keywords:
                                args_buffer.append(repr(value))
                            continue
                    if not keywords:
                        args.extend(args_buffer)
                        args_buffer = []
                value, simple = _format(value, level)
                allsimple = allsimple and simple
                if keywords:
                    args.append("%s=%s" % (name, value))
                else:
                    args.append(value)
            if include_attributes and node._attributes:
                for name in node._attributes:
                    try:
                        value = getattr(node, name)
                    except AttributeError:
                        continue
                    if value is None and getattr(cls, name, ...) is None:
                        continue
                    value, simple = _format(value, level)
                    allsimple = allsimple and simple
                    args.append("%s=%s" % (name, value))
            if node in types:
                if allsimple and len(args) <= 3:
                    return (
                        "%s: type(%s) (%s)"
                        % (
                            node.__class__.__name__,
                            get_type_name(types[node]),
                            ", ".join(args),
                        ),
                        not args,
                    )
                return (
                    "%s type(%s) (%s%s)"
                    % (
                        node.__class__.__name__,
                        get_type_name(types[node]),
                        prefix,
                        sep.join(args),
                    ),
                    False,
                )
            else:
                if allsimple and len(args) <= 3:
                    return (
                        "%s(%s)" % (node.__class__.__name__, ", ".join(args)),
                        not args,
                    )
                return (
                    "%s(%s%s)" % (node.__class__.__name__, prefix, sep.join(args)),
                    False,
                )

        elif isinstance(node, list):
            if not node:
                return "[]", True
            return (
                "[%s%s]" % (prefix, sep.join(_format(x, level)[0] for x in node)),
                False,
            )
        return repr(node), True

    if not isinstance(node, ast.AST):
        raise TypeError("expected AST, got %r" % node.__class__.__name__)
    if indent is not None and not isinstance(indent, str):
        indent = " " * indent
    return _format(node)[0]
