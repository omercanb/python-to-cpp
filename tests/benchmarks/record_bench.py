"""
The interface for recording and reading benchmark runs to/from the benchmarks csv
Ensures that writes to the csv are correct
"""

import csv
import datetime
import statistics
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from tests.benchmarks.run_bench import BenchmarkMode

default_csv = Path(__file__).resolve().parent / "benchmarks.csv"

headers = [
    "benchmark",
    "mode",
    "commit",
    "datetime",
    "mean",
    "cv",
    "min",
    "p50",
    "p90",
    "p99",
    "max",
    "times",
]


def compute_row(benchmark: str, mode: BenchmarkMode, times: list[float]):
    stats = compute_statistics(times)
    commit = get_git_commit_hash()
    date = datetime.datetime.now()
    row = {
        "benchmark": benchmark,
        "mode": mode.name,
        "commit": commit,
        "datetime": date,
        **stats,
        "times": ";".join(f"{time}" for time in times),
    }
    return row


def compute_statistics(times: list[float]) -> dict[str, float]:
    arr = np.array(times)
    p50, p90, p99 = np.percentile(arr, [50, 90, 99])
    min_time = np.min(arr)
    max_time = np.max(arr)
    mean = np.mean(arr)
    cv = np.std(arr) / mean
    return {
        "mean": mean,
        "cv": cv,
        "min": min_time,
        "p50": p50,
        "p90": p90,
        "p99": p99,
        "max": max_time,
    }


def get_git_commit_hash() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, capture_output=True
    )
    return result.stdout.strip().decode()


def check_commit_is_clean():
    result = subprocess.run(
        ["git", "status", "--porcelain"], check=True, capture_output=True
    )
    if result.stdout.strip() or result.stderr.strip():
        raise ValueError(
            "git commit is not clean so benchmark run cannot be saved. Commit before trying to save the benchmark or run without --save on."
        )


def has_header(csv):
    lines = open(csv).readlines()
    return len(lines) > 0


def write_to_csv(
    benchmark: str,
    mode: BenchmarkMode,
    times: list[float],
    csv_file=default_csv,
    override_save=False,
):
    if not override_save:
        check_commit_is_clean()

    row = compute_row(benchmark, mode, times)
    with open(csv_file, "a", newline="") as f:
        writer = csv.DictWriter(f, headers)
        if not has_header(csv_file):
            writer.writeheader()
        writer.writerow(row)
