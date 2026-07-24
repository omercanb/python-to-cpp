def num() -> int:
    return 0


def main() -> int:
    a = num()
    b = a or ""
    if b:
        print(b)
    return 0
