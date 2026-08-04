def main() -> int:
    [n for n in range(10)]
    x = 20
    [x for x in range(x)]
    {x: x for x in range(x) if x % 2 == 0}
    [x for x in range(x) if x % 2 for y in range(x) if y % 2]
    y = 10
    z = [1, 2, 3]
    [x for x in zip(z, range(x))]
    return 0
