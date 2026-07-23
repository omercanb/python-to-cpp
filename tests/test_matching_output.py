import glob

import pytest

from main import translate_source
from python.utils import build_and_run_capture
from tests.test_utils import print_output_diff, run_python_and_capture

test_path = "tests/test_files"


class TestIdenticalOutput:
    paths = glob.glob(f"{test_path}/*.py")

    @pytest.mark.parametrize("filename", paths, ids=lambda p: p.split("/")[-1])
    def test_file(self, filename: str):
        """Test that a Python file produces identical output between Python and C++."""
        program = open(filename).read()
        cpp_program = translate_source(program)
        cpp_output = build_and_run_capture(cpp_program)
        python_output = run_python_and_capture(filename)
        print_output_diff(python_output.stdout, cpp_output.stdout)
        assert cpp_output.stdout == python_output.stdout
