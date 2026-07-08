import ast
import types
import typing
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp

import name_resolution
import scope
import symbol_declaration
import validate
from formatting import *
from name_resolution import NameResolver
from scope import ScopeTracker, ScopeTreeCreator, ScopeType
from symbol_declaration import SymbolDefiner
from type_inference import ClassTypeDeclarer, FunctionAndClassTypeAnnotator
from utils import build_and_run, dump

ANNOTATION_TYPES = {
    "int": int,
    "float": float,
    "bool": bool,
    "str": str,
}

includes = ["print.h", "list.h", "ptr.h"]


def pipeline(program: str):
    tree = ast.parse(program)
    # print(dump(tree, indent=4))
    # validate.Validator().visit(tree)

    scope_tree_creator = ScopeTreeCreator()
    scope_tree_creator.visit(tree)
    node_scopes = scope_tree_creator.node_scopes
    print_scopes_of_all_symbols(node_scopes)

    symbol_definer = SymbolDefiner(node_scopes)
    symbol_definer.visit(tree)

    name_resolver = NameResolver(node_scopes)
    name_resolver.visit(tree)
    bindings = name_resolver.bindings

    class_declarer = ClassTypeDeclarer(node_scopes, bindings)
    class_declarer.visit(tree)
    types = class_declarer.types

    type_annotator = FunctionAndClassTypeAnnotator(node_scopes, bindings, types)
    type_annotator.visit(tree)


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


class ScopeTester(ast.NodeVisitor):
    def __init__(self, scope):
        self.scope_tracker = scope.ScopeTracker()

    def visit(self, node: ast.AST):
        cur_scope = self.scope_tracker.scope
        self.scope_tracker.update(node)
        new_scope = self.scope_tracker.scope
        if cur_scope != new_scope:
            if hasattr(node, "lineno"):
                print(node.lineno)
            self.scope_tracker.scope.print_self()
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Name(self, node: ast.Name):
        if not isinstance(node.ctx, ast.Load):
            return
        res = self.scope_tracker.scope.resolve(node.id)
        if not isinstance(res, symbols.Builtin):
            symbol_type, definition_node = res
            print(
                f"Resolve {ast.unparse(node)} on line {node.lineno}, definition on {definition_node.lineno or 'unkown'}: {ast.unparse(definition_node)}"
            )


