



def add(x: int, y: int) -> int:
    print(x, y)
    return x + y

def loop(x: int) -> None:
    if x > 0:
        print(x)
        loop(x-1)

global_x = 10
def combinator() -> None:
    print(global_x)
    global_x -= 1
    if global_x > 0:
        combinator()
        combinator()
        combinator()
        combinator()

def range(start: int, end: int) -> None:
    if start >= end:
        return 
    print(start)
    range(start + 1, end)



def main():
    # l: list[int]
    # n: tuple[int, list[str]]
    # m: tuple[int, float, str, bool]
    x = 10
    y = 20
    z = x + y
    print(z)
    a = 0.4
    b  = 2*a + (x)
    print(b)
    c = a / b
    d: float = 1.0
    print(a, b, c)


    i: int
    i = 20
    i += 2
    i %= 10
    #print("i: ", i)

    if i > 10:
        print(i)
    else:
        print(d)

    if a or b and c:
        print(a)
    if ((a or b) or c) and d:
        print()
    if a <= b < c <= d:
        print()

    print(a if b else c)

    # loop(5)

    i = 10
    while i > 5:
        print(i)
        i -= 1

    j = 0
    while j < 20:
        j += 1
        if j % 2 == 0:
            continue
        print(j)
        if j % 11 == 0:
            break

    # for k in range(10):
    #     print(k)

    h = 3
    j: int

    # combinator()
    #
    # range(10, 20)

    l = [[3, 4], [4, 4]]
    
    # l: list[int]
    # n: tuple[int, list[str]]
    # m: tuple[int, float, str, bool]
