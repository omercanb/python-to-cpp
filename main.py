import sys

from pipeline import generate, analyse
from cpp_build import build_and_run
from convert_to_python import convert_to_python
from frontend.validate import render, validate


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
    output = generate(result)
    print(output)
    build_and_run(output)


def main():
    full_pipeline()

if __name__ == "__main__":
    main()
