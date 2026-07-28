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

from tqdm import tqdm
from typing_extensions import Final

from tests.benchmarks import record_bench
from tests.benchmarks.benchmarking import BenchmarkInfo, benchmarks
from tests.benchmarks.run_bench import (
    BenchmarkMode,
    get_all_benchmarks,
    import_all,
    run_benchmark,
    run_interpreted,
)


def main():
    find_failing_translations()
    pass


def find_failing_translations():
    benchmarks = get_all_benchmarks()
    benchmark_map = {benchmark.name: benchmark for benchmark in benchmarks}
    for benchmark in tqdm(benchmark_map):
        try:
            run_benchmark(benchmark_map[benchmark], BenchmarkMode.translated)
        except Exception as e:
            print(e)


def record_python_baselines():
    benchmarks = get_all_benchmarks()
    benchmark_map = {benchmark.name: benchmark for benchmark in benchmarks}
    for benchmark in tqdm(benchmark_map):
        times = run_benchmark(
            benchmark_map[benchmark], BenchmarkMode.interpreted, min_iter=20
        )
        record_bench.write_to_csv(
            benchmark, BenchmarkMode.interpreted, times, override_save=True
        )


if __name__ == "__main__":
    main()
