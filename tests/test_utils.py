"""Utilities for testing transpiler output."""

import difflib
import os
import subprocess
import sys
import tempfile

from python.utils import compile_cpp


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
        # sys.executable, not "python": a bare "python" hits the pyenv shim,
        # 0.27s a call against 0.016s.
        result = subprocess.run(
            [sys.executable, temp_path], capture_output=True, text=True
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
        difflib.unified_diff(python_lines, cpp_lines, fromfile="python", tofile="cpp")
    )
    if diff:
        print("\n--- Diff ---")
        print("\n".join(diff))


def compile_cpp_test(cpp_file: str) -> str:
    """Compile a C++ test file and return the executable path.

    Args:
        cpp_file: Path to the C++ source file

    Returns:
        Path to the compiled executable

    Raises:
        RuntimeError: If compilation fails
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix="") as exe_file:
        exe_path = exe_file.name

    # Get project root - assumes tests/ directory structure
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # These include the same cpp/ runtime, so they share its precompiled header.
    result = compile_cpp(cpp_file, exe_path, includes=[project_root])
    if result.returncode != 0:
        os.unlink(exe_path)
        raise RuntimeError(f"Compilation failed:\n{result.stdout}\n{result.stderr}")

    return exe_path


def run_cpp_test(cpp_file: str) -> subprocess.CompletedProcess:
    """Compile and run a C++ test file, capturing output.

    Args:
        cpp_file: Path to the C++ source file

    Returns:
        CompletedProcess with stdout containing the output
    """
    exe_path = compile_cpp_test(cpp_file)
    try:
        result = subprocess.run([exe_path], capture_output=True, text=True)
        return result
    finally:
        os.unlink(exe_path)
