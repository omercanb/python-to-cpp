def read(a: list[int], i: int) -> int:
    return a[i]


def write(a: list[int], i: int, v: int) -> None:
    a[i] = v


def last(a: list[int]) -> int:
    return a[-1]


def set_last(a: list[int], v: int) -> None:
    a[-1] = v


def slice_full(a: list[int]) -> list[int]:
    return a[1:3]


def slice_open(a: list[int]) -> list[int]:
    return a[:2]


def tuple_index(pair: tuple[int, int]) -> int:
    return pair[0]


def matrix_get(m: list[list[int]], i: int, j: int) -> int:
    return m[i][j]


def matrix_set(m: list[list[int]], i: int, j: int, v: int) -> None:
    m[i][j] = v
