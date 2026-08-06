from pathlib import Path

from mypy_pass import analyse
from python.convert_to_python import PythonPrinter

test_file = Path(__file__).parent / "program.py"


def test_comprehension_transform_snapshot(snapshot):
    program = analyse(str(test_file), open(test_file).read())
    back_to_python = PythonPrinter().visit(program.tree)
    assert snapshot == back_to_python
