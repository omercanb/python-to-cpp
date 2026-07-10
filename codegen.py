import ast
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field

from formatting import get_scope_identifier, get_type_name
from name_resolution import BindingTable
from py_types import (
    ClassType,
    FunctionType,
    MethodType,
    PyType,
    RangeType,
    TypeTable,
    is_object,
)
from scope import Scope, ScopeType, ScopingNodeVisitor

includes = ["print.h", "list.h", "ptr.h", "range.h"]


@dataclass
class DeclarationMarker:
    scope: Scope
    indent: int


@dataclass
class CppTranslator(ScopingNodeVisitor):
    def __init__(self, node_scopes, bindings: BindingTable, types: TypeTable):
        super().__init__(node_scopes)
        self.bindings = bindings
        self.types = types
        self.indent_level: int = 0
        self.output: list[str | DeclarationMarker] = []
        self.includes: list[str] = []
        # A map of indices in the output list to where declarations should go
        self.declarations: dict[Scope, list[str]] = defaultdict(list)
        self.marked_scopes: set[Scope] = set()
        self.current_self_name: str | None = None

    def commas(self, lst: list[ast.AST]):
        return ", ".join(self.visit(node) for node in lst)

    def indent(self):
        self.indent_level += 4

    def unindent(self):
        self.indent_level -= 4

    def stmt(self, string=""):
        self.output.append(f'{self.indent_level * " "}{string}')

    def include(self, string):
        self.includes.append(string)

    def flush(self):
        s = ""
        for include in self.includes:
            s += include + "\n"
        s += "\n"
        for item in self.output:
            if isinstance(item, DeclarationMarker):
                declarations = self.declarations[item.scope]
                for declaration in declarations:
                    s += f'{" " * item.indent}{declaration}\n'
                if declarations:
                    s += "\n"
            else:
                s += item + "\n"
        return s

    def declaration_marker(self):
        scope = self.scope()
        if scope not in self.marked_scopes:
            self.marked_scopes.add(scope)
            # Because a function def is still in the module scope, we first enter the scope then put the declaration market
            # Because of this, out current position ends up being one after the starting line of the scope, so we mitigate this
            self.output.append(DeclarationMarker(scope, self.indent_level))

    def add_declaration(self, node: ast.AST):
        match node:
            case ast.Name():
                declaration = self.get_var_declaration(node)
            case ast.FunctionDef():
                declaration = self.get_func_declaration(node)
            case ast.ClassDef():
                declaration = self.get_class_declaration(node)
            case _:
                assert False
        self.declarations[self.scope()].append(declaration)

    def get_var_declaration(self, node: ast.Name):
        typ = self.types[node]
        return f"{cpp_type(typ)} {node.id};"

    def get_func_declaration(self, node: ast.FunctionDef):
        typ = self.types[node]
        assert isinstance(typ, FunctionType)
        return f"{get_function_signature(typ)};"

    def get_class_declaration(self, node: ast.ClassDef):
        typ = self.types[node]
        assert isinstance(typ, ClassType)
        return f"{get_class_signature(typ)};"

    @contextmanager
    def method_self(self, node: ast.FunctionDef):
        # first parameter of a method/constructor is `self`
        saved = self.current_self_name
        self.current_self_name = node.args.args[0].arg
        try:
            yield
        finally:
            self.current_self_name = saved

    def visit_Module(self, node: ast.Module):
        self.include("#include <iostream>")
        for include in includes:
            self.include(f'#include "{include}"')
        self.include(f"using namespace py;\n")
        self.declaration_marker()
        for child in node.body:
            self.visit(child)

    def emit_body(self, node: ast.FunctionDef):
        self.indent()
        # We have to do something pretty hacky here
        # Since in a function declaration we don't know the function scope until we've stepped into the function, we need to first step into the funciton, then place the declaration marker
        # But since the first statement could have filled out the output we need to move to where the first stmt finished
        current_output = self.output
        self.output = []
        for stmt in node.body:
            self.visit(stmt)
            if stmt == node.body[0]:
                new_output = self.output
                self.output = current_output
                self.declaration_marker()
                self.output.extend(new_output)

        self.unindent()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func = self.types[node]
        assert isinstance(func, FunctionType)
        if self.scope().typ != ScopeType.CLASS:
            self.add_declaration(node)
        self.stmt(f"{get_function_signature(func)} {{")
        self.emit_body(node)
        self.stmt("}\n")

    def visit_ClassDef(self, node: ast.ClassDef):
        cls = self.types[node]
        assert isinstance(cls, ClassType)
        self.add_declaration(node)
        self.stmt(f"{get_class_signature(cls)} {{")
        self.stmt("public:")
        self.indent()

        for field_name, field_type in cls.fields.items():
            self.stmt(f"{cpp_type(field_type)} {field_name};")
        self.stmt()

        if cls.constructor is not None:
            self.stmt(f"{get_constructor_signature(cls, cls.constructor)} {{")
            with self.method_self(cls.constructor.node):
                self.emit_body(cls.constructor.node)
            self.stmt("}")
            self.stmt()

        for method in cls.methods:
            self.stmt(f"{get_method_signature(method)} {{")
            with self.method_self(method.node):
                self.emit_body(method.node)
            self.stmt("}")
            self.stmt()
        self.unindent()
        self.stmt("};")

    def visit_Return(self, node: ast.Return):
        if node.value:
            self.stmt(f"return {self.visit(node.value)};")
        else:
            self.stmt(f"return;")

    def visit_While(self, node: ast.While):
        self.stmt(f"while ({self.visit(node.test)}) {{")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.unindent()
        self.stmt("}")

    def visit_Break(self, node: ast.Break):
        self.stmt("break;")

    def visit_Continue(self, node: ast.Continue):
        self.stmt("continue;")

    def visit_For(self, node: ast.For):
        assert isinstance(node.target, ast.Name)
        self.test_declare_name(node.target)
        target = self.visit(node.target)
        iterable = self.visit(node.iter)
        var = f"{node.target.id}__iter"
        for_line = f"for (auto {var} = iter({iterable}); !{var}.done();)"
        self.stmt(f"{for_line} {{")
        self.indent()
        self.stmt(f"{target} = next({var});")
        for child in node.body:
            self.visit(child)
        self.unindent()
        self.stmt("}")

    def visit_If(self, node: ast.If):
        # Hack to make it so we don't parenthesize the bool op twice
        if isinstance(node.test, ast.BoolOp):
            self.stmt(f"if {self.visit(node.test)} {{")
        else:
            self.stmt(f"if ({self.visit(node.test)}) {{")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.unindent()
        if node.orelse:
            self.stmt("} else {")
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.unindent()
        self.stmt("}")

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.stmt(self.translate_assign([node.target], node.value))

    def visit_Assign(self, node: ast.Assign):
        self.stmt(self.translate_assign(node.targets, node.value))

    def visit_Expr(self, node: ast.Expr):
        self.stmt(f"{self.visit(node.value)};")

    def visit_Attribute(self, node: ast.Attribute):
        value_node = node.value
        if isinstance(value_node, ast.Name) and value_node.id == self.current_self_name:
            return f"this->{node.attr}"  # self.x -> this->x
        return f"{self.visit(value_node)}->{node.attr}"  # obj.x -> obj->x

    def visit_Subscript(self, node: ast.Subscript):
        if isinstance(node.slice, ast.Slice):
            raise NotImplementedError("slice subscription (a[i:j]) not supported")
        value = self.visit(node.value)
        index = self.visit(node.slice)
        return f"{value}[{index}]"
        # return f"(*{value})[{index}]"  # deref the ptr, then operator[] on the list

    def visit_Call(self, node: ast.Call):
        s = ""
        builtin_funcs = ["print", "len"]
        if isinstance(node.func, ast.Name) and node.func.id in builtin_funcs:
            s += f"{node.func.id}("
        else:
            call = self.visit(node.func)
            s += f"{call}("
        s += self.commas(node.args)
        s += ")"
        if is_object(self.types[node.func]):
            s = pointer_to(s)
        return s

    def visit_Name(self, node: ast.Name):
        if node.id == self.current_self_name:
            return "this"
        return node.id

    def visit_Constant(self, node: ast.Constant):
        value = node.value
        if isinstance(value, bool):  # before int — bool is a subclass of int
            return "true" if value else "false"
        if isinstance(value, str):
            return f'"{value}"'  # plus escaping for embedded quotes/newlines
        if value is None:
            return "nullptr"  # or however ptr.h spells null
        return f"{value}"

    def visit_AugAssign(self, node: ast.AugAssign):
        self.stmt(
            f"{self.visit(node.target)} {cpp_op(node.op)}= {self.visit(node.value)};"
        )

    def visit_IfExp(self, node: ast.IfExp):
        # Need to parenthesize because precedence of ternary is low in c++
        return f"({self.visit(node.test)} ? {self.visit(node.body)} : {self.visit(node.orelse)})"

    def visit_BinOp(self, node: ast.BinOp):
        return f"({self.visit(node.left)} {cpp_op(node.op)} {self.visit(node.right)})"

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

    def visit_List(self, node: ast.List):
        typ = self.types.get(node)
        if isinstance(typ, ListType):
            elem = cpp_type(typ.element_type)
        else:
            # no inferred element type (e.g. bare literal not tied to a decl):
            # fall back to the first element's type, or error
            raise PyToCppError(node, "cannot determine list element type")
        elements = self.commas(node.elts)
        list = f"list<{elem}>({{{elements}}})"
        return pointer_to(list)

    def translate_assign(self, targets: list[ast.expr], value: ast.expr | None):
        assert len(targets) == 1
        target = targets[0]
        # Check if it's a declaration
        if isinstance(target, ast.Name):
            self.test_declare_name(target)
        s = f"{self.visit(target)}"
        if value is not None:
            s += f" = {self.visit(value)}"
        s += ";"
        return s

    def test_declare_name(self, name: ast.Name):
        print("HERE", name)
        if self.bindings[name].node == name:
            self.add_declaration(name)


