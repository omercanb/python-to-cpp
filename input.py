class A:
    def __init__(self, num: int) -> None:
        self.num = num

    class B:
        def __init__(self, field: str) -> None:
            self.field = field

        def b(self) -> None:
            print(self)


class C:
    pass


# int(3)
#
#
# class A:
#     a = b = 10
#     c: int
#
#     def __init__(self):
#         self.y = self.x = 10
#         self.z: int
#         self.l: float = 10
#
#     def hi(self):
#         print("hi")
#
#
# def fun(arg):
#     for x in range(10):
#         print(x)
#
#     y = [row for i in range(10) for row in range(i, 10)]
#     x = [b for b in range(10)]
#     a = 10
#
#     # matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#     # odds = [entry for row in matrix for entry in row]
#     # print(odds)
#
#     def inner():
#         a = 10
#         a = 20
#
#
# fun(10)


# class A:
#     def __init__(self, x: int) -> None:
#         self.x = x
#
#     pass
#
#
# class B:
#     def __init__(self, a: A) -> None:
#         print(a)
#         self.a = a
#
#
# B
#
#
# class C:
#     def __init__(self, some_bullshii: str) -> None:
#         self.z = some_bullshii
#
#     def do_shit(self) -> None:
#         print(self)
#
#     def recurse(self, x: int) -> int:
#         if x > 10:
#             return x + self.recurse(x - 1)
#         return 0
#
#     class Hello:
#         def ohmygor(self) -> int:
#             return 2
#
#
# C
#
#
# def fun(x: int, y: A) -> None:
#     class B:
#         pass
#
#     a = B()
#     pass
#
#
# # fmt: off
# l = [a for 
#      a in range(10)
#      for b in 
#      range(a, 10)]
# fmt: on

# def add(x: int, y: int) -> int:
#     print(x, y)
#     return x + y
#

# def loop(x: int) -> None:
#     if x > 0:
#         print(x)
#         loop(x - 1)
#
#
# def show(x: list[int]) -> None:
#     i = 10
#     while i > 10:
#         print(x)
#         i -= 1


#
# global_x = 10
# def combinator() -> None:
#     print(global_x)
#     global_x -= 1
#     if global_x > 0:
#         combinator()
#         combinator()
#         combinator()
#         combinator()
#
# def range(start: int, end: int) -> None:
#     if start >= end:
#         return
#     print(start)
#     range(start + 1, end)
#
#
#
# def main() -> int:
#     # l: list[int]
#     # n: tuple[int, list[str]]
#     # m: tuple[int, float, str, bool]
#     x = 10
#     y = 20
#     z = x + y
#     print(z)
#     a = 0.4
#     b  = 2*a + (x)
#     print(b)
#     c = a / b
#     d: float = 1.0
#     print(a, b, c)
#
#
#     i: int
#     i = 20
#     i += 2
#     i %= 10
#     #print("i: ", i)
#
#     if i > 10:
#         print(i)
#     else:
#         print(d)
#
#     if a or b and c:
#         print(a)
#     if ((a or b) or c) and d:
#         print()
#     if a <= b < c <= d:
#         print()
#
#     print(a if b else c)
#
#     # loop(5)
#
#     i = 10
#     while i > 5:
#         print(i)
#         i -= 1
#
#     j = 0
#     while j < 20:
#         j += 1
#         if j % 2 == 0:
#             continue
#         print(j)
#         if j % 11 == 0:
#             break
#
#     # for k in range(10):
#     #     print(k)
#
#     h = 3
#     j: int
#
#     # combinator()
#     #
#     # range(10, 20)
#
#     q = [1, 2, 3]
#
#     l = [[3, 4], [4, 4]]
#     q = [a, b, c]
#
#     print(q)
#     print(l)
#     print(a, b, c)
#
#     l[3]
#     l.append(2)
#
#     # l: list[int]
#     # n: tuple[int, list[str]]
#     # m: tuple[int, float, str, bool]
#     return 0
#
# class C:
#     x: int
#     def __init__(self, x):
#         self.x = x
#
#     def print(self):
#         print(self.x)
