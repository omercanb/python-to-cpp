def main() -> int:
    nums = [1, 2, 3, 4, 5]
    a = list(map(lambda x: x * 2, nums))
    print(a)
    for s in map(lambda x: str(x), nums):
        print(s)
    filtered = list(filter(lambda x: x % 2 == 0, nums))
    print(filtered)
    for x, y in zip(nums, a):
        print(x, y)
    nums = a
    for i, n in enumerate(nums):
        print(i, n)
    return 0
