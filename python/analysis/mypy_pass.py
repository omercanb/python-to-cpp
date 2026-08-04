import os
import sys
from dataclasses import dataclass
from pathlib import Path

from mypy import build
from mypy.main import define_options
from mypy.modulefinder import BuildSource
from mypy.nodes import (
    AssignmentStmt,
    DictExpr,
    Expression,
    FuncDef,
    ListExpr,
    MypyFile,
    NameExpr,
    RefExpr,
    SetExpr,
    TempNode,
    TypeInfo,
    Var,
)
from mypy.options import Options
from mypy.types import ProperType, Type, get_proper_type

from python.analysis.validate import validate
from python.codegen.mypy_codegen import StatementCodegen
from python.errors import UnsupportedProgram, render
from python.transform.comprehension_transformer import ComprehensionRemover
from python.transform.tree_transformer import Transformer
from python.visitor import Traverser

type TypeTable = dict[Expression, ProperType | TypeInfo]

_STRICT_ASSIGNMENTS = define_options()[2]


@dataclass
class AnalysisResult:
    tree: MypyFile
    types: TypeTable
    source: str
    path: str | None


def mypy_options():
    opts = Options()
    opts.export_types = True  # required to populate result.types
    opts.preserve_asts = True  # keep the trees alive after checking
    # Caching typeshed takes a build from ~0.45s to ~0.015s
    # Make sure to always give the source when using BuildSource
    # because with this on it will otherwise just skip the file
    opts.incremental = True
    # A cache dir per worker; concurrent writers to one can corrupt it.
    worker = os.environ.get("PYTEST_XDIST_WORKER")
    opts.cache_dir = f".mypy_cache/{worker}" if worker else ".mypy_cache"
    for option, value in _STRICT_ASSIGNMENTS:
        setattr(opts, option, value)
    opts.strict_optional = True
    return opts


def parse(path: str | None, source: str) -> MypyFile:
    # Path is an optional parameter because it's only used for error messages
    result = build.build(
        sources=[BuildSource(path, "main", source)], options=mypy_options()
    )
    if result.errors:
        print("\n".join(result.errors))
        sys.exit(1)
    tree = result.files["main"]
    return tree


def analyse(path: str | None, source: str) -> AnalysisResult:
    """
    The mypy analysis pass
    Does type inference, defines classes, resolves names
    Does some additional work on top of just running mypy
    """
    # Path is an optional parameter because it's only used for error messages
    result = build.build(
        sources=[BuildSource(path, "main", source)], options=mypy_options()
    )
    if result.errors:
        print("\n".join(result.errors))
        sys.exit(1)
    tree = result.files["main"]
    _apply_transforms(tree, result.types)

    types = get_resolved_types(result.files["main"], result.types)

    return AnalysisResult(result.files["main"], types, source, path)


def _apply_transforms(tree: MypyFile, types: dict[Expression, Type]):
    t = ComprehensionRemover(types)
    t.visit(tree)
    print(tree)


def _generate(result: AnalysisResult) -> str:
    """Validate, then translate. Codegen only ever sees a translatable tree."""
    return StatementCodegen(result.tree, result.types).generate()


def pipeline(path: str, source: str) -> str:
    result = analyse(path, source)
    diagnostics = validate(result.tree, result.types)
    if diagnostics:
        print(render(diagnostics, result.source, path))
        raise UnsupportedProgram(diagnostics)
    output = _generate(result)
    return output


def get_resolved_types(tree: MypyFile, types: dict[Expression, Type]) -> TypeTable:
    """
    Mypy can resolve types even if they weren't determined when declared, eg: a = [], a.append(1) becomes a list[int]
    However, only the type known at that moment is stored in the the type table thats returned from mypy and it instead stores the types in an attribute.
    This function uses those attributes to create the type table that should actually be used for the program
    """
    fixup_partial_literals(tree, types)

    type_table: TypeTable = {}
    temps = 0
    for expr, t in types.items():
        if isinstance(expr, TempNode):
            temps += 1
            # This is an artifact from type checking according to mypy
            continue
        if isinstance(expr, RefExpr) and expr.node is not None:
            # if isinstance(expr.node, TypeInfo):
            #     type_table[expr] = expr.node
            if isinstance(expr.node, Var) or isinstance(expr.node, FuncDef):
                assert expr.node.type is not None
                type_table[expr] = get_proper_type(expr.node.type)
            else:
                type_table[expr] = get_proper_type(types[expr])
        else:
            type_table[expr] = get_proper_type(t)

    assert len(type_table) + temps == len(types), "Some types weren't captured"
    return type_table


def fixup_partial_literals(tree: MypyFile, types: dict[Expression, Type]) -> None:
    """
    Mypy doesn't really try to type container literals
    For example: a = [], a.append(1). Then [] will have type list[Never] while a has type list[int]
    This function provides a type to the container literal
    """

    class _PartialLiteralFinder(Traverser):
        def __init__(self, types: dict[Expression, Type]) -> None:
            self.types = types

        def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
            if len(o.lvalues) == 1:
                lvalue = o.lvalues[0]
                if (
                    isinstance(lvalue, NameExpr)
                    and isinstance(lvalue.node, Var)
                    and isinstance(o.rvalue, (ListExpr, DictExpr, SetExpr))
                ):
                    resolved = lvalue.node.type
                    assert resolved is not None
                    self.types[lvalue] = resolved
                    self.types[o.rvalue] = resolved
            super().visit_assignment_stmt(
                o
            )  # keep recursing into nested functions/blocks

    _PartialLiteralFinder(types).visit(tree)
