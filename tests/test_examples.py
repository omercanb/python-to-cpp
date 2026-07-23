"""Run the example programs and check they match CPython."""

import glob

import pytest

from main import translate_source
from python.utils import build_and_run_capture
from tests.test_utils import print_output_diff, run_python_and_capture

examples_path = "examples"


class TestExamples:
    paths = glob.glob(f"{examples_path}/*.py")

    @pytest.mark.parametrize("filename", paths, ids=lambda p: p.split("/")[-1])
    def test_example(self, filename: str):
        """An example must produce identical output in Python and C++."""
        program = open(filename).read()
        cpp_program = translate_source(program)
        cpp_output = build_and_run_capture(cpp_program)
        python_output = run_python_and_capture(filename)
        print_output_diff(python_output.stdout, cpp_output.stdout)
        assert cpp_output.stdout == python_output.stdout
