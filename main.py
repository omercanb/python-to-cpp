import sys

from mypy.nodes import (
    Expression,
    TypeInfo,
)
from mypy.types import ProperType

from python.analysis.mypy_pass import _analyse, _generate
from python.errors import UnsupportedProgram, render
from python.utils import build_and_run

# Mypys strict upgrades




def full_pipeline():
    file = "input.py"
    result = _analyse(file, open(file).read())
    # print(result.tree)
    # print_types(result.types)
    try:
        output = _generate(result)
    except UnsupportedProgram as unsupported:
        print(render(unsupported.diagnostics, result.source, file))
        sys.exit(1)
    print(output)
    build_and_run(output)


def main():
    # cProfile.run("full_pipeline()", sort="cumtime")
    full_pipeline()


# Guarded: the tests import from here, and unguarded this ran the whole
# pipeline on every import.
if __name__ == "__main__":
    main()
