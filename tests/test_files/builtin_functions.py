def main() -> int:
    numbers = [4, 1, 7, 3]
    empty: list[int] = []

    print(sum(numbers), sum(empty))
    print(min(numbers), max(numbers))
    print(min(3, 8), max(3, 8), min(2.5, 1.5))

    # any/all take Iterable[object], so the list is named to keep its own type
    zeros = [0, 0]
    with_zero = [1, 0, 2]
    print(any(numbers), any(zeros), any(empty))
    print(all(numbers), all(with_zero), all(empty))

    # anything iterable, not just lists
    print(sum(range(5)), max(range(5)))
    print(sum({1, 2, 3}))
    print(min("hello"), max("hello"))

    print(divmod(7, 2), divmod(-7, 2))

    # Python rounds halves to even
    print(round(2.5), round(3.5), round(-2.5))
    print(round(2.567, 1), round(2.567, 2))
    print(round(5))

    print(chr(65), ord("A"))
    print(chr(ord("a") + 1))

    # sum over the values a comprehension produced
    print(sum([v * 2 for v in numbers]))

    return 0
