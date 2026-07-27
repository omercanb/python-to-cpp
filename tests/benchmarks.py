import glob

import pytest

enabled_benchmarks = ["integers"]


@pytest.fixture(scope="session")
def get_benchmarks():
    """Return a function running one test program, capturing its output."""
    all_benchmarks = glob.glob("**/*.py")
    filtered_benchmarks = []
    for path in all_benchmarks:
        for enabled_pattern in enabled_benchmarks:
            if enabled_pattern in path:
                filtered_benchmarks.append(path)
                break
    return filtered_benchmarks
