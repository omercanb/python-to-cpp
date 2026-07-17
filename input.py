def l() -> list[int]:
    return [1, 2, 3]


def tup() -> tuple[int, float]:
    return (1, 2.0)


def main() -> int:
    lst = l()
    lst.append(3)
    return 0