def commas(lst):
    return ", ".join(lst)


def _params(arg_nodes: list[ast.arg], arg_types: list[PyType]) -> str:
    assert len(arg_nodes) == len(arg_types)
    return ", ".join(f"{cpp_type(t)} {a.arg}" for a, t in zip(arg_nodes, arg_types))


def get_function_signature(f: FunctionType) -> str:
    assert isinstance(f.node, ast.FunctionDef)
    params = _params(f.node.args.args, f.argument_types)
    return f"{cpp_type(f.return_type)} {f.name}({params})"


def get_method_signature(m: MethodType) -> str:
    assert isinstance(m.node, ast.FunctionDef)
    params = _params(m.node.args.args[1:], m.argument_types)
    return f"{cpp_type(m.return_type)} {m.name}({params})"


def get_constructor_signature(cls: ClassType, ctor: MethodType) -> str:
    assert isinstance(ctor.node, ast.FunctionDef)
    params = _params(ctor.node.args.args[1:], ctor.argument_types)
    return f"{cls.name}({params})"


def get_class_signature(c: ClassType):
    s = f"class {c.name}"
    return s


from functools import singledispatch

from py_types import (
    BuiltinType,
    ClassType,
    FunctionType,
    ListType,
    MethodType,
    PyType,
    SliceType,
    UnknownType,
)

