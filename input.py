def main() -> int:
    nums = [1, 2, 3, 4, 5]
    nums2: list[int] = [2]
    for n in map(lambda x: 2 * x, nums):
        nums2.append(n)
    print(nums)
    print(nums2)
    return 0
