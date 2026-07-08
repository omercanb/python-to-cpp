int(3)


def main():
    global x
    x = 20
    print(x)


# print(x)

y = 10


class A:
    a = 42
    b = a

    # c = list(A.a + i for i in range(10))
    def __init__(self):
        d = list(A.a + i for i in range(10))
        print(y)


class X:
    a = 10
    b = 10

    def __init__(self):
        self.a = 20

    def bull():
        print(X)

    class Y:
        pass


one = X()
two = X()
X.a = 100
one.a = 50
print("start")
print(X.a, one.a)
print(X.a, two.a)

a = b = 3
print(id(a), id(b))
a = 2
print(a, b)

l = [a for a in range(10) for a in range(a, 10)]
print(l)


# a = A()
# a.a = 10
# other_a = A()
# other_a.a = 20
# print(a.a)
# print(other_a.a)

#
# def a():
#     x = 10
#     def b():
#         nonlocal x
#         def c():
#             x = 20
#         c()
#     b()
#     print(x)
# a()
