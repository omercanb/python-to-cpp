def main() -> int:
    a = 1
    b = 2
    c = 3
    l = []
    l.append(1)
    print(l)
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


# from typing import Dict, List
#
#
# def dict_iteration() -> None:
#     a = []
#     for j in range(1000):
#         d = {}
#         for i in range(j % 10):
#             d["Foobar-%d" % j] = j
#             d["%d str" % j] = i
#         a.append(d)
#
#     n = 0
#     for i in range(1000):
#         for d in a:
#             for k in d:
#                 if k == "0 str":
#                     n += 1
#             for k in d.keys():
#                 if k == "0 str":
#                     n += 1
#             for v in d.values():
#                 if v == 0:
#                     n += 1
#             for k, v in d.items():
#                 if v == 1 or k == "1 str":
#                     n += 1
#     assert n == 202000, n
#

# def dict_to_list() -> None:
#     a = []
#     for j in range(1000):
#         d = {}
#         for i in range(j % 10):
#             d["Foobar-%d" % j] = j
#             d["%d str" % j] = i
#         a.append(d)
#
#     n = 0
#     for i in range(1000):
#         for d in a:
#             n + +len(list(d))
#             n += len(list(d.keys()))
#             n += len(list(d.values()))
#             n += len(list(d.items()))
#     assert n == 5400000, n
#
#
# def dict_set_default() -> None:
#     n = 0
#     for i in range(100 * 1000):
#         d: Dict[int, List[int]] = {}
#         for j in range(i % 10):
#             for k in range(i % 11):
#                 d.setdefault(j, []).append(k)
#         n += len(d)
#     assert n == 409095, n
#
#
# def dict_clear() -> None:
#     n = 0
#     for i in range(1000 * 1000):
#         d = {}
#         for j in range(i % 4):
#             d[j] = "x"
#         d.clear()
#         assert len(d) == 0
#
#
# def dict_copy() -> None:
#     a = []
#     for j in range(100):
#         d = {}
#         for i in range(j % 10):
#             d["Foobar-%d" % j] = j
#             d["%d str" % j] = i
#         a.append(d)
#
#     n = 0
#     for i in range(10 * 1000):
#         for d in a:
#             d2 = d.copy()
#             d3 = d2.copy()
#             d4 = d3.copy()
#             assert len(d4) == len(d)
#
#
# def dict_call_keywords() -> None:
#     n = 0
#     for i in range(1000 * 1000):
#         d = dict(id=5, name="dummy", things=[])
#         n += len(d)
#     assert n == 3000000, n
#
#
# def dict_call_generator() -> None:
#     a = []
#     for j in range(1000):
#         items = [
#             ("Foobar-%d" % j, j),
#             ("%d str" % j, "x"),
#         ]
#         if j % 2 == 0:
#             items.append(("blah", "bar"))
#         a.append(items)
#
#     n = 0
#     for i in range(1000):
#         for s in a:
#             d = dict((key, value) for key, value in s)
#             assert len(d) == len(s)
#
#
# def dict_del_item() -> None:
#     d = {"long_lived": "value"}
#     for j in range(1000 * 1000):
#         d["xyz"] = "asdf"
#         d["asdf"] = "lulz"
#         del d["xyz"]
#         d["foobar"] = "baz zar"
#         del d["foobar"]
#         del d["asdf"]
