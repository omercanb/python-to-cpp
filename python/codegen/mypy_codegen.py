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
    FuncDef,
    IfStmt,
    IndexExpr,
    MypyFile,
    RaiseStmt,
    ReturnStmt,
    SymbolTable,
    TryStmt,
    Var,
    WhileStmt,
)
from mypy.types import Type

from python.analysis.find_declarations import get_declarations
from python.codegen.class_def import translate_class_def
from python.codegen.codegen_utils import pointer_to
from python.codegen.comprehension import (
    captured_names,
    find_comprehensions,
    translate_comprehension,
)
from python.codegen.expression_codegen import ExpressionCodegen
from python.codegen.for_loop import translate_for_stmt
from python.codegen.translation_utils import (
    call_method,
    is_truthy,
    translate_func_signature,
)
from python.codegen.exceptions import translate_raise_stmt, translate_try_stmt
from python.codegen.typegen import cpp_type, is_pointer, ptr_type
from python.visitor import Traverser

includes = [
    "types.h",
    "exceptions.h",
    "finally.h",
    "truthy.h",
    "iter.h",
    "tuple.h",
    "ptr.h",
    "slice.h",
    "list.h",
    "strops.h",
    "dict.h",
    "set.h",
    "print.h",
    "scalars.h",
    "mathops.h",
    "builtins.h",
]


class StatementCodegen(Traverser):
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
        self.temp_count = 0
        # Each comprehension node mapped to the call that replaces it.
        self.comprehension_calls: dict[object, str] = {}
        self.expr_codegen.comprehension_calls = self.comprehension_calls

    def temp_name(self, prefix: str) -> str:
        """A name for a generated variable, unique across the file."""
        self.temp_count += 1
        return f"__{prefix}_{self.temp_count}"

    def visit_statements(self, statements):
        for statement in statements:
            self.visit(statement)

    def indent(self):
        self.indent_level += 1

    def unindent(self):
        self.indent_level -= 1

    def indented(self) -> str:
        """Return indentation string."""
        return "    " * self.indent_level

    def emit(self, code: str):
        """Emit a line of code."""
        # A blank separator stays blank rather than carrying the indent.
        self.output.append(f"{self.indented()}{code}" if code else "")

    def visit_block(self, o: Block):
        """Generate code for a block of statements."""
        self.indent()
        super().visit_block(o)
        self.unindent()

    def get_expr(self, expr: Expression, lvalue=False):
        self.expr_codegen.lvalue = lvalue
        return self.expr_codegen.visit(expr)

    def get_condition(self, expr: Expression) -> str:
        """Generate an expression to be used as a conditon"""
        self.expr_codegen.lvalue = False
        return self.expr_codegen.condition(expr)

    def translate_declaration(self, name: str, typ: Type):
        cpp = cpp_type(typ)
        return f"{cpp} {name};"

    def generate_declarations(self, declarations: SymbolTable):
        for name, item in declarations.items():
            # tree.names also holds functions, classes, imports and the
            # module dunders (__name__, __spec__, ...), none of which are
            # user globals to declare.
            if not isinstance(item.node, Var) or name.startswith("__"):
                continue
            t = item.type
            assert t
            self.emit(self.translate_declaration(name, t))

    def generate_includes(self):
        for include in includes:
            self.emit(f'#include "{include}"')
        self.emit(f"using namespace py;")

    def generate_global_declarations(self):
        self.generate_declarations(self.tree.names)

    def generate(self) -> str:
        """Generate all C++ code."""
        self.generate_includes()
        self.generate_global_declarations()
        self.visit(self.tree)
        return "\n".join(self.output)

    def visit_mypy_file(self, o: MypyFile):
        # A comprehension becomes a function, which has to be defined before
        # whatever definition calls it.
        for definition in o.defs:
            self.lift_comprehensions(definition)
            self.visit(definition)

    def lift_comprehensions(self, definition):
        """Emit a function per comprehension, and record how to call each."""
        locals_of = self.local_names(definition)
        for node, enclosing in find_comprehensions(definition):
            name = self.temp_name("comprehension").lstrip("_")
            captures = captured_names(
                node, lambda n: n in locals_of or n in enclosing
            )
            translate_comprehension(self, node, name, captures)
            arguments = ", ".join(capture.name for capture in captures)
            self.comprehension_calls[node] = f"{name}({arguments})"

    def local_names(self, definition) -> set[str]:
        """The names a definition holds itself, rather than reading globally."""
        if not isinstance(definition, FuncDef):
            return set()
        declarations = get_declarations(definition, self.types)
        return set(declarations) | {
            argument.variable.name for argument in definition.arguments
        }

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
            self.visit(stmt)
        self.unindent()
        self.emit("}")
        self.emit("")

    def visit_class_def(self, o: ClassDef):
        translate_class_def(self, o)

    def visit_assignment_stmt(self, o: AssignmentStmt):
        target = o.lvalues[0]
        rhs = self.get_expr(o.rvalue)
        # a[i] = x goes through __setitem__ so dict can insert new keys.
        if isinstance(target, IndexExpr):
            base = self.get_expr(target.base)
            index = self.get_expr(target.index)
            call = call_method(base, self.types[target.base], "__setitem__", index, rhs)
            self.emit(f"{call};")
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
            condition_cpp = self.get_condition(condition)
            if i == 0:
                self.emit(f"if ({condition_cpp}) {{")
            else:
                self.emit(f"}} else if ({condition_cpp}) {{")
            self.visit_block(body)
        if o.else_body:
            self.emit("} else {")
            self.visit_block(o.else_body)
        self.emit("}")

    def visit_for_stmt(self, o: ForStmt):
        translate_for_stmt(self, o)

    def visit_while_stmt(self, o: WhileStmt):
        self.emit("// While loop")
        self.emit(f"while ({self.get_condition(o.expr)}) {{")
        self.visit_block(o.body)
        self.emit("}")

    def visit_try_stmt(self, o: TryStmt):
        translate_try_stmt(self, o)

    def visit_raise_stmt(self, o: RaiseStmt):
        translate_raise_stmt(self, o)

    def visit_expression_stmt(self, o: ExpressionStmt):
        self.emit(f"{self.get_expr(o.expr)};")

    def visit_break_stmt(self, _: BreakStmt):
        self.emit("break;")

    def visit_continue_stmt(self, _: ContinueStmt):
        self.emit("continue;")
