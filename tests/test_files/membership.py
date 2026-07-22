def main() -> int:
    l = [1, 2, 3]
    print(2 in l, 9 in l)
    print(2 not in l, 9 not in l)

    d = {1: 10, 2: 20}
    # `in` on a dict tests keys, not values
    print(1 in d, 9 in d)
    print(10 in d.values())
    print(1 not in d, 9 not in d)

    s = {1, 2, 3}
    print(2 in s, 9 in s)
    print(2 not in s, 9 not in s)

    text = "hello world"
    print("hello" in text, "zz" in text)
    print("o w" in text)
    print("hello" not in text, "zz" not in text)

    t = (1, 2, 3)
    print(2 in t, 9 in t)

    # Tuples as the elements rather than the container. Each container
    # needs tuple equality, and set/dict additionally need tuple hashing.
    pairs = [(1, 2), (3, 4)]
    print((1, 2) in pairs, (9, 9) in pairs)
    print((1, 2) not in pairs, (9, 9) not in pairs)
    # Order matters: (2, 1) is a different key from (1, 2)
    print((2, 1) in pairs)

    pair_set = {(1, 2), (3, 4)}
    print((1, 2) in pair_set, (9, 9) in pair_set)
    print((2, 1) in pair_set)

    pair_dict = {(1, 2): "a", (3, 4): "b"}
    print((1, 2) in pair_dict, (9, 9) in pair_dict)

    nested = ((1, 2), (3, 4))
    print((1, 2) in nested, (9, 9) in nested)

    mixed = [("a", 1), ("b", 2)]
    print(("a", 1) in mixed, ("a", 2) in mixed)

    strs = ["a", "b"]
    print("a" in strs, "z" in strs)

    # Chained with other comparisons, and used as a condition
    if 2 in l:
        print("found")
    else:
        print("missing")

    count = 0
    for x in [1, 2, 3, 4]:
        if x in s:
            count = count + 1
    print(count)

    return 0
