"""LeetCode 494: count sign assignments via the smaller subset sum.

Require nonnegative integer nums; negative elements raise ValueError.
Empty nums have one assignment to target zero, none to other targets.
Input is preserved. For feasible parity/range, q = (sum(nums) - abs(target)) // 2:
O(n(q + 1)) time, O(q + 1) stored integers, under constant-cost arithmetic.
Rejected range/parity takes O(n + 1) time and O(1) auxiliary space.
"""


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """Count index subsets; zeros double counts and duplicates stay distinct."""
    if any(value < 0 for value in nums):
        raise ValueError("nums must contain only nonnegative integers")
    total = sum(nums)
    if abs(target) > total or (total - abs(target)) % 2:
        return 0

    subset_sum = (total - abs(target)) // 2
    ways = [0] * (subset_sum + 1)
    ways[0] = 1
    for value in nums:
        # Descending sums prevent reusing this index; zero doubles each cell.
        for subtotal in range(subset_sum, value - 1, -1):
            ways[subtotal] += ways[subtotal - value]
    return ways[subset_sum]


class Solution:
    """LeetCode submission interface."""

    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        return find_target_sum_ways(nums, target)
