# class A:
#     def __init__(self, x: int) -> None:
#         self.x = x
#
#
# class B:
#     def __init__(self, a: A, y: str) -> None:
#         self.a = a
#         self.y = y
#
#     def printA(self) -> None:
#         print(self.a.x)
#
#
# class C:
#     def __init__(self, x: str, y: str) -> None:
#         self.x = x
#         self.y = y
#
#     def combine(self) -> str:
#         return self.x + self.y
#
#
# def add(a: int, b: int) -> int:
#     return a + b
#
#
# def mul(a: int) -> int:
#     return 2 * a
#
#
# def main() -> int:
#     a = 3 + 4 * 5
#     c = a / 2
#     d: float = a
#     e = add(a, d)
#     l: list[int] = []
#     mul(3)
#     z = mul
#     print(z(a))
#     l.append(2)
#     l.append(4)
#     l.extend(l)
#     l.extend(l)
#     cls = B(A(10), "hi")
#     stuf = C("hi", "hello")
#     print(stuf.combine())
#     print(l, a)
#     print(l.count(2))
#     i = 0
#     while i < 10:
#         print(i)
#         i += 1
#     cls.printA()
#     cls.a = A(20)
#     cls.printA()
#     print(cls.a.x)
#     print(len(l))
#     l.extend(l)
#     print(len(l))
#     print(l)
#     print(l[0], l[1])
#     return 0
#
