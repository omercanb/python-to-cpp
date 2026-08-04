"""Transforms for putting comprehensions into more useful forms"""

from ast import Name

from mypy.nodes import (
    ArgKind,
    AssignmentStmt,
    Block,
    CallExpr,
    DictExpr,
    DictionaryComprehension,
    Expression,
    ForStmt,
    FuncDef,
    GeneratorExpr,
    IfStmt,
    IndexExpr,
    ListComprehension,
    Lvalue,
    MemberExpr,
    NameExpr,
    SetComprehension,
    SetExpr,
    Statement,
    Var,
)
from mypy.types import Type

from python.namer import TempNameGenerator
from python.transform.tree_transformer import Transformer


class ComprehensionRemover(Transformer):
    def __init__(self, types: dict[Expression, Type]):
        super().__init__()
        self.types = types

    # def visit_list_comprehension(self, o: ListComprehension) -> None:
    #     self.visit(o.generator)
    #
    def visit_set_comprehension(self, o: SetComprehension):
        tmp_name = TempNameGenerator().temp_name("set_comprehension")

        name = NameExpr(tmp_name)
        name.is_new_def = True

        assign = AssignmentStmt([name], rvalue=SetExpr([]))
        body_statement = CallExpr(
            MemberExpr(NameExpr(tmp_name), "add"),
            [o.generator.left_expr],
            [ArgKind.ARG_POS],
            arg_names=[None],
        )
        comprehension = self.expand_comprehension(o.generator, body_statement)
        self.hoist([assign, comprehension])

        typ = self.types[o]
        self.types[assign.rvalue] = typ
        self.types[assign.lvalues[0]] = typ
        self.types[body_statement.callee] = typ

        return NameExpr(tmp_name)

    def visit_dictionary_comprehension(self, o: DictionaryComprehension):
        tmp_name = TempNameGenerator().temp_name("dict_comprehension")

        name = NameExpr(tmp_name)
        name.is_new_def = True

        assign = AssignmentStmt([name], rvalue=DictExpr([]))
        body_statement = AssignmentStmt(
            [IndexExpr(NameExpr(tmp_name), o.key)], rvalue=o.value
        )
        comprehension = self.expand_comprehension(o, body_statement)
        comprehension_function = FuncDef(
            TempNameGenerator().temp_name("comprehension"),
        )
        self.hoist([assign, comprehension])

        typ = self.types[o]
        self.types[assign.rvalue] = typ
        self.types[assign.lvalues[0]] = typ
        self.types[body_statement.lvalues[0].base] = typ

        return NameExpr(tmp_name)

    def expand_comprehension(
        self, o: GeneratorExpr | DictionaryComprehension, body_stmt: Statement
    ):
        # Expand the comprehension into a for loop over the iterator and adding to a container
        """
        [(i, j) for i in range(10) if i % 2 for j in range(10) if j % 2] ->
        tmp = []
        for i in range(10):
            if i % 2:
                for j in range(10):
                    if j % 2:
                        tmp.append((i, j))
        """
        inner = body_stmt
        for index_variable, interated_sequence, conditions in zip(
            reversed(o.indices), reversed(o.sequences), reversed(o.condlists)
        ):
            for condition in conditions:
                inner = IfStmt([condition], [Block([inner])], else_body=None)
            # for index_variable in iterated_sequence: if condition[0]: if condition[1]: ...
            inner = ForStmt(
                index_variable, interated_sequence, Block([inner]), else_body=None
            )
        return inner
