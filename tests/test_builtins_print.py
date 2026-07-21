from main import translate_source
from python.utils import build_and_run_capture
from tests.test_utils import print_output_diff, run_python_and_capture


class TestPrintBuiltin:
    """Test the print() builtin function with str() conversions and kwargs."""

    def test_print_with_kwargs(self):
        """Test print() with sep and end keyword arguments."""
        cpp_code = """
#include <iostream>
#include "print.h"
using namespace py;

int main() {
    // Test 1: default print, no args
    print();

    // Test 2: single arg with defaults
    print(42);

    // Test 3: multiple args with default separator
    print("Hello", "World", 123);

    // Test 4: custom separator (using _print_kwargs)
    _print_kwargs(",", "\\n", "a", "b", "c");

    // Test 5: custom separator and end (using _print_kwargs)
    _print_kwargs("|", " END\\n", 1, 2, 3);

    // Test 6: boolean with defaults
    print(true, false);

    return 0;
}
"""
        result = build_and_run_capture(cpp_code)
        expected_output = """
42
Hello World 123
a,b,c
1|2|3 END
True False
"""
        assert result.stdout.strip() == expected_output.strip()

    def test_input_py_matches_python(self):
        """Test that input.py produces identical output between Python and C++."""
        # Read and translate input.py
        with open("input.py") as f:
            program = f.read()

        cpp_program = translate_source(program)
        cpp_output = build_and_run_capture(cpp_program)
        python_output = run_python_and_capture("input.py")

        # Print outputs for debugging
        print_output_diff(python_output.stdout, cpp_output.stdout)

        assert cpp_output.stdout == python_output.stdout
