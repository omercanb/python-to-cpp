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
from tqdm import tqdm
from typing_extensions import Final

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tests.benchmarks.mypyc_benchmarks import record
from tests.benchmarks.mypyc_benchmarks.runbench import (
    BenchmarkMode,
    get_all_benchmarks,
    import_all,
    run_benchmark,
    run_interpreted,
)


def main():
    pass


def record_python_baselines():
    benchmarks = get_all_benchmarks()
    benchmark_map = {benchmark.name: benchmark for benchmark in benchmarks}
    for benchmark in tqdm(benchmark_map):
        times = run_benchmark(
            benchmark_map[benchmark], BenchmarkMode.interpreted, min_iter=20
        )
        record.write_to_csv(
            benchmark, BenchmarkMode.interpreted, times, override_save=True
        )


if __name__ == "__main__":
    main()
