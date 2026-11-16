"""LeetCode 213: House Robber II using slice-free linear ranges.

Assume nonnegative integer values. Empty input returns 0. Input is preserved.
O(n + 1) time, O(1) auxiliary variables under constant-cost arithmetic.
"""


def rob(nums: list[int]) -> int:
    """Break the circle by excluding either endpoint, then take the maximum."""
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]

    def rob_range(start: int, stop: int) -> int:
        two_back = one_back = 0
        for index in range(start, stop):
            two_back, one_back = one_back, max(one_back, two_back + nums[index])
        return one_back

    return max(rob_range(0, n - 1), rob_range(1, n))


class Solution:
    """LeetCode submission interface."""

    def rob(self, nums: list[int]) -> int:
        return rob(nums)
