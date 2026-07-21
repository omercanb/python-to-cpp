import sys
from dataclasses import dataclass

from mypy import build
from mypy.api import run
from mypy.build import BuildSource
from mypy.nodes import AssignmentStmt, ClassDef, Expression, FuncDef, MypyFile, Var
from mypy.options import Options
from mypy.traverser import TraverserVisitor
from mypy.types import CallableType, Type

from python.analysis.name_resolution import NameResolver
from python.analysis.scope import ScopeTreeCreator
from python.analysis.symbol_declaration import SymbolDefiner
from python.analysis.type_annotation import (
    ClassTypeDeclarer,
    FunctionAndClassTypeAnnotator,
    TypeAnnotator,
)
from python.analysis.type_inference import TypeInferrer
from python.codegen.codegen import CppTranslator
from python.codegen.mypy_codegen import StatementCodegen
from python.formatting import *
from python.utils import build_and_run, dump

includes = ["print.h", "list.h", "ptr.h"]


def pipeline(program: str, debug=False):
    tree = ast.parse(program)
    if debug:
        print(dump(tree, indent=4))
    # return
    # validate.Validator().visit(tree)

    scope_tree_creator = ScopeTreeCreator()
    scope_tree_creator.visit(tree)
    node_scopes = scope_tree_creator.node_scopes

    symbol_definer = SymbolDefiner(node_scopes)
    symbol_definer.visit(tree)

    name_resolver = NameResolver(node_scopes)
    name_resolver.visit(tree)
    bindings = name_resolver.bindings
    if debug:
        print_bindings(bindings)

    class_declarer = ClassTypeDeclarer(node_scopes, bindings)
    class_declarer.visit(tree)
    types = class_declarer.types

    type_annotator = FunctionAndClassTypeAnnotator(node_scopes, bindings, types)
    type_annotator.visit(tree)

    # type_annotator = TypeAnnotator(node_scopes, bindings, types)
    # type_annotator.visit(tree)

    try:
        type_inference = TypeInferrer(node_scopes, bindings, types)
        type_inference.visit(tree)
    finally:
        if debug:
            print(typed_unparse(tree, types))
    return

    translator = CppTranslator(node_scopes, bindings, types)
    translator.visit(tree)
    s = translator.flush()
    return s

    # print(dump(tree, ptypes=ptypes, indent=4))


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


def main():
    file = "input.py"
    result = mypy_pipeline(file)
    codegen = StatementCodegen(result.tree, result.types)
    output = codegen.generate()
    print(output)
    build_and_run(output)


main()
