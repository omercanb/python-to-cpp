def main() -> int:
    a = 1
    b = 2
    c = 3
    print()
    print(a)
    print(a, b, c)
    print(end="end")
    print(sep="sep")
    print(a, b, c, sep="-")
    print(a, end="()")
    print(b, end="()")
    print(c)
    # Orders swapped
    print(a, b, c, end="end", sep="sep")

    return 0
