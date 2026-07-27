from __future__ import annotations

import argparse
import glob
import os
import re
import statistics
import subprocess
import sys
import time
from enum import Enum, auto
from importlib import import_module
from pathlib import Path
from typing import NamedTuple, Optional

from benchmarking import BenchmarkInfo, benchmarks
from typing_extensions import Final

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from main import pipeline
from python import utils
from python.utils import compile_cpp, compile_proc

raw_output = False

# Minimum total time (seconds) to run a benchmark
MIN_TIME = 2.0
# Minimum number of iterations to run a benchmark
MIN_ITER = 10


BINARY_EXTENSION: Final = "pyd" if sys.platform == "win32" else "so"
utils.set_cpp_dir(Path("../../../cpp"))

# A cache of the translated executables that gets populated when first translated
translated_executable_paths: dict[str, str] = {}
# A cache of the compiled handwritten files
handwritten_executable_paths: dict[str, str] = {}


def run_once(benchmark: BenchmarkInfo, mode: BenchmarkMode) -> float:
    if mode == BenchmarkMode.interpreted:
        return run_interpreted(benchmark)
    elif mode == BenchmarkMode.translated:
        return run_translated(benchmark)
    elif mode == BenchmarkMode.handwritten:
        return run_handwritten(benchmark)
    assert False


def run_interpreted(benchmark: BenchmarkInfo) -> float:
    module = benchmark.module
    program = (
        'import %s; import benchmarking as bm; print("\\nelapsed:", bm.run_once("%s"))'
        % (
            module,
            benchmark.name,
        )
    )
    cmd = [sys.executable, "-c", program]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    return parse_elapsed_time(result.stdout)


def run_translated(benchmark: BenchmarkInfo) -> float:
    if benchmark.name not in translated_executable_paths:
        translated_executable_paths[benchmark.name] = translate_and_compile_benchmark(
            benchmark
        )
    binary = translated_executable_paths[benchmark.name]
    cmd = [f"./{binary}"]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    return parse_elapsed_time(result.stdout)


def run_handwritten(benchmark: BenchmarkInfo) -> float:
    if benchmark.name not in handwritten_executable_paths:
        handwritten_executable_paths[benchmark.name] = compile_handwritten_benchmark(
            benchmark
        )
    binary = translated_executable_paths[benchmark.name]
    cmd = [f"./{binary}"]
    result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    return parse_elapsed_time(result.stdout)


def parse_elapsed_time(output: bytes) -> float:
    m = re.search(rb"\belapsed: ([-+0-9.e]+)\b", output)
    assert m is not None, "could not find elapsed time in output:\n%r" % output
    return float(m.group(1))


