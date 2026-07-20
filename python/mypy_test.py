import sys

from mypy import build
from mypy.api import run
from mypy.build import BuildSource
from mypy.nodes import AssignmentStmt, ClassDef, FuncDef, NameExpr, Var
from mypy.options import Options
from mypy.traverser import TraverserVisitor
from mypy.types import CallableType

normal_report, error_report, exit_status = run(["input.py", "--strict"])
if exit_status != 0:
    print(normal_report)
    print(error_report)
    sys.exit(exit_status)

opts = Options()
opts.export_types = True  # required to populate result.types
opts.preserve_asts = True  # keep the trees alive after checking
opts.incremental = False  # avoid stale cache surprises
opts.disallow_untyped_defs = True
opts.disallow_untyped_calls = True
opts.check_untyped_defs = True
opts.strict_optional = True


result = build.build(
    sources=[BuildSource("input.py", "example", None)],
    options=opts,
)

tree = result.files["example"]  # MypyFile
types = result.types  # dict[Expression, Type]


class BasicVisitor(TraverserVisitor):
    """Basic AST visitor for mypy tree."""

    # def visit_func_def(self, o: FuncDef) -> None:
    #     assert isinstance(o.type, CallableType)
    #     if o.info:
    #         print("Method", o.name, o.type, o.info)
    #         print("return type", o.type.ret_type)
    #     else:
    #         print("Function", o.name, o.type, o.body)
    #         print("return type", o.type.ret_type)
    #     super().visit_func_def(o)
    #
    # def visit_class_def(self, o: ClassDef) -> None:
    #     print(f"Class", o.name, o.info)
    #     super().visit_class_def(o)
    #
    # def visit_var(self, o: Var) -> None:
    #     print(f"Var: {o.name} : {o.type}")
    #     super().visit_var(o)
    #
    # def visit_assignment_stmt(self, o: AssignmentStmt) -> None:
    #     print(f"Assignment: {o}")
    #     super().visit_assignment_stmt(o)

    def visit_name_expr(self, o: NameExpr):
        print("Name Expr")
        print(o)
        print(o.fullname)
        print(o.name)
        print(o.is_new_def)
        super().visit_name_expr(o)


visitor = BasicVisitor()
tree.accept(visitor)
for name, sym in tree.names.items():
    print(name, sym)
