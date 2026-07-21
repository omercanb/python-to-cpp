"""
Template node visitor for C++ code generation.
Fill in the visit_* methods to generate C++ code.
Separated into expression and statement visitors.
"""

from mypy.nodes import (
    AssignmentStmt,
    Block,
    BreakStmt,
    CallExpr,
    ClassDef,
    ComparisonExpr,
    ContinueStmt,
)
from mypy.nodes import Expression
from mypy.nodes import Expression as MypyExpression
from mypy.nodes import (
    ExpressionStmt,
    FloatExpr,
    ForStmt,
    FuncDef,
    IfStmt,
    IndexExpr,
    IntExpr,
    ListExpr,
    MemberExpr,
    MypyFile,
    NameExpr,
    OpExpr,
    ReturnStmt,
    StrExpr,
    UnaryExpr,
    WhileStmt,
)
from mypy.traverser import TraverserVisitor
from mypy.types import Type
from mypy.visitor import ExpressionVisitor

from python.analysis.find_declarations import get_declarations
from python.codegen.codegen_utils import list_of
from python.codegen.declarations import generate_func_signature
from python.codegen.typegen import cpp_type


class ExpressionCodegen(ExpressionVisitor[str]):
    """Generate C++ code for expressions."""

    def __init__(self, types_dict: dict[MypyExpression, Type]):
        self.types = types_dict

    def visit_name_expr(self, o: NameExpr) -> str:
        return o.name

    def visit_member_expr(self, o: MemberExpr) -> str:
        """Handle attribute access considering wether the object will be a pointer or value"""
        # TODO: Handle attribute access
        obj = o.expr.accept(self)
        return f"{obj}.{o.name}"

    def visit_call_expr(self, o: CallExpr) -> str:
        # TODO consider if we need to worry about the ordering difference between kw arguements in python and arguments in c++
        callee = o.callee.accept(self)
        arguments = [arg.accept(self) for arg in o.args]
        return f"{callee}({', '.join(arguments)})"

    def visit_op_expr(self, o: OpExpr) -> str:
        left = o.left.accept(self)
        right = o.right.accept(self)
        return f"({left} {o.op} {right})"

    def visit_unary_expr(self, o: UnaryExpr) -> str:
        operand = o.expr.accept(self)
        return f"{o.op}{operand}"

    def visit_index_expr(self, o: IndexExpr) -> str:
        base = o.base.accept(self)
        index = o.index.accept(self)
        return f"{base}[{index}]"

    def visit_comparison_expr(self, o: ComparisonExpr) -> str:
        # TODO: Generate comparison
        return "comparison"

    def visit_int_expr(self, o: IntExpr) -> str:
        return str(o.value)

    def visit_str_expr(self, o: StrExpr) -> str:
        return f'"{o.value}"'

    def visit_float_expr(self, o: FloatExpr) -> str:
        return str(o.value)

    def visit_list_expr(self, o: ListExpr) -> str:
        elements = [element.accept(self) for element in o.items]
        return list_of(elements)


includes = ["list.h", "ptr.h"]


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

    def get_expr(self, expr: Expression):
        return expr.accept(self.expr_codegen)

    def translate_declaration(self, name: str, typ: Type):
        return f"{cpp_type(typ)} {name};"

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
        signature = generate_func_signature(o, self.expr_codegen)
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
        lhs = self.get_expr(o.lvalues[0])
        rhs = self.get_expr(o.rvalue)
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
                self.emit(f"if ({condition_cpp}) {{")
            else:
                self.emit(f"}} else if ({condition_cpp}) {{")
            self.visit_block(body)
        if o.else_body:
            self.emit("} else {")
            self.visit_block(o.else_body)
        self.emit("}")

    def visit_for_stmt(self, _: ForStmt):
        assert False, "For loop not yet implemented"

    def visit_while_stmt(self, o: WhileStmt):
        self.emit("// While loop")
        self.emit(f"while ({self.get_expr(o.expr)}) {{")
        self.visit_block(o.body)
        self.emit("}")

    def visit_expression_stmt(self, o: ExpressionStmt):
        self.emit(self.get_expr(o.expr))

    def visit_break_stmt(self, _: BreakStmt):
        self.emit("break;")

    def visit_continue_stmt(self, _: ContinueStmt):
        self.emit("continue;")
