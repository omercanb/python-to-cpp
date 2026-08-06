import sys

from mypy_pass import _generate, analyse
from python.compile import build_and_run
from python.convert_to_python import convert_to_python
from python.frontend.validate import render, validate

# Mypys strict upgrades


def full_pipeline():

    file = "input.py"
    result = analyse(file, open(file).read())
    # for k, v in result.types.items():
    #     print(f"{k} : {v}")
    print(str(result.tree))
    print(convert_to_python(result.tree))
    # print_types(result.types)
    diagnostics = validate(result.tree, result.types)
    if diagnostics:
        print(render(diagnostics, result.source, file))
        sys.exit(1)
    output = _generate(result)
    print(output)
    build_and_run(output)


def main():
    # cProfile.run("full_pipeline()", sort="cumtime")
    full_pipeline()


# Guarded: the tests import from here, and unguarded this ran the whole
# pipeline on every import.
if __name__ == "__main__":
    main()
