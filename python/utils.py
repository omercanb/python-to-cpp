from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

from python.formatting import *


def build_and_run(translated: str, src="main.cpp", exe="main", std="c++17"):
    """Write `translated` to a .cpp file, compile with g++, run it, print output."""
    # 1. write the source
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    # 2. compile:  g++ main.cpp -o main
    compile_proc = subprocess.run(
        ["g++", "-ggdb", f"-std={std}", f"-Icpp", src, "-o", exe],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        print("--- compile FAILED ---")
        print(compile_proc.stderr)
        return  # stop: no binary to run
    if compile_proc.stderr:  # warnings still compile
        print("--- compiler warnings ---")
        print(compile_proc.stderr)

    # 3. run ./main and print its output
    run_proc = subprocess.run(["stdbuf", "-oL", f"./{exe}"])
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")


def build_and_run_capture(
    translated: str, src="main.cpp", exe="main", std="c++17"
) -> subprocess.CompletedProcess:
    """Write `translated` to a .cpp file, compile with g++, run it, print output."""
    # 1. write the source
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    # 2. compile:  g++ main.cpp -o main
    compile_proc = subprocess.run(
        ["g++", "-ggdb", f"-std={std}", f"-Icpp", src, "-o", exe],
        capture_output=True,
        text=True,
    )
    if compile_proc.returncode != 0:
        print("--- compile FAILED ---")
        print(compile_proc.stderr)
        raise ValueError("Compile error")
    if compile_proc.stderr:  # warnings still compile
        print("--- compiler warnings ---")
        print(compile_proc.stderr)

    # 3. run ./main and print its output
    run_proc = subprocess.run(
        ["stdbuf", "-oL", f"./{exe}"], capture_output=True, text=True
    )
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")
    return run_proc
