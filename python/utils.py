from __future__ import annotations

import os
import subprocess
import tempfile
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Mapping

from python.formatting import *

# clang, not g++: only its precompiled headers pay off (0.45s -> 0.07s a compile)
COMPILER = "clang++"
CPP_DIR = Path("cpp")
PCH_HEADER = CPP_DIR / ".pch.h"
PCH_FILE = CPP_DIR / ".pch.h.pch"


def ensure_pch(std: str) -> Path | None:
    """Build a precompiled header of cpp/*.h, refreshing it when one changes."""
    # Skip our own generated header, or it ends up including itself.
    headers = sorted(h for h in CPP_DIR.glob("*.h") if h != PCH_HEADER)
    if not headers:
        return None
    if PCH_FILE.exists() and PCH_FILE.stat().st_mtime >= max(
        h.stat().st_mtime for h in headers
    ):
        return PCH_FILE

    PCH_HEADER.write_text("".join(f'#include "{h.name}"\n' for h in headers))
    # Build to a private path and rename, so a parallel worker refreshing at the
    # same time can never leave a half-written pch behind.
    temporary = PCH_FILE.with_suffix(f".{os.getpid()}.tmp")
    built = subprocess.run(
        [COMPILER, f"-std={std}", f"-I{CPP_DIR}", "-fpch-instantiate-templates",
         "-x", "c++-header", str(PCH_HEADER), "-o", str(temporary)],
        capture_output=True,
        text=True,
    )
    if built.returncode != 0:
        temporary.unlink(missing_ok=True)
        # Warn, don't print: pytest swallows prints on a passing run, which is
        # how a broken pch stayed unnoticed once already.
        warnings.warn(
            f"precompiled header failed to build, compiling without it "
            f"(expect a ~4x slower compile):\n{built.stderr}",
            stacklevel=2,
        )
        return None
    os.replace(temporary, PCH_FILE)
    return PCH_FILE


def compile_cpp(
    src: str, exe: str, includes: list[str] | None = None, std: str = "c++17"
) -> subprocess.CompletedProcess:
    """Compile `src` to `exe` using the precompiled header."""
    directories = [str(CPP_DIR)] + (includes or [])

    def run(pch: Path | None):
        command = [COMPILER, f"-std={std}"] + [f"-I{d}" for d in directories]
        if pch is not None:
            command += ["-include-pch", str(pch)]
        return subprocess.run(command + [src, "-o", exe], capture_output=True, text=True)

    compiled = run(ensure_pch(std))
    if compiled.returncode != 0 and "precompiled header" in compiled.stderr:
        # clang rejects a stale pch rather than using it, so just drop it.
        warnings.warn(
            f"precompiled header rejected, recompiling {src} without it "
            f"(expect a ~4x slower compile):\n{compiled.stderr}",
            stacklevel=2,
        )
        compiled = run(None)
    return compiled


def compile_proc(translated: str, src="main.cpp", exe="main", std="c++17"):
    Path(src).write_text(translated)
    print(f"--- wrote {src} ---\n{translated}\n")

    compiled = compile_cpp(src, exe, std=std)
    if compiled.returncode != 0:
        print("--- compile FAILED ---")
        print(compiled.stderr)
        return  # stop: no binary to run
    if compiled.stderr:  # warnings still compile
        print("--- compiler warnings ---")
        print(compiled.stderr)


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
