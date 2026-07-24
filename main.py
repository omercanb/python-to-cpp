import cProfile
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from mypy import build
from mypy.build import BuildSource
from mypy.main import define_options
from mypy.nodes import AssignmentStmt, ClassDef, Expression, FuncDef, MypyFile, Var
from mypy.options import Options
from mypy.types import CallableType, Type

from python.analysis.validate import validate
from python.codegen.mypy_codegen import StatementCodegen
from python.errors import UnsupportedProgram, render
from python.formatting import *
from python.utils import build_and_run

includes = ["print.h", "list.h", "ptr.h"]

# Mypys strict upgrades
_STRICT_ASSIGNMENTS = define_options()[2]


@dataclass
class AnalysisResult:
    tree: MypyFile
    types: dict[Expression, Type]
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


def _analyse(path: str | None, source: str) -> AnalysisResult:
    # The text forces a re-parse, the path keeps real filenames in errors.
    result = build.build(
        sources=[BuildSource(path, "main", source)], options=mypy_options()
    )
    if result.errors:
        print("\n".join(result.errors))
        sys.exit(1)
    return AnalysisResult(result.files["main"], result.types, source, path)


def mypy_pipeline_source(source: str):
    return _analyse(None, source)


def mypy_pipeline(path: str):
    return _analyse(path, Path(path).read_text())


def _generate(result: AnalysisResult) -> str:
    """Validate, then translate. Codegen only ever sees a translatable tree."""
    diagnostics = validate(result.tree, result.types)
    if diagnostics:
        raise UnsupportedProgram(diagnostics)
    return StatementCodegen(result.tree, result.types).generate()


def translate(path: str):
    return _generate(mypy_pipeline(path))


def translate_source(source: str):
    return _generate(mypy_pipeline_source(source))


def full_pipeline():
    file = "input.py"
    result = mypy_pipeline(file)
    print(result.tree)
    try:
        output = _generate(result)
    except UnsupportedProgram as unsupported:
        print(render(unsupported.diagnostics, result.source, file))
        sys.exit(1)
    print(output)
    build_and_run(output)


def main():
    # cProfile.run("full_pipeline()", sort="cumtime")
    full_pipeline()


# Guarded: the tests import from here, and unguarded this ran the whole
# pipeline on every import.
if __name__ == "__main__":
    main()
