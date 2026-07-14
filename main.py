from python.analysis.name_resolution import NameResolver
from python.analysis.scope import ScopeTreeCreator
from python.analysis.symbol_declaration import SymbolDefiner
from python.analysis.type_inference import (
    ClassTypeDeclarer,
    FunctionAndClassTypeAnnotator,
    TypeInferrer,
)
from python.codegen.codegen import CppTranslator
from python.formatting import *
from python.utils import build_and_run, dump

includes = ["print.h", "list.h", "ptr.h"]


def pipeline(program: str):
    tree = ast.parse(program)
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
        print(typed_unparse(tree, types))

    translator = CppTranslator(node_scopes, bindings, types)
    translator.visit(tree)
    s = translator.flush()
    build_and_run(s)

    # print(dump(tree, types=types, indent=4))


def main():
    file = "input.py"
    program = open(file).read()
    pipeline(program)
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
    # types = inferrer.types
    # for k, v in types.items():
    #     print(dump(k), v)
    #
    # translated = CppTranslator(types).visit(tree)
    # build_and_run(translated)


main()
