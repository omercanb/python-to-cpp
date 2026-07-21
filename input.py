# def main() -> int:
#     a = 1
#     b = 2
#     c = 3
#     print()
#     print(a)
#     print(a, b, c)
#     print(end="end")
#     print(sep="sep")
#     print(a, b, c, sep="-")
#     print(a, end="()")
#     print(b, end="()")
#     print(c)
#
#     return 0


def main() -> int:
    x = 2
    l = [2, 3, 4]
    for i in range(len(l)):
        print(l)
    for i in range(x):
        print("first", i)
    for i in range(x, x + 5):
        print("second", i)
    for i in range(x, x + 10, 2):
        print("third", i)
    for i in range(x, x - 7, -2):
        print("fourth", i)
    step = x
    for i in range(x, 10 * x, step):
        print("fifth", i)
    step = -2
    for i in range(5 * x, 10 * x, step):
        print("sixth", i)
    for n in l:
        print("seventh", n)
    l2 = [2.0, 3.0]
    r = range(10)
    return 0