def smoothen(a: list[float]) -> list[float]:
    # Remove (at most) one third of the slowest runs (these are likely outliers).
    return sorted(a)[: 2 * (len(a) + 1) // 3]


class BenchmarkMode(Enum):
    interpreted = auto()  # Running the benchamrk with python
    translated = auto()  # Running the benchmark after translating
    handwritten = auto()  # Running the custom written C++ version of the benchmark


def run_benchmark(
    benchmark: BenchmarkInfo,
    mode: BenchmarkMode,
    min_iter: Optional[int] = None,
    min_time: Optional[float] = None,  # Min time in seconds
) -> list[float]:

    if not min_iter:
        # Use default minimum iterations
        if benchmark.min_iterations is not None:
            min_iter = benchmark.min_iterations
        else:
            min_iter = MIN_ITER
    if not min_time:
        min_time = 2

    if not raw_output:
        print("running %s : %s" % (benchmark.name, mode.name))

    # Warm up
    run_once(benchmark, mode)

    times = []
    n = 0
    while True:
        t = run_once(benchmark, mode)
        times.append(t)
        if not raw_output:
            sys.stdout.write(".")
            sys.stdout.flush()
        n += 1
        long_enough = sum(times) >= MIN_TIME
        if long_enough and n >= min_iter:
            break

    if not raw_output:
        print()
    return times

    # if benchmark.compiled_only:
    #     # TODO: Remove this once it's no longer needed for debugging
    #     print(f"runtimes: {sorted(times_compiled)}")
    # if benchmark.strip_outlier_runs:
    #     times_interpreted = smoothen(times_interpreted)
    #     times_compiled = smoothen(times_compiled)
    # n = max(len(times_interpreted), len(times_compiled))
    # if interpreted:
    #     stdev1 = statistics.stdev(times_interpreted)
    #     mean1 = sum(times_interpreted) / n
    # else:
    #     stdev1 = 0.0
    #     mean1 = 0.0
    # if compiled:
    #     stdev2 = statistics.stdev(times_compiled)
    #     mean2 = sum(times_compiled) / n
    # else:
    #     stdev2 = 0.0
    #     mean2 = 0.0
    # if not raw_output:
    #     if interpreted:
    #         print(
    #             "interpreted: %.6fs (avg of %d iterations; stdev %.2g%%)"
    #             % (mean1, n, 100.0 * stdev1 / mean1)
    #         )
    #     if compiled:
    #         print(
    #             "compiled:    %.6fs (avg of %d iterations; stdev %.2g%%)"
    #             % (mean2, n, 100.0 * stdev2 / mean2)
    #         )
    #     if compiled and interpreted:
    #         print()
    #         relative = sum(times_interpreted) / sum(times_compiled)
    #         print("compiled is %.3fx faster" % relative)
    # else:
    #     print(
    #         "%d %.6f %.6f %.6f %.6f"
    #         % (n, sum(times_interpreted) / n, stdev1, sum(times_compiled) / n, stdev2)
    #     )


def get_statistics(times: list[float]):
    return (statistics.mean(times), statistics.stdev(times))


def get_python_filepath(benchmark: BenchmarkInfo) -> str:
    fname = benchmark.module.replace(".", "/") + ".py"
    return fname


def get_translated_filepath(benchmark: BenchmarkInfo) -> str:
    fname = benchmark.module.replace(".", "/") + ".cpp"
    return fname


def get_handwritten_filepath(benchmark: BenchmarkInfo) -> str:
    fname = "handwritten_" + benchmark.module.replace(".", "/") + ".cpp"
    return fname


def translate_and_compile_benchmark(benchmark: BenchmarkInfo) -> str:
    if not raw_output:
        print("compiling %s..." % benchmark.module)
    cpp = translate_module_for_benchmarking(benchmark.module, benchmark.name)
    exe = compile_proc(
        cpp,
        get_translated_filepath(benchmark),
    )
    return exe


def translate_module_for_benchmarking(module: str, benchmark: str) -> str:
    """Remove all the benchmark decorators form a module, translate to C++, and add a main function that times the benchmark function"""
    fnam = module.replace(".", "/") + ".py"
    file = open(fnam).read()
    file = file.replace("@benchmark()\n", "")
    cpp = pipeline(fnam, file)
    assert "int main" not in cpp
    main_function = main_function_template(benchmark)
    cpp += "\n" + main_function
    cpp = "#include <chrono>\n" + cpp
    return cpp


def compile_handwritten_benchmark(benchmark: BenchmarkInfo) -> str:
    filepath = get_handwritten_filepath(benchmark)
    executable_path = filepath.rstrip(".cpp")
    exe = compile_cpp(get_handwritten_filepath(benchmark), executable_path)
    return executable_path


def main_function_template(benchmark: str) -> str:
    # Add a main function that runs the benchmark and times it
    main_function = """
    int main() {
        auto t0 = std::chrono::steady_clock::now();
        %s(); // Call the benchmarked function
        auto t1 = std::chrono::steady_clock::now();
        auto s = std::chrono::duration<double>(t1 - t0).count() ;
        std::cout << "elapsed: " << s << '\\n';
        return 0;
    }
    """ % benchmark
    return main_function


def import_all() -> None:
    files = glob.glob(f"microbenchmarks/*.py")
    files += glob.glob(f"benchmarks/*.py")
    for fnam in files:
        filepath = Path(fnam).resolve()
        if filepath.name == "__init__.py" or filepath.suffix != ".py":
            continue
        benchmarks_root_dir = Path(__file__).parent.resolve()
        module_parts = filepath.with_suffix("").relative_to(benchmarks_root_dir).parts
        module = ".".join(module_parts)
        import_module(module)


def delete_binaries() -> None:
    binaries = [
        p for p in Path("microbenchmarks/").iterdir() if p.is_file() and not p.suffix
    ]
    binaries += [
        p for p in Path("benchmarks/").iterdir() if p.is_file() and not p.suffix
    ]
    for fnam in binaries:
        os.remove(fnam)


class Args(NamedTuple):
    benchmark: str
    is_list: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Run a mypyc benchmark in compiled and/or interpreted modes."
    )
    parser.add_argument(
        "benchmark",
        nargs="?",
        help="name of benchmark to run (use --list to show options)",
    )
    parser.add_argument(
        "--list", action="store_true", help="show names of all benchmarks"
    )
    parser.add_argument(
        "--raw", action="store_true", help="use machine-readable raw output"
    )
    parsed = parser.parse_args()
    if parsed.raw:
        global raw_output
        raw_output = True

    if not parsed.list and not parsed.benchmark:
        parser.print_help()
        sys.exit(2)
    args = Args(parsed.benchmark, parsed.list)
    return args


def get_all_benchmarks():
    import_all()
    return benchmarks


def list_benchmarks():
    for benchmark in sorted(benchmarks):
        if benchmark.compiled_variant:
            # Don't show benchmarks with compiled_variants twice
            continue
        suffix = ""
        if not raw_output:
            if benchmark.module.startswith("microbenchmarks."):
                suffix += " (micro)"
            if benchmark.compiled_only:
                suffix += " (compiled only)"
        print(benchmark.name + suffix)


def get_benchmark(name: str) -> BenchmarkInfo:
    for benchmark in benchmarks:
        if benchmark.name == name and not benchmark.compiled_variant:
            return benchmark
    sys.exit("unknown benchmark %r" % name)


def main() -> None:

    args = parse_args()
    if args.is_list:
        list_benchmarks()
        sys.exit(0)

    benchmark = get_benchmark(args.benchmark)

    interpreted_times = run_benchmark(benchmark, BenchmarkMode.interpreted)
    compiled_times = run_benchmark(benchmark, BenchmarkMode.translated)

    print_stats("interpreted", interpreted_times)
    print_stats("compiled", compiled_times)
    delete_binaries()


def print_stats(label: str, times: list[float]):
    mean = statistics.mean(times)
    print(
        f"{label}: avg: {statistics.mean(times):.6f}s cv: {100*statistics.stdev(times)/mean:g}% iterations: {len(times)} "
    )


delete_binaries()
# Import before parsing args so that syntax errors get reported.
import_all()

if __name__ == "__main__":
    main()
