from __future__ import annotations

import argparse
import glob
import os
import re
import statistics
import subprocess
import sys
import time
from importlib import import_module
from pathlib import Path
from typing import NamedTuple

from benchmarking import BenchmarkInfo, benchmarks
from typing_extensions import Final

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from main import pipeline
from python import utils
from python.utils import compile_proc
from tests.benchmarks.mypyc_benchmarks.runbench import get_all_benchmarks, import_all


def main() -> None:
    print(get_all_benchmarks())
    benchmarks = map(lambda x: x.name, get_all_benchmarks())
    print(list(benchmarks))


if __name__ == "__main__":
    main()
