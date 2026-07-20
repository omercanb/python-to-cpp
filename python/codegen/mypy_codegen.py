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
    DictExpr,
)
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
    PassStmt,
    ReturnStmt,
    StrExpr,
    UnaryExpr,
    WhileStmt,
)
from mypy.traverser import TraverserVisitor
from mypy.types import Type, get_proper_type
from mypy.visitor import ExpressionVisitor, NodeVisitor


class ExpressionCodegen(ExpressionVisitor[str]):
    """Generate C++ code for expressions."""

    def __init__(self, types_dict: dict[MypyExpression, Type]):
        self.types = types_dict

    def get_type_string(self, node: MypyExpression) -> str:
        """Get C++ type string for a mypy type."""
        if node in self.types:
            t = get_proper_type(self.types[node])
            return str(t)
        return "auto"

    def visit_name_expr(self, o: NameExpr) -> str:
        """Handle variable references.

        Args:
            o.name: variable name
            o.node: what it resolves to
        """
        # TODO: Generate C++ code for variable reference
        return o.name

    def visit_member_expr(self, o: MemberExpr) -> str:
        """Handle attribute access (obj.attr).

        Args:
            o.expr: the object
            o.name: the attribute name
        """
        # TODO: Handle attribute access
        obj = o.expr.accept(self)
        return f"{obj}.{o.name}"

    def visit_call_expr(self, o: CallExpr) -> str:
        """Handle function calls.

        Args:
            o.callee: function being called
            o.args: arguments
            o.arg_names: keyword argument names
        """
        # TODO: Generate function call
        return "call()"

    def visit_op_expr(self, o: OpExpr) -> str:
        """Handle binary operations.

        Args:
            o.op: operator (+, -, *, /, etc.)
            o.left: left operand
            o.right: right operand
        """
        # TODO: Generate binary operation
        left = o.left.accept(self)
        right = o.right.accept(self)
        return f"({left} {o.op} {right})"

    def visit_unary_expr(self, o: UnaryExpr) -> str:
        """Handle unary operations.

        Args:
            o.op: operator (-, +, ~, not)
            o.operand: the operand
        """
        # TODO: Generate unary operation
        operand = o.expr.accept(self)
        return f"{o.op}{operand}"

    def visit_index_expr(self, o: IndexExpr) -> str:
        """Handle subscripting (arr[idx]).

        Args:
            o.base: the container
            o.index: the index
        """
        # TODO: Generate subscript
        base = o.base.accept(self)
        index = o.index.accept(self)
        return f"{base}[{index}]"

    def visit_comparison_expr(self, o: ComparisonExpr) -> str:
        """Handle comparisons (a == b, a < b, etc.).

        Args:
            o.operators: list of operators
            o.operands: list of operands
        """
        # TODO: Generate comparison
        return "comparison"

    def visit_int_expr(self, o: IntExpr) -> str:
        """Handle integer literals."""
        return str(o.value)

    def visit_str_expr(self, o: StrExpr) -> str:
        """Handle string literals."""
        return f'"{o.value}"'

    def visit_float_expr(self, o: FloatExpr) -> str:
        """Handle float literals."""
        return str(o.value)

    def visit_list_expr(self, o: ListExpr) -> str:
        """Handle list literals."""
        # TODO: Generate list literal
        return "[]"

    def visit_dict_expr(self, o: DictExpr) -> str:
        """Handle dict literals."""
        # TODO: Generate dict literal
        return "{}"


