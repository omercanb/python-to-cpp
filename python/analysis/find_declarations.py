"""Save the variables that need to be declared inside each function"""

from mypy.nodes import (
    AssignmentStmt,
    Expression,
    ForStmt,
    FuncDef,
    IndexExpr,
    Lvalue,
    MemberExpr,
    NameExpr,
    TupleExpr,
)
from mypy.traverser import TraverserVisitor
from mypy.types import CallableType, Type, get_proper_type


class _DeclarationCollector(TraverserVisitor):
    """Collect all local variable declarations in a function."""

    def __init__(self, types_dict: dict[Expression, Type]):
        self.types = types_dict
        self.declarations: dict[str, Type] = {}

    def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
        """Collect variables from assignment statements."""
        for lvalue in o.lvalues:
            self.check_names(lvalue)
        o.rvalue.accept(self)

    def visit_for_stmt(self, o: ForStmt) -> None:
        self.check_names(o.index)

    def check_names(self, lvalue: Lvalue) -> None:
        """Recursively collect all names in an lvalue."""
        if isinstance(lvalue, NameExpr):
            # Simple: x = ...
            self.check_add_declaration(lvalue)

        elif isinstance(lvalue, TupleExpr):
            # Destructuring: x, y = ...
            for item in lvalue.items:
                self.check_names(item)

        elif isinstance(lvalue, (IndexExpr, MemberExpr)):
            # d[k] = ... / obj.attr = ... write into something that exists.
            pass
        else:
            assert False, "Other assigns not yet supported"

    def check_add_declaration(self, name: NameExpr):
        """Check if name is a declaration and add it to declarations"""
        if name.is_new_def:
            assert name.name not in self.declarations
            self.declarations[name.name] = self.types[name]


def get_declarations(
    func: FuncDef, types_dict: dict[Expression, Type]
) -> dict[str, Type]:
    collector = _DeclarationCollector(types_dict)
    func.accept(collector)
    return collector.declarations
