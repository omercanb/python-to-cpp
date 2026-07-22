def main() -> int:
    a = 0
    b = 5
    if a:
        print("a truthy")
    else:
        print("a falsy")
    if b:
        print("b truthy")
    else:
        print("b falsy")

    s1 = ""
    s2 = "hello"
    if s1:
        print("s1 truthy")
    else:
        print("s1 falsy")
    if s2:
        print("s2 truthy")
    else:
        print("s2 falsy")

    empty: list[int] = []
    full = [1, 2, 3]
    if empty:
        print("empty truthy")
    else:
        print("empty falsy")
    if full:
        print("full truthy")
    else:
        print("full falsy")

    print(not a)
    print(not b)
    print(bool(a))
    print(bool(b))
    print(bool(0.0))
    print(bool(1.5))
    print(bool(True))
    print(bool(False))

    n = 3
    while n:
        print(n)
        n = n - 1

    return 0
