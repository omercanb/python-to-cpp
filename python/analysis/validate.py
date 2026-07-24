"""Reject Python the transpiler cannot translate, before code generation.

Codegen may then assume its input is translatable, so what is left there are
invariants rather than user facing checks. Every construct is collected in one
walk so a program reports all of its problems at once.
"""

from __future__ import annotations

from mypy.nodes import (
    AssignmentStmt,
    Block,
    CallExpr,
    ClassDef,
    DictExpr,
    DictionaryComprehension,
    Expression,
    ExpressionStmt,
    FuncDef,
    GeneratorExpr,
    IfStmt,
    IndexExpr,
    IntExpr,
    ListComprehension,
    ListExpr,
    Lvalue,
    MemberExpr,
    MypyFile,
    NameExpr,
    OpExpr,
    PassStmt,
    RaiseStmt,
    ReturnStmt,
    SetComprehension,
    SetExpr,
    StarExpr,
    StrExpr,
    TempNode,
    TryStmt,
    TupleExpr,
    UnaryExpr,
    Var,
    WhileStmt,
)
from mypy.types import CallableType, TupleType, Type, UnionType, get_proper_type

from python.codegen.builtins import EXCEPTION_TYPES
from python.codegen.exceptions import names_a_class
from python.codegen.typegen import UnsupportedType, cpp_type, cpp_type_name
from python.errors import Diagnostic, diagnostic
from python.visitor import Traverser

SUPPORTED_EXCEPTIONS = ", ".join(
    sorted({name.rpartition(".")[2] for name in EXCEPTION_TYPES})
)


class _ReturnFinder(Traverser):
    def __init__(self) -> None:
        self.found = False

    def visit_return_stmt(self, o: ReturnStmt) -> None:
        self.found = True


def returns(block: Block) -> bool:
    finder = _ReturnFinder()
    finder.visit(block)
    return finder.found


def _type_hint(t: Type) -> str:
    """Holding a function in a variable is the common way to land here."""
    if isinstance(get_proper_type(t), CallableType):
        return (
            "a function cannot be stored in a variable, call it where it is "
            "needed instead:\nprint(add(1, 2))"
        )
    return (
        "use int, float, str, bool, or a list, dict, set or tuple of those:\n"
        "values: list[int] = []"
    )


def _name_of(expression: Expression, fallback: str) -> str:
    """The written name, for hints that quote the code back at the reader."""
    return expression.name if isinstance(expression, NameExpr) else fallback


def _tuple_index_hint(o: IndexExpr) -> str:
    base = _name_of(o.base, "pair")
    index = _name_of(o.index, "i")
    return (
        "a tuple holds a different type at each position, so the position has "
        "to be known at compile time.\n"
        f"Index it with a literal:\n"
        f"{base}[0]\n"
        f"or hold the values in a list, where every element has one type:\n"
        f"{base} = [1, 2]\n"
        f"print({base}[{index}])"
    )