class StatementCodegen(TraverserVisitor):
    """Generate C++ code from mypy AST statements."""

    def __init__(
        self,
        tree: MypyFile,
        types_dict: dict[MypyExpression, Type],
        expr_codegen: ExpressionCodegen | None = None,
    ):
        self.tree = tree
        self.types = types_dict
        self.expr_codegen = expr_codegen or ExpressionCodegen(types_dict)
        self.indent_level = 0
        self.output: list[str] = []

    def indent(self) -> str:
        """Return indentation string."""
        return "  " * self.indent_level

    def emit(self, code: str) -> None:
        """Emit a line of code."""
        self.output.append(f"{self.indent()}{code}")

    def get_type_string(self, node: MypyExpression) -> str:
        """Get C++ type string for a mypy type."""
        if node in self.types:
            t = get_proper_type(self.types[node])
            return str(t)
        return "auto"

    # ============================================================
    # TOP-LEVEL DEFINITIONS
    # ============================================================

    def visit_func_def(self, o: FuncDef) -> None:
        """Generate C++ function definition.

        Args:
            o.type.ret_type: return type
            o.type.arg_names: parameter names
            o.type.arg_types: parameter types
            o.body: function body
        """
        if o.info:
            # This is a method
            self.visit_method(o)
        else:
            # This is a module-level function
            self.emit(f"// Function: {o.name}")
            # TODO: Generate C++ function
            super().visit_func_def(o)

    def visit_class_def(self, o: ClassDef) -> None:
        """Generate C++ class definition.

        Args:
            o.info: class type information
        """
        self.emit(f"// Class: {o.name}")
        # TODO: Generate C++ struct/class
        super().visit_class_def(o)

    def visit_method(self, o: FuncDef) -> None:
        """Generate C++ method definition.

        Similar to visit_func_def, but handle 'self' parameter.
        """
        # TODO: Generate C++ method
        pass

    # ============================================================
    # STATEMENTS
    # ============================================================

    def visit_block(self, o: Block) -> None:
        """Generate code for a block of statements."""
        self.indent_level += 1
        super().visit_block(o)
        self.indent_level -= 1

    def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
        """Generate C++ assignment.

        Args:
            o.lvalues: what's being assigned to
            o.rvalue: what's being assigned
        """
        # TODO: Handle assignment (e.g., x = 5)
        self.emit(f"// Assignment")
        super().visit_assignment_stmt(o)

    def visit_return_stmt(self, o: ReturnStmt) -> None:
        """Generate C++ return statement.

        Args:
            o.expr: the return value (can be None)
        """
        # TODO: Generate return statement
        if o.expr:
            expr_code = o.expr.accept(self.expr_codegen)
            self.emit(f"return {expr_code};")
        else:
            self.emit("return;")
        super().visit_return_stmt(o)

    def visit_if_stmt(self, o: IfStmt) -> None:
        """Generate C++ if/else statement.

        Args:
            o.expr: list of condition expressions
            o.body: list of body blocks (one per condition)
            o.else_body: optional else block
        """
        # TODO: Generate if statement
        self.emit("// If statement")
        super().visit_if_stmt(o)

    def visit_for_stmt(self, o: ForStmt) -> None:
        """Generate C++ for loop.

        Args:
            o.index: loop variable
            o.expr: what to iterate over
            o.body: loop body
        """
        # TODO: Generate for loop (e.g., for x in items:)
        self.emit("// For loop")
        super().visit_for_stmt(o)

    def visit_while_stmt(self, o: WhileStmt) -> None:
        """Generate C++ while loop.

        Args:
            o.expr: condition
            o.body: loop body
        """
        # TODO: Generate while loop
        self.emit("// While loop")
        super().visit_while_stmt(o)

    def visit_expression_stmt(self, o: ExpressionStmt) -> None:
        """Generate C++ expression statement.

        Args:
            o.expr: the expression
        """
        # TODO: Generate expression (usually a function call)
        self.emit("// Expression statement")
        super().visit_expression_stmt(o)

    def visit_pass_stmt(self, _o: PassStmt) -> None:
        """Skip pass statements (they generate nothing in C++)."""
        pass

    def visit_break_stmt(self, _o: BreakStmt) -> None:
        """Generate C++ break."""
        self.emit("break;")

    def visit_continue_stmt(self, _o: ContinueStmt) -> None:
        """Generate C++ continue."""
        self.emit("continue;")

    # ============================================================
    # UTILITIES
    # ============================================================

    def generate(self) -> str:
        """Generate all C++ code."""
        self.tree.accept(self)
        return "\n".join(self.output)
