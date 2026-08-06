from dataclasses import dataclass
from pathlib import Path

from mypy.nodes import (
    DictionaryComprehension,
    GeneratorExpr,
    ListComprehension,
    NameExpr,
    SetComprehension,
)

from analysis.free_variables import get_free_variables
from pipeline import parse
from convert_to_python import convert_to_python
from visitor import Traverser

test_file = Path(__file__).parent / "program.py"


@dataclass
class PrintedName:
    fullname: str
    line: int
    column: int

    def __init__(self, name: NameExpr):
        self.fullname = name.fullname
        self.line = name.line
        self.column = name.column


def test_free_variable_snapshot(snapshot):
    result = parse(str(test_file), open(test_file).read())
    collector = ComprehensionCollector()
    collector.visit(result)
    free_vars_lists = []
    for vars_list in collector.free_var_list:
        free_vars_lists.append([])
        for var in vars_list:
            free_vars_lists[-1].append(PrintedName(var))
    for i, comprehension_text in enumerate(collector.comprehension_text):
        free_vars_lists[i] = (comprehension_text, free_vars_lists[i])
    assert free_vars_lists == snapshot


class ComprehensionCollector(Traverser):
    def __init__(self):
        self.free_var_list: list[list[NameExpr]] = []
        self.comprehension_text: list[str] = []

    def visit_list_comprehension(self, o: ListComprehension):
        self.free_var_list.append(get_free_variables(o))
        self.comprehension_text.append(convert_to_python(o))
        self.visit_comprehension(o.generator)

    def visit_set_comprehension(self, o: SetComprehension):
        self.free_var_list.append(get_free_variables(o))
        self.comprehension_text.append(convert_to_python(o))
        self.visit_comprehension(o.generator)

    def visit_dictionary_comprehension(self, o: DictionaryComprehension):
        self.free_var_list.append(get_free_variables(o))
        self.comprehension_text.append(convert_to_python(o))
        self.visit_comprehension(o)

    def visit_comprehension(self, o: GeneratorExpr | DictionaryComprehension) -> None:
        if isinstance(o, GeneratorExpr):
            self.visit(o.left_expr)
        if isinstance(o, DictionaryComprehension):
            self.visit(o.key)
            self.visit(o.value)
        for index in o.indices:
            self.visit(index)
        for sequence in o.sequences:
            self.visit(sequence)
        for conditions in o.condlists:
            for condition in conditions:
                self.visit(condition)
