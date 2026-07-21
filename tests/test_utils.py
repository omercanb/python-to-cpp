"""Utilities for testing transpiler output."""

import difflib
import os
import subprocess


def run_python_and_capture(path: str) -> subprocess.CompletedProcess:
    """Run a Python file and capture its output.

    Appends a call to main() if the file defines a main function.

    Args:
        path: Path to the Python file

    Returns:
        CompletedProcess with stdout containing the output
    """
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


def print_output_diff(python_output: str, cpp_output: str) -> None:
    """Print Python and C++ outputs side-by-side with a unified diff.

    Args:
        python_output: Output from running Python code
        cpp_output: Output from running C++ code
    """
    print("\n--- Python Output ---")
    print(python_output)
    print("\n--- C++ Output ---")
    print(cpp_output)

    python_lines = python_output.splitlines()
    cpp_lines = cpp_output.splitlines()
    diff = list(
        difflib.unified_diff(
            python_lines, cpp_lines, fromfile="python", tofile="cpp"
        )
    )
    if diff:
        print("\n--- Diff ---")
        print("\n".join(diff))
