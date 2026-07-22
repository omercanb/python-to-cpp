def main() -> int:
    a = 1
    b = 2
    c = 3
    print(a < b < c)
    print(a > b)
    print(a > b > c)
    d = 3
    print(c <= d)
    print(a == d)
    print(c == d)
    l1 = [1, 2, 3]
    l2 = [1, 2, 3]
    print(l1 is l1)
    print(l1 is l2)
    return 0
