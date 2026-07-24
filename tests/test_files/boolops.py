def side(v: int) -> int:
    print("SIDE")
    return v


def main() -> int:
    a: int = 1
    b: int = 2
    zero: int = 0

    # `and` / `or` yield an operand, not a bool
    print(a and b)
    print(a or b)
    print(zero and b)
    print(zero or b)
    print(zero and zero)
    print(zero or zero)

    empty: str = ""
    text: str = "hi"
    print(empty or text)
    print(text and empty)
    print(text or empty)
    print(empty and text)

    no_items: list[int] = []
    print(no_items or [1, 2])
    print([3] and no_items)
    print([3] or [4])
    print(no_items and [4])

    f: float = 0.0
    g: float = 2.5
    print(f or g)
    print(g and f)

    # the right side is skipped when the left already decides it
    print(zero and side(9))
    print(a or side(9))
    print(a and side(9))
    print(zero or side(9))

    # chained, and mixed with other operators
    print(a and b and 3)
    print(zero or zero or 3)
    print(a and b or 3)
    print(zero or b and 3)
    print((a and b) + 1)

    # conditions only need truthiness, so the operands need not share a type
    if a and text:
        print("cond and")
    if empty or a:
        print("cond or")
    if not (empty or zero):
        print("cond not")
    if a and text and b:
        print("cond chained")
    if no_items or text:
        print("cond mixed")
    if zero and side(9):
        print("unreachable")

    n: int = 0
    while n < 2 and text:
        n = n + 1
    print(n)

    # `not` yields a bool in a value position
    print(not a)
    print(not zero)
    print(not empty)
    print(not (a and b))

    return 0
