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
    PassStmt,
    ReturnStmt,
    StrExpr,
    UnaryExpr,
    WhileStmt,
)
from mypy.traverser import TraverserVisitor
from mypy.types import (
    AnyType,
    Instance,
    NoneType,
    ProperType,
    TupleType,
    Type,
    UnionType,
    get_proper_type,
)
from mypy.visitor import ExpressionVisitor, NodeVisitor

from python.codegen.codegen_utils import list_of


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

    def get_expr(self, o: Expression) -> str:
        return o.accept(self.expr_codegen)

    def indent(self) -> str:
        """Return indentation string."""
        return "  " * self.indent_level

    def emit(self, code: str):
        """Emit a line of code."""
        self.output.append(f"{self.indent()}{code}")

    def get_type_string(self, node: MypyExpression) -> str:
        """Get C++ type string for a mypy type."""
        if node in self.types:
            t = get_proper_type(self.types[node])
            return str(t)
        return "auto"

    def visit_func_def(self, o: FuncDef):
        """Generate a function or method definition"""
        is_method = o.info is not None
        if is_method:
            self.generate_method_def(o)
        else:
            self.generate_func_def(o)

    def visit_class_def(self, o: ClassDef):
        """Generate C++ class definition.

        Args:
            o.info: class type information
        """
        self.emit(f"// Class: {o.name}")
        # TODO: Generate C++ struct/class
        super().visit_class_def(o)

    def generate_method_def(self, o: FuncDef):
        """Generate C++ method definition.

        Similar to visit_func_def, but handle 'self' parameter.
        """
        # TODO: Generate C++ method
        pass

    def generate_func_def(self, o: FuncDef):
        pass

    # ============================================================
    # STATEMENTS
    # ============================================================

    def visit_block(self, o: Block):
        """Generate code for a block of statements."""
        self.indent_level += 1
        super().visit_block(o)
        self.indent_level -= 1

    def visit_assignment_stmt(self, o: AssignmentStmt):
        """Generate C++ assignment.

        Args:
            o.lvalues: what's being assigned to
            o.rvalue: what's being assigned
        """
        # TODO: Handle assignment (e.g., x = 5)
        self.emit(f"// Assignment")
        super().visit_assignment_stmt(o)

    def visit_return_stmt(self, o: ReturnStmt):
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

    def visit_if_stmt(self, o: IfStmt):
        """Generate C++ if/else statement.

        Args:
            o.expr: list of condition expressions
            o.body: list of body blocks (one per condition)
            o.else_body: optional else block
        """
        # TODO: Generate if statement
        self.emit("// If statement")
        super().visit_if_stmt(o)

    def visit_for_stmt(self, o: ForStmt):
        """Generate C++ for loop.

        Args:
            o.index: loop variable
            o.expr: what to iterate over
            o.body: loop body
        """
        # TODO: Generate for loop (e.g., for x in items:)
        self.emit("// For loop")
        super().visit_for_stmt(o)

    def visit_while_stmt(self, o: WhileStmt):
        """Generate C++ while loop.

        Args:
            o.expr: condition
            o.body: loop body
        """
        # TODO: Generate while loop
        self.emit("// While loop")
        super().visit_while_stmt(o)

    def visit_expression_stmt(self, o: ExpressionStmt):
        self.emit(self.get_expr(o.expr))

    def visit_break_stmt(self, _: BreakStmt):
        self.emit("break;")

    def visit_continue_stmt(self, _: ContinueStmt):
        self.emit("continue;")

    # ============================================================
    # UTILITIES
    # ============================================================

    def generate(self) -> str:
        """Generate all C++ code."""
        self.tree.accept(self)
        return "\n".join(self.output)


def ptr_type(t: str) -> str:
    return f"ptr<{t}>"


def cpp_type(t: Type) -> str:
    """Convert a mypy type to C++ type string.

    Uses pattern matching to handle different type kinds.
    """
    t = get_proper_type(t)

    match t:
        # Builtin types
        case Instance(type=type_info) if type_info.fullname == "builtins.int":
            return "int"
        case Instance(type=type_info) if type_info.fullname == "builtins.float":
            return "double"
        case Instance(type=type_info) if type_info.fullname == "builtins.str":
            return "std::string"
        case Instance(type=type_info) if type_info.fullname == "builtins.bool":
            return "bool"

        # Container types
        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.list" and args
        ):
            elem_type = cpp_type(args[0])
            return ptr_type(f"list<{elem_type}>")

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.dict" and len(args) >= 2
        ):
            key_type = cpp_type(args[0])
            val_type = cpp_type(args[1])
            return ptr_type(f"dict<{key_type}, {val_type}>")

        case Instance(type=type_info, args=args) if (
            type_info.fullname == "builtins.set" and args
        ):
            elem_type = cpp_type(args[0])
            return ptr_type(f"set<{elem_type}>")

        # Tuple with fixed elements
        case TupleType(items=items):
            elem_types = ", ".join(cpp_type(item) for item in items)
            return f"tuple<{elem_types}>"

        # Optional[T] = T | None
        case UnionType(items=items) if len(items) == 2 and any(
            isinstance(item, NoneType) for item in items
        ):
            non_none = next(item for item in items if not isinstance(item, NoneType))
            inner = cpp_type(non_none)
            return f"std::optional<{inner}>"

        # Generic union
        case UnionType(items=items):
            types = ", ".join(cpp_type(item) for item in items)
            return f"std::variant<{types}>"

        # None/void
        case NoneType():
            return "void"

        # Any type
        case AnyType():
            return "auto"

        # Custom classes
        case Instance(type=type_info):
            return type_info.fullname.replace(".", "::")

        # Iterator/Iterable
        case Instance(type=type_info, args=args) if (
            "Iterator" in type_info.fullname and args
        ):
            elem_type = cpp_type(args[0])
            return f"Iterator<{elem_type}>"

        # Default fallback
        case _:
            assert False, f"Conversion not implemented for type {t}"
