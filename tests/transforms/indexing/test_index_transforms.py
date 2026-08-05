from pathlib import Path

from python.analysis.mypy_pass import analyse
from python.printer import PythonPrinter

test_file = Path(__file__).parent / "program.py"


def test_index_transform_snapshot(snapshot):
    program = analyse(str(test_file), open(test_file).read())
    back_to_python = PythonPrinter().visit(program.tree)
    assert snapshot == back_to_python
