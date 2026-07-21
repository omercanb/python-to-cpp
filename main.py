import sys
from dataclasses import dataclass

from mypy import build
from mypy.api import run
from mypy.build import BuildSource
from mypy.nodes import AssignmentStmt, ClassDef, Expression, FuncDef, MypyFile, Var
from mypy.options import Options
from mypy.traverser import TraverserVisitor
from mypy.types import CallableType, Type

from python.codegen.mypy_codegen import StatementCodegen
from python.formatting import *
from python.utils import build_and_run

includes = ["print.h", "list.h", "ptr.h"]


def validate(path: str):
    normal_report, error_report, exit_status = run([path, "--strict"])
    if exit_status != 0:
        print(normal_report)
        print(error_report)
        sys.exit(exit_status)


@dataclass
class AnalysisResult:
    tree: MypyFile
    types: dict[Expression, Type]


def mypy_options():
    opts = Options()
    opts.export_types = True  # required to populate result.types
    opts.preserve_asts = True  # keep the trees alive after checking
    opts.incremental = False  # avoid stale cache surprises
    opts.disallow_untyped_defs = True
    opts.disallow_untyped_calls = True
    opts.check_untyped_defs = True
    opts.strict_optional = True
    return opts


def mypy_pipeline_source(source: str):
    opts = mypy_options()
    result = build.build(sources=[BuildSource(None, "main", source)], options=opts)
    tree = result.files["main"]
    types = result.types
    return AnalysisResult(tree, types)


def mypy_pipeline(path: str):
    opts = mypy_options()

    result = build.build(
        sources=[BuildSource(path, "main", None)],
        options=opts,
    )

    tree = result.files["main"]
    types = result.types
    return AnalysisResult(tree, types)


def translate(path: str):
    result = mypy_pipeline(path)
    codegen = StatementCodegen(result.tree, result.types)
    output = codegen.generate()
    return output


def translate_source(source: str):
    result = mypy_pipeline_source(source)
    codegen = StatementCodegen(result.tree, result.types)
    output = codegen.generate()
    return output


def main():
    file = "input.py"
    result = mypy_pipeline(file)
    codegen = StatementCodegen(result.tree, result.types)
    output = codegen.generate()
    print(output)
    build_and_run(output)


main()
