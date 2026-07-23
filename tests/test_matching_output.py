"""Runs tests on python programs in the test_files directory by translating them into c++ and comparing the output against the python version"""

import glob
import os
import re
import subprocess
import tempfile
from pathlib import Path

import pytest

from main import translate_source
from python.utils import compile_cpp
from tests.test_utils import print_output_diff, run_python_and_capture

test_path = "tests/test_files"
paths = sorted(glob.glob(f"{test_path}/*.py"))


def _process_cpp_file(name: str, source: str, includes: set[str]):
    """Prepeare a C++ file for being batched.
    Remove #includes and add them to the includes set
    Remove 'using namespace's
    Rename int main() to int run()
    Return the processed program
    """
    body = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("#include"):
            includes.add(stripped)
        elif not stripped.startswith("using namespace"):
            body.append(line)
    body = "\n".join(body)
    # Replace the int main function with a custom run function
    cpp_main_function_regex = r"\bint\s+main\s*\(\s*\)"
    renamed = re.sub(cpp_main_function_regex, "int run()", body)
    return renamed


def _get_dispatch_function(translations: list[tuple[str, str]]):
    """
    Returns a main function that dispatches out to the different test programs based on the first command line argument.
    The files basenames are used as the dispatch command
    """
    dispatch = "".join(
        f'    if (argc > 1 && std::strcmp(argv[1], "{name}") == 0)'
        f" return prog_{name.removesuffix('.py')}::run();\n"
        for index, (name, _) in enumerate(translations)
    )
    return f"int main(int argc, char** argv) {{\n{dispatch}    return 1;\n}}\n"


def _join_cpp_files(translations: list[tuple[str, str]]) -> tuple[set[str], list[str]]:
    includes: set[str] = set()
    bodies: list[str] = []
    for index, (name, source) in enumerate(translations):
        processed_file = _process_cpp_file(name, source, includes)
        base_name = name.removesuffix(".py")
        namespaced_file = f"namespace prog_{base_name} {{\n{processed_file}\n}}\n"
        bodies.append(namespaced_file)
    return includes, bodies


def _batch_source(translations: list[tuple[str, str]]) -> str:
    """Fold every translated program into one translation unit.

    Includes are hoisted out because they cannot sit inside a namespace; each
    program's `main` becomes `run`, and a dispatcher picks one by name.
    """
    includes, bodies = _join_cpp_files(translations)
    dispatch_function = _get_dispatch_function(translations)
    return (
        "\n".join(sorted(includes))
        + "\nusing namespace py;\n\n"
        + "\n".join(bodies)
        + "\n#include <cstring>\n"
        + f"\n{dispatch_function}\n"
    )


@pytest.fixture(scope="session")
def batched_binary():
    """Compile every test program into a single binary.

    Both the compile and macOS's ~0.175s first-run check on a new executable
    are then paid once instead of once per program.
    """
    translations = [
        (os.path.basename(p), translate_source(open(p).read())) for p in paths
    ]
    current_directory = Path(os.path.abspath(__file__)).parent.resolve()
    source = os.path.join(current_directory, "batch.cpp")

    tmp_directory = tempfile.mkdtemp()
    exe = os.path.join(tmp_directory, "batch")

    with open(source, "w") as f:
        f.write(_batch_source(translations))

    compiled = compile_cpp(source, exe)
    assert compiled.returncode == 0, f"batch compile failed:\n{compiled.stderr}"
    return exe


class TestIdenticalOutput:
    @pytest.mark.parametrize("filename", paths, ids=lambda p: p.split("/")[-1])
    def test_file(self, filename: str, batched_binary: str):
        """Test that a Python file produces identical output between Python and C++."""
        cpp_output = subprocess.run(
            [batched_binary, os.path.basename(filename)],
            capture_output=True,
            text=True,
        )
        python_output = run_python_and_capture(filename)
        print_output_diff(python_output.stdout, cpp_output.stdout)
        assert cpp_output.stdout == python_output.stdout