@dataclass
class CppTranslator:
    types: dict[ast.AST, type]
    current_scope = ScopeType.MODULE
    prev_scope = None

    def new_scope(self, scope_type: ScopeType):
        self.prev_scope = self.current_scope
        self.current_scope = scope_type

    def old_scope(self):
        self.current_scope = self.prev_scope

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise ValueError(f"No support for {node}")
        return visitor(node)

    def visit_Module(self, node: ast.Module):
        s = "#include <iostream>\n"
        for include in includes:
            s += f'#include "{include}"\n'
        s += f"using namespace py;"
        s += "\n"
        s += "\n\n".join(self.visit(child) or "" for child in node.body)
        return s

    def visit_Expr(self, node: ast.Expr):
        return f"{self.visit(node.value)};"

    def visit_Call(self, node: ast.Call):
        s = ""
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            s += "print("
        else:
            s += f"{self.visit(node.func)}("
        s += ", ".join(self.visit(arg) for arg in node.args)
        s += ")"
        return s

    def visit_AnnAssign(self, node: ast.AnnAssign):
        return self.translate_assign([node.target], node.value)

    def visit_Assign(self, node: ast.Assign):
        return self.translate_assign(node.targets, node.value)

    def translate_assign(self, targets: list[ast.expr], value: ast.expr | None):
        assert len(targets) == 1
        target = targets[0]
        assert isinstance(target, ast.Name)
        s = ""
        if target.is_declaration:
            s += f"{cpp_type(self.types[target])} "
        s += f"{target.id}"
        if value is not None:
            s += f"= {self.visit(value)}"
        s += ";"
        return s

    def visit_AugAssign(self, node: ast.AugAssign):
        return f"{self.visit(node.target)} {cpp_op(node.op)}= {self.visit(node.value)};"

    def visit_Constant(self, node: ast.Constant):
        return f"{node.value}"

    def visit_BinOp(self, node: ast.BinOp):
        return f"({self.visit(node.left)} {cpp_op(node.op)} {self.visit(node.right)})"

    def visit_Name(self, node: ast.Name):
        return f"{node.id}"

    def visit_If(self, node: ast.If):
        s = ""
        # Hack to make it so we don't parenthesize the bool op twice
        if isinstance(node.test, ast.BoolOp):
            s += f"if {self.visit(node.test)} {{\n"
        else:
            s += f"if ({self.visit(node.test)}) {{\n"
        for stmt in node.body:
            s += f"{self.visit(stmt)}\n"
        if node.orelse:
            s += "} else {\n"
            for stmt in node.orelse:
                s += f"{self.visit(stmt)}\n"
        s += "}\n"
        return s

    def visit_IfExp(self, node: ast.IfExp):
        # Need to parenthesize because precedence of ternary is low in c++
        return f"({self.visit(node.test)} ? {self.visit(node.body)} : {self.visit(node.orelse)})"

    # Currently this is not quite right because an if(x) in python will use a truthiness condition while in c++ it may be different
    # For when we have only number types though, this is fine
    def visit_BoolOp(self, node: ast.BoolOp):
        s = "("
        s += f" {cpp_op(node.op)} ".join(self.visit(expr) for expr in node.values)
        s += ")"
        return s

    def visit_Compare(self, node: ast.Compare):
        # In python comparisons can be chained like a <= b < c
        # We need to convert that to (a <= b) && (b <= c)
        assert len(node.ops) >= 1
        assert len(node.ops) == len(node.comparators)
        for op in node.ops:
            assert is_cpp_op(op)
        # If there is just one comparison we don't need to parenthesize
        if len(node.ops) == 1:
            s = f"{self.visit(node.left)} {cpp_op(node.ops[0])} {self.visit(node.comparators[0])}"
        else:
            s = f"({self.visit(node.left)} {cpp_op(node.ops[0])} {self.visit(node.comparators[0])})"
            for i in range(1, len(node.ops)):
                s += f" && ({self.visit(node.comparators[i-1])} {cpp_op(node.ops[i])} {self.visit(node.comparators[i])})"
        return s

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.new_scope(ScopeType.FUNCTION)
        s = ""
        if node.name == "main":
            s += "int main() {\n"
        else:
            function_type = self.types[node]
            return_type = function_type.__args__[-1]
            argument_types = function_type.__args__[:-1]
            s += f"{cpp_type(return_type)} {node.name}("
            s += ", ".join(
                f"{cpp_type(arg_type)} {arg.arg}"
                for arg_type, arg in zip(argument_types, node.args.args)
            )
            s += ") {\n"
        for stmt in node.body:
            s += f"{self.visit(stmt)}\n"
        s += "}\n\n "
        self.old_scope()
        return s

    def visit_Return(self, node: ast.Return):
        if node.value:
            return f"return {self.visit(node.value)};"
        else:
            return f"return;"

    def visit_While(self, node: ast.While):
        s = f"while ({self.visit(node.test)}) {{\n"
        for stmt in node.body:
            s += f"{self.visit(stmt)}\n"
        s += "}\n"
        return s

    def visit_Break(self, node: ast.Break):
        return "break;"

    def visit_Continue(self, node: ast.Continue):
        return "continue;"

    def visit_For(self, node: ast.For):
        pass

    def visit_List(self, node: ast.List):
        s = "ptr(new list({"
        s += ", ".join(self.visit(element) for element in node.elts)
        s += "}))"
        return s

    def visit_ClassDef(self, node: ast.ClassDef):
        self.new_scope(ScopeType.CLASS)
        for stmt in node.body:
            self.visit(stmt)
        self.old_scope()

    pass


is_object = defaultdict(lambda: False)
is_object[list] = True

# Python type  ->  C++ type
cpp_types = {
    int: "int",
    float: "double",
    bool: "bool",
    str: "std::string",
    type(None): "void",
    list: "list",
}


def cpp_type(typ: type) -> str:
    s = ""
    # The type is a subscripted type like list[int]
    if isinstance(typ, types.GenericAlias):
        args = typing.get_args(typ)
        origin = typing.get_origin(typ)
        # Building the C++ type template
        s = ""
        if is_object[origin]:  # Objects need to be refcounted
            s += "ptr<"
        s += f"{cpp_types[origin]}<"
        s += ", ".join(cpp_type(arg) for arg in args)
        s += ">"
        if is_object[origin]:
            s += ">"

        return s
    else:
        try:
            return cpp_types[typ]
        except KeyError:
            raise NotImplementedError(f"no C++ mapping for {typ.__name__}")


# AST operator class  ->  C++ symbol
CPP_OPS = {
    # arithmetic (ast.BinOp)
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",  # NOTE: semantics differ
    ast.Mod: "%",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    # comparison (ast.Compare)
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    # boolean (ast.BoolOp)
    ast.And: "&&",
    ast.Or: "||",
    # unary (ast.UnaryOp)
    ast.UAdd: "+",
    ast.USub: "-",
    ast.Not: "!",
    ast.Invert: "~",
}


def cpp_op(op):
    try:
        return CPP_OPS[type(op)]
    except KeyError:
        raise NotImplementedError(f"no C++ mapping for {type(op).__name__}")


def is_cpp_op(op):
    return type(op) in CPP_OPS


main()
