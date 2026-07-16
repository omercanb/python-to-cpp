import difflib
import glob
import os
import subprocess

from main import pipeline
from python.utils import build_and_run_capture

test_path = "tests/test_files"


class TestIdenticalOutput:
    paths = glob.glob(f"{test_path}/*.py")

    def test_files(self):
        for path in self.paths:
            self.run_file(path)

    def run_python_and_capture(self, path: str):
        program = open(path).read()
        # The main function is not handled in any special way for translation to c++
        program_with_main = f"{program}\nmain()"
        temp_path = f"{path}.tmp"
        try:
            with open(temp_path, "w") as f:
                f.write(program_with_main)
            result = subprocess.run(
                ["python", temp_path], capture_output=True, text=True
            )
        finally:
            os.remove(temp_path)
        return result

    def run_file(self, filename: str):
        program = open(filename).read()
        # The main function is not handled in any special way for translation to c++
        cpp_program = pipeline(program)
        cpp_output = build_and_run_capture(cpp_program)
        python_output = self.run_python_and_capture(filename)
        print("Python Output")
        print(python_output.stdout)
        print("Cpp Output")
        print(cpp_output.stdout)
        python_lines = python_output.stdout.splitlines()
        cpp_lines = cpp_output.stdout.splitlines()
        diff = difflib.unified_diff(
            python_lines, cpp_lines, fromfile="python", tofile="cpp"
        )
        print("Diff")
        print("\n".join(diff))
        assert cpp_output.stdout == python_output.stdout
