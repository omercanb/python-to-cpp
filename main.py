import cProfile
import sys
from dataclasses import dataclass

from mypy import build
from mypy.build import BuildSource
from mypy.main import define_options
from mypy.nodes import AssignmentStmt, ClassDef, Expression, FuncDef, MypyFile, Var
from mypy.options import Options
from mypy.types import CallableType, Type

from python.codegen.mypy_codegen import StatementCodegen
from python.formatting import *
from python.utils import build_and_run

includes = ["print.h", "list.h", "ptr.h"]

# The (option, value) pairs `mypy --strict` sets, taken from mypy itself so they
# stay correct across upgrades. Checking during the build we already run saves a
# second full analysis pass.
_STRICT_ASSIGNMENTS = define_options()[2]


@dataclass
class AnalysisResult:
    tree: MypyFile
    types: dict[Expression, Type]


def mypy_options():
    opts = Options()
    opts.export_types = True  # required to populate result.types
    opts.preserve_asts = True  # keep the trees alive after checking
    opts.incremental = False  # avoid stale cache surprises
    for option, value in _STRICT_ASSIGNMENTS:
        setattr(opts, option, value)
    opts.strict_optional = True
    return opts


def _analyse(source: BuildSource) -> AnalysisResult:
    result = build.build(sources=[source], options=mypy_options())
    if result.errors:
        print("\n".join(result.errors))
        sys.exit(1)
    return AnalysisResult(result.files["main"], result.types)


def mypy_pipeline_source(source: str):
    return _analyse(BuildSource(None, "main", source))


def mypy_pipeline(path: str):
    return _analyse(BuildSource(path, "main", None))


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


def full_pipeline():
    file = "input.py"
    result = mypy_pipeline(file)
    print(result.tree)
    codegen = StatementCodegen(result.tree, result.types)
    output = codegen.generate()
    print(output)
    build_and_run(output)


def main():
    # cProfile.run("full_pipeline()", sort="cumtime")
    full_pipeline()


main()
