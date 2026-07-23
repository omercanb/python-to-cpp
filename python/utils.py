from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

from python.formatting import *


def compile_proc(translated: str, src="main.cpp", exe="main", std="c++17"):
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    # 2. compile:  g++ main.cpp -o main
    compile_proc = subprocess.run(
        ["g++", f"-std={std}", f"-Icpp", src, "-o", exe],
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


def build_and_run(translated: str, src="main.cpp", exe="main", std="c++17"):
    """Write `translated` to a .cpp file, compile with g++, run it, print output."""
    compile_proc(translated, src, exe, std)
    run_proc = subprocess.run(["stdbuf", "-oL", f"./{exe}"])
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")


def build_and_run_capture(
    translated: str, src: str | None = None, exe: str | None = None, std="c++17"
) -> subprocess.CompletedProcess:
    """Write `translated` to a .cpp file, compile with g++, run it, print output.

    Defaults to a fresh directory per call, so parallel test workers don't
    overwrite each other's main.cpp/main. Pass src/exe to write somewhere
    specific.
    """
    with tempfile.TemporaryDirectory() as directory:
        src = src or f"{directory}/main.cpp"
        exe = exe or f"{directory}/main"
        compile_proc(translated, src, exe, std)

        run_proc = subprocess.run(
            ["stdbuf", "-oL", Path(exe).resolve()], capture_output=True, text=True
        )
    # print("--- program output ---")
    # print(run_proc.stdout, end="")
    if run_proc.stderr:
        print("--- stderr ---")
        print(run_proc.stderr, end="")
    print(f"--- exit code: {run_proc.returncode} ---")
    return run_proc
