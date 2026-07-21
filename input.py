def main() -> int:
    nums = [1, 2, 3, 4, 5]
    nums2: list[int] = [2]
    for n in map(lambda x: 2 * x, nums):
        nums2.append(n)
    print(nums)
    print(nums2)
    print(list(map(lambda x: x * 2, nums)))
    return 0
