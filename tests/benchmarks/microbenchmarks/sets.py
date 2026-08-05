from typing import List, Tuple

from tests.benchmarks.benchmarking import benchmark


@benchmark()
def in_set() -> None:
    a: List[Tuple[int, int]] = []
    for j in range(100):
        for i in range(10):
            a.append((i * 2, i))
            a.append((i, i + 2))
            a.append((i, i))
            a.append((i, i))

    n = 0
    for i in range(1000):
        for s in a:
            if 6 in s:
                n += 1
            if i in {3, 4, 5}:
                n += 1
    assert n == 612000, n


@benchmark()
def set_literal_iteration() -> None:
    n = 0
    for p in range(1000):
        for l in range(10):
            for i in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}:
                n += i
            for s in {"yes", "no"}:
                if s == "yes":
                    n += 1
            for a in {True, False}:
                n += 1
    assert n == 580000, n
