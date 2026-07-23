"""Tests for C++ implementations by running compiled binaries."""

import os
import subprocess
import glob
from .test_utils import compile_cpp_test


class TestCppTests:
    """Discover and run C++ unit tests from cpp_tests/ directory."""

    @classmethod
    def setup_class(cls):
        """Compile all C++ test files once."""
        cpp_tests_dir = os.path.join(os.path.dirname(__file__), "cpp_tests")
        test_files = glob.glob(os.path.join(cpp_tests_dir, "test_*.cpp"))

        cls.executables = {}
        for test_file in test_files:
            test_name = os.path.splitext(os.path.basename(test_file))[0]
            exe_path = compile_cpp_test(test_file)
            cls.executables[test_name] = exe_path

    @classmethod
    def teardown_class(cls):
        """Clean up compiled binaries."""
        for exe_path in cls.executables.values():
            if os.path.exists(exe_path):
                os.unlink(exe_path)

    def test_cpp_binaries(self):
        """Run all compiled C++ test binaries."""
        for test_name, exe_path in self.executables.items():
            result = subprocess.run([exe_path], capture_output=True, text=True)
            assert (
                result.returncode == 0
            ), f"{test_name} failed:\n{result.stderr}"
            assert (
                "All tests passed!" in result.stdout
            ), f"{test_name} did not report success"
