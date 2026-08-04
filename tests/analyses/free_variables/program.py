def main() -> int:
    n = 10
    print([[x for x in range(n)] for x in range(n)])

    threshold = 5
    print([x for x in range(n) if x > threshold])

    print([x + y for x in range(n) for y in range(x)])

    a = [1, 2, 3]
    print([a[i] for i in range(n)])

    print({a: a for a in a})

    [a[i] for i in range(n)]
    return 0