class _Validator(Traverser):
    def __init__(self, types: dict[Expression, Type]):
        self.types = types
        self.diagnostics: list[Diagnostic] = []

    def report(self, node, kind: str, message: str, hint: str) -> None:
        self.diagnostics.append(diagnostic(node, kind, message, hint))

    def check_type(self, node, t: Type) -> None:
        """Report a type codegen has no C++ spelling for."""
        try:
            cpp_type(t)
        except UnsupportedType as unsupported:
            self.report(
                node,
                "unsupported-type",
                f"no C++ equivalent for the type `{unsupported.type}`",
                _type_hint(unsupported.type),
            )

    def check_inferred_type(self, node: Expression) -> None:
        t = self.types.get(node)
        if t is not None:
            self.check_type(node, t)

    def visit_class_def(self, o: ClassDef) -> None:
        if o.base_type_exprs:
            self.report(
                o,
                "class-inheritance",
                "a base class is not supported",
                "give the class its own copy of what it needs:\n"
                "class Square:\n"
                "    def __init__(self, side: int) -> None:\n"
                "        self.side = side",
            )
        for statement in o.defs.body:
            self.check_class_member(statement)
        super().visit_class_def(o)

    def check_class_member(self, statement) -> None:
        """A class body holds annotations and methods, and nothing else."""
        if isinstance(statement, (FuncDef, PassStmt)):
            return
        # A docstring is an expression statement; it is simply dropped.
        if isinstance(statement, ExpressionStmt) and isinstance(
            statement.expr, StrExpr
        ):
            return
        if isinstance(statement, AssignmentStmt):
            # `x: int` parses as an assignment whose value is a placeholder.
            if isinstance(statement.rvalue, TempNode):
                return
            self.report(
                statement,
                "class-variable",
                "a class level value is not supported",
                "every attribute is per instance, so set it in __init__:\n"
                "def __init__(self) -> None:\n"
                "    self.kind = \"point\"",
            )
            return
        self.report(
            statement,
            "class-body",
            "only attributes and methods are supported in a class body",
            "move anything else outside the class",
        )

    def visit_func_def(self, o: FuncDef) -> None:
        signature = get_proper_type(o.type)
        if isinstance(signature, CallableType):
            self.check_type(o, signature.ret_type)
        for argument in o.arguments:
            if argument.variable.type is not None:
                self.check_type(argument, argument.variable.type)
        super().visit_func_def(o)

    def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
        for lvalue in o.lvalues:
            self.check_lvalue(lvalue)
        super().visit_assignment_stmt(o)

    def check_lvalue(self, lvalue: Lvalue) -> None:
        if isinstance(lvalue, NameExpr):
            if lvalue.is_new_def:
                self.check_inferred_type(lvalue)
            return
        if isinstance(lvalue, TupleExpr):
            for item in lvalue.items:
                self.check_lvalue(item)
            return
        if isinstance(lvalue, StarExpr):
            self.report(
                lvalue,
                "starred-assignment",
                "a starred assignment target is not supported",
                "take the parts by slicing instead:\n"
                "first = values[0]\nrest = values[1:]",
            )
            return
        # Writing into something that already exists, nothing to declare.
        assert isinstance(lvalue, (IndexExpr, MemberExpr)), lvalue

    def visit_try_stmt(self, o: TryStmt) -> None:
        if o.is_star:
            # mypy records no span for the `except*` token itself, so point at
            # the first handler's class rather than at `try`.
            handled = next((t for t in o.types if t is not None), o)
            self.report(
                handled,
                "except-star",
                "`except*` groups are not supported",
                "use a plain except clause:\nexcept ValueError as error:",
            )
        for type_expression in o.types:
            self.check_handler_type(type_expression)
        if o.finally_body is not None and returns(o.finally_body):
            self.report(
                o.finally_body,
                "return-in-finally",
                "`return` inside `finally` is not supported",
                "return after the try statement instead:\n"
                "try:\n    ...\nfinally:\n    cleanup()\nreturn result",
            )
        super().visit_try_stmt(o)

    def check_handler_type(self, type_expression: Expression | None) -> None:
        if type_expression is None:
            return
        if isinstance(type_expression, TupleExpr):
            self.report(
                type_expression,
                "except-tuple",
                "an except clause takes a single exception class",
                "write one clause per class:\n"
                "except ValueError:\n    ...\nexcept KeyError:\n    ...",
            )
            return
        self.check_exception_class(type_expression)

    def visit_raise_stmt(self, o: RaiseStmt) -> None:
        if o.from_expr is not None:
            self.report(
                o,
                "raise-from",
                "chaining exceptions with `from` is not supported",
                'raise the new exception on its own:\nraise KeyError("missing")',
            )
        raised = o.expr
        if raised is not None:
            klass = raised.callee if isinstance(raised, CallExpr) else raised
            self.check_exception_class(klass)
            if isinstance(raised, CallExpr) and len(raised.args) > 1:
                self.report(
                    raised,
                    "exception-arguments",
                    "an exception takes a single message",
                    'join the parts into one string:\nraise ValueError("a: " + b)',
                )
        super().visit_raise_stmt(o)

    def check_exception_class(self, expression: Expression) -> None:
        """Only classes are checked; a variable holds an already valid one."""
        if not names_a_class(expression):
            return
        assert isinstance(expression, NameExpr)
        if expression.fullname not in EXCEPTION_TYPES:
            self.report(
                expression,
                "unsupported-exception",
                f"`{expression.name}` has no C++ equivalent",
                f"use one of: {SUPPORTED_EXCEPTIONS}\n"
                "a base class like LookupError has to be spelled as the "
                "concrete classes it covers",
            )

    def visit_dict_expr(self, o: DictExpr) -> None:
        for key, _ in o.items:
            if key is None:
                self.report(
                    o,
                    "dict-unpacking",
                    "`**` unpacking in a dict literal is not supported",
                    "copy the entries across in a loop:\n"
                    'merged = {"a": 1}\n'
                    "for key in other:\n    merged[key] = other[key]",
                )
                break
        self.check_inferred_type(o)
        super().visit_dict_expr(o)

    # A list or set comprehension holds a GeneratorExpr, so its parts are
    # walked directly; anything that still reaches visit_generator_expr is a
    # bare generator.
    def visit_list_comprehension(self, o: ListComprehension) -> None:
        self.check_inferred_type(o)
        self.visit_comprehension_parts(o.generator)
        self.visit(o.generator.left_expr)

    def visit_set_comprehension(self, o: SetComprehension) -> None:
        self.check_inferred_type(o)
        self.visit_comprehension_parts(o.generator)
        self.visit(o.generator.left_expr)

    def visit_dictionary_comprehension(self, o: DictionaryComprehension) -> None:
        self.check_inferred_type(o)
        super().visit_dictionary_comprehension(o)

    def visit_generator_expr(self, o: GeneratorExpr) -> None:
        self.report(
            o,
            "generator-expression",
            "generator expressions are not supported",
            "wrap it in a list, which is built in one go rather than lazily:\n"
            "total = sum([v * 2 for v in values])",
        )

    def visit_list_expr(self, o: ListExpr) -> None:
        self.check_inferred_type(o)
        super().visit_list_expr(o)

    def visit_set_expr(self, o: SetExpr) -> None:
        self.check_inferred_type(o)
        super().visit_set_expr(o)

    def visit_index_expr(self, o: IndexExpr) -> None:
        base_type = get_proper_type(self.types.get(o.base))
        if isinstance(base_type, TupleType) and not isinstance(o.index, IntExpr):
            self.report(
                o.index,
                "tuple-index",
                "a tuple can only be indexed by an integer literal",
                _tuple_index_hint(o),
            )
        super().visit_index_expr(o)

    def visit_if_stmt(self, o: IfStmt) -> None:
        for condition in o.expr:
            self.visit_condition(condition)
        for body in o.body:
            self.visit(body)
        if o.else_body is not None:
            self.visit(o.else_body)

    def visit_while_stmt(self, o: WhileStmt) -> None:
        self.visit_condition(o.expr)
        self.visit(o.body)
        if o.else_body is not None:
            self.visit(o.else_body)

    def visit_condition(self, expression: Expression) -> None:
        """Walk an expression in condition position.

        Mirrors ExpressionCodegen.condition: and/or/not there become &&/||/!,
        which need no value at all, so the operands never need a common type.
        """
        if isinstance(expression, OpExpr) and expression.op in ("and", "or"):
            self.visit_condition(expression.left)
            self.visit_condition(expression.right)
            return
        if isinstance(expression, UnaryExpr) and expression.op == "not":
            self.visit_condition(expression.expr)
            return
        self.visit(expression)

    def visit_op_expr(self, o: OpExpr) -> None:
        if o.op in ("and", "or"):
            self.check_bool_op(o)
        super().visit_op_expr(o)

    def check_bool_op(self, o: OpExpr) -> None:
        result = get_proper_type(self.types.get(o))
        if not isinstance(result, UnionType):
            return
        try:
            spellings = {cpp_type_name(item) for item in result.items}
        except UnsupportedType:
            return  # reported against the operand that carries the type
        if len(spellings) > 1:
            self.report(
                o,
                "mixed-bool-op",
                f"`{o.op}` on unrelated types has no single C++ type",
                f"`{o.op}` returns one of its operands, so both sides need the "
                "same type.\nUse it directly in a condition instead:\n"
                "if count or fallback:",
            )


def validate(tree: MypyFile, types: dict[Expression, Type]) -> list[Diagnostic]:
    """Every construct in the file that cannot be translated, in source order."""
    validator = _Validator(types)
    validator.visit(tree)
    for symbol in tree.names.values():
        if isinstance(symbol.node, Var) and symbol.type is not None:
            validator.check_type(symbol.node, symbol.type)
    # Nested and/or report once each, which reads as the same complaint twice.
    unique = {(d.position, d.kind): d for d in validator.diagnostics}
    return sorted(unique.values(), key=lambda d: d.position)
