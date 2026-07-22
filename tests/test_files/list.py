def get_list() -> list[int]:
    return [1, 2, 3, 4, 5]


def main() -> int:
    l = get_list()
    for n in l:
        print(n)
    l2 = ["a", "b", "c"]
    l2 = ["a", "a", "a"]
    l3 = list([0, 1, 0, 1])
    return 0
