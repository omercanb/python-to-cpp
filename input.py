from tests.benchmarks.benchmarking import benchmark


@benchmark()
def multiple_assignment() -> None:
    x = 0
    y = 1
    a = [2, 3]
    n = 0
    for i in range(1000000):
        x, y = y, x
        a[0], a[1] = a[1], a[0]
        xx, yy = a[0], a[1]
        n += x + xx
    assert n == 3000000, n


def main() -> int:
    multiple_assignment()
    return 0
