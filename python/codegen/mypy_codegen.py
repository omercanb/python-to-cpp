"""
Template node visitor for C++ code generation.
Fill in the visit_* methods to generate C++ code.
Separated into expression and statement visitors.
"""

from mypy.nodes import AssignmentStmt, Block, BreakStmt, ClassDef, ContinueStmt
from mypy.nodes import Expression
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import (
    ExpressionStmt,
    ForStmt,
    IndexExpr,
    FuncDef,
    IfStmt,
    MypyFile,
    ReturnStmt,
    WhileStmt,
)
from mypy.traverser import TraverserVisitor
from mypy.types import Type

from python.analysis.find_declarations import get_declarations
from python.codegen.codegen_utils import pointer_to
from python.codegen.expression_codegen import ExpressionCodegen
from python.codegen.for_loop import translate_for_stmt
from python.codegen.translation_utils import (
    access_operator,
    is_truthy,
    translate_func_signature,
)
from python.codegen.typegen import cpp_type, ptr_type, is_pointer

includes = [
    "types.h",
    "truthy.h",
    "iter.h",
    "tuple.h",
    "ptr.h",
    "list.h",
    "dict.h",
    "print.h",
    "scalars.h",
    "mathops.h",
]


class StatementCodegen(TraverserVisitor):
    """Generate C++ code from mypy AST statements."""

    def __init__(
        self,
        tree: MypyFile,
        types_dict: dict[MypyExpression, Type],
    ):
        self.tree = tree
        self.types = types_dict
        self.expr_codegen = ExpressionCodegen(types_dict)
        self.indent_level = 0
        self.output: list[str] = []

    def indent(self):
        self.indent_level += 1

    def unindent(self):
        self.indent_level -= 1

    def indented(self) -> str:
        """Return indentation string."""
        return "    " * self.indent_level

    def emit(self, code: str):
        """Emit a line of code."""
        self.output.append(f"{self.indented()}{code}")

    def visit_block(self, o: Block):
        """Generate code for a block of statements."""
        self.indent()
        super().visit_block(o)
        self.unindent()

    def get_expr(self, expr: Expression, lvalue=False):
        self.expr_codegen.lvalue = lvalue
        return expr.accept(self.expr_codegen)

    def translate_declaration(self, name: str, typ: Type):
        cpp = cpp_type(typ)
        return f"{cpp} {name};"

    def generate_includes(self):
        for include in includes:
            self.emit(f'#include "{include}"')
        self.emit(f"using namespace py;")

    def generate(self) -> str:
        """Generate all C++ code."""
        self.generate_includes()
        self.tree.accept(self)
        return "\n".join(self.output)

    def visit_func_def(self, o: FuncDef):
        """Generate a function or method definition"""
        signature = translate_func_signature(o, self.expr_codegen)
        declarations = get_declarations(o, self.types)
        declaration_lines = [
            self.translate_declaration(name, typ) for name, typ in declarations.items()
        ]

        definition_line = f"{signature} {{"
        self.emit(definition_line)
        self.indent()
        for declaration in declaration_lines:
            self.emit(declaration)
        for stmt in o.body.body:
            stmt.accept(self)
        self.unindent()
        self.emit("}")
        self.emit("")

    def visit_class_def(self, o: ClassDef):
        assert False, "Classdef not yet implemented"

    def visit_assignment_stmt(self, o: AssignmentStmt):
        target = o.lvalues[0]
        rhs = self.get_expr(o.rvalue)
        # a[i] = x goes through __setitem__ rather than assigning to a
        # reference, so dict can insert on a key it doesn't have yet.
        if isinstance(target, IndexExpr):
            base = self.get_expr(target.base)
            index = self.get_expr(target.index)
            access = access_operator(self.types[target.base])
            self.emit(f"{base}{access}__setitem__({index}, {rhs});")
            return
        lhs = self.get_expr(target, lvalue=True)
        self.emit(f"{lhs} = {rhs};")

    def visit_return_stmt(self, o: ReturnStmt):
        if o.expr:
            self.emit(f"return {self.get_expr(o.expr)};")
        else:
            self.emit("return;")

    def visit_if_stmt(self, o: IfStmt):
        # Unlike python ast is a list of if, elif, ..., elif, else
        conditions = o.expr
        bodies = o.body
        for i, (condition, body) in enumerate(zip(conditions, bodies)):
            condition_cpp = self.get_expr(condition)
            if i == 0:
                self.emit(f"if ({is_truthy(condition_cpp)}) {{")
            else:
                self.emit(f"}} else if ({is_truthy(condition_cpp)}) {{")
            self.visit_block(body)
        if o.else_body:
            self.emit("} else {")
            self.visit_block(o.else_body)
        self.emit("}")

    def visit_for_stmt(self, o: ForStmt):
        translate_for_stmt(self, o)

    def visit_while_stmt(self, o: WhileStmt):
        self.emit("// While loop")
        self.emit(f"while ({is_truthy(self.get_expr(o.expr))}) {{")
        self.visit_block(o.body)
        self.emit("}")

    def visit_expression_stmt(self, o: ExpressionStmt):
        self.emit(f"{self.get_expr(o.expr)};")

    def visit_break_stmt(self, _: BreakStmt):
        self.emit("break;")

    def visit_continue_stmt(self, _: ContinueStmt):
        self.emit("continue;")
