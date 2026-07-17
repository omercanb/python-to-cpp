from python.analysis.name_resolution import NameResolver
from python.analysis.scope import ScopeTreeCreator
from python.analysis.symbol_declaration import SymbolDefiner
from python.analysis.type_annotation import (
    ClassTypeDeclarer,
    FunctionAndClassTypeAnnotator,
)
from python.analysis.type_inference import TypeInferrer
from python.codegen.codegen import CppTranslator
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


def main():
    file = "input.py"
    program = open(file).read()
    s = pipeline(program, debug=True)
    if s:
        build_and_run(s)
    return
    #
    # print(dump(tree, indent=4))
    # # validate.Validator().visit(tree)
    #
    # # scope.ScopeResolver().visit(tree)
    # definer = symbols.SymbolDefiner()
    # definer.visit(tree)
    # definer.scope.print_tree()
    # ScopeTester(definer.scope).visit(tree)
    # return
    #
    # print("inferring")
    # inferrer = type_inference.TypeInferrer()
    # inferrer.visit(tree)
    # ptypes = inferrer.ptypes
    # for k, v in ptypes.items():
    #     print(dump(k), v)
    #
    # translated = CppTranslator(ptypes).visit(tree)
    # build_and_run(translated)


main()
