



def add(x: int, y: int) -> int:
    print(x, y)
    return x + y


def main():
    x: int = 10
    y: int = 20
    z: int = x + y
    print(z)
    a: float = 0.4
    b: float = 2 * a + 5
    print(b)
    c: float = a / b
    print(c)
    d: float = x / y;
    print(d)
    f: int
    print(a, b, c, d);

    i: int
    i = 20
    i += 2
    i /= 5
    i %= 10
    #print("i: ", i)

    if i > 10:
        print(i)
    else:
        print(d)

    if a or b or c and d:
        print(a)
    if ((a or b) or c) and d:
        print()
    if a <= b < c <= d:
        print()

    print(a if b else c)
