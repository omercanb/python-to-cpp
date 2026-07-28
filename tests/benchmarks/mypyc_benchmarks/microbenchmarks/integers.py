from benchmarking import benchmark


@benchmark()
def int_bitwise_ops() -> None:
    a: list[int] = []
    for i in range(1000):
        a.append(i * i * 12753 % (2**20 - 1))
    b: list[int] = []
    for t in range(40):
        b.append(a[10 + t])
    n = 0
    for i in range(50):
        for j in a:
            for k in b:
                j |= k
                j &= ~(j ^ k)
                x = j >> 5
                n += x
                n += x << 1
                n &= 0xFFFFFF
    assert n == 4867360


@benchmark()
def int_bitwise_ops2() -> None:
    a: list[int] = []
    for i in range(1000):
        a.append(i * i * 2654435761 & 0xFFFFFFFF)
    b: list[int] = []
    for t in range(49):
        b.append(a[10 + t * 10])
    n = 0
    for i in range(10):
        for j in a:
            for k in b:
                j |= k
                j &= ~(j ^ k)
                if (1 << (i * 3)) & j:
                    n += 1
                n += j & 1
    assert n == 183000
