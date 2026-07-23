def pytest_addoption(parser):
    parser.addoption(
        "--separate-compile",
        action="store_true",
        help="Compile each test program on its own instead of batching them all "
        "into one binary. Slower, but a compile error names the program it came "
        "from rather than a line in the combined source.",
    )
