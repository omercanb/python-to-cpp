# mypy: disallow-untyped-defs
"""Simple, brute-force N-Queens solver."""

from tests.benchmarks.benchmarking import benchmark


def generate_permutations(values: list[int], start: int, result: list[list[int]]) -> None:
    """Fill `result` with every permutation of `values`, built eagerly."""
    n = len(values)
    if start == n:
        result.append(list(values))
        return
    for i in range(start, n):
        tmp = values[start]
        values[start] = values[i]
        values[i] = tmp

        generate_permutations(values, start + 1, result)

        tmp = values[start]
        values[start] = values[i]
        values[i] = tmp


def permutations(n: int) -> list[list[int]]:
    """All permutations of range(n), as a list built up front instead of lazily."""
    result: list[list[int]] = []
    generate_permutations(list(range(n)), 0, result)
    return result


# From http://code.activestate.com/recipes/576647/
def do_n_queens(queen_count: int) -> list[list[int]]:
    """N-Queens solver.

    Args:
        queen_count: the number of queens to solve for. This is also the
            board size.

    Returns:
        Solutions to the problem. Each returned value looks like
        [3, 8, 2, 1, 4, ..., 6] where each number is the column position for the
        queen, and the index into the list indicates the row.
    """
    cols = range(queen_count)
    solutions: list[list[int]] = []
    for vec in permutations(queen_count):
        if (queen_count == len({vec[i] + i for i in cols})
                        == len({vec[i] - i for i in cols})):
            solutions.append(vec)
    return solutions


def bench_n_queens(queen_count: int) -> None:
    do_n_queens(queen_count)


@benchmark()
def nqueens() -> None:
    queen_count = 8
    for i in range(3):
        bench_n_queens(queen_count)