CPP_SCALAR_TYPES = {
    int: "int",
    float: "double",
    bool: "bool",
    str: "std::string",
    None: "void",
    type(None): "void",
}

CPP_CONTAINER_TYPES = {
    list: "list",
    # dict: "dict",
    # set: "set",
    # tuple: "tuple",
}


def pointer_to(item: str) -> str:
    return f"ptr(new {item})"


@singledispatch
def cpp_type(typ: PyType) -> str:
    raise NotImplementedError(f"no C++ mapping for {typ!r}")


@cpp_type.register
def _(typ: BuiltinType) -> str:
    try:
        return CPP_SCALAR_TYPES[typ.builtin]
    except (KeyError, TypeError):
        raise NotImplementedError(f"no C++ mapping for builtin {typ.builtin!r}")


@cpp_type.register
def _(typ: RangeType) -> str:
    return f"range"


@cpp_type.register
def _(typ: ListType) -> str:
    return f"ptr<list<{cpp_type(typ.element_type)}>>"


@cpp_type.register
def _(typ: ClassType) -> str:
    return f"ptr<{typ.name}>"


@cpp_type.register
def _(typ: FunctionType) -> str:
    ret = cpp_type(typ.return_type)
    args = ", ".join(cpp_type(a) for a in typ.argument_types)
    return f"std::function<{ret}({args})>"


@cpp_type.register
def _(typ: UnknownType) -> str:
    raise NotImplementedError("cannot emit C++ for an unresolved (unknown) type")


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
