# from tests.benchmarks.benchmarking import benchmark

# @benchmark()
# def multiple_assignment() -> None:
#     x = 0
#     y = 1
#     a = [2, 3]
#     n = 0
#     for i in range(1000000):
#         x, y = y, x
#         a[0], a[1] = a[1], a[0]
#         xx, yy = a[0], a[1]
#         n += x + xx
#     assert n == 3000000, n


def main() -> int:
    # a = [1, 2, 3]
    # b = [i for i in a]
    # print(b)
    for i in range(10):
        print(i)
    for i in range(10):
        print(i)
    s = {a for a in range(10)}

    d = {a: a for a in range(10)}
    {b: b for b in range(10)}
    n = 10
    m = 10
    print([n for n in range(n) for _ in range(m)])
    # a: dict[int, int] = {}
    # a[0] = 1
    #
    # [(i, j) for i in range(10) if i % 2 if i % 3 for j in range(10) if j % 2]
    # # multiple_assignment()
    return 0


main()


# def list_remove() -> None:
#     for j in range(10 * 1000):
#         a = []
#         for i in range(10):
#             a.append(list(range(11 + i)))
#
#         for i in range(10):
#             for s in a:
#                 s.remove(i)
#
#         total = sum([len(s) for s in a])
#         assert total == 55, total
