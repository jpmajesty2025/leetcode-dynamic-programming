"""LeetCode 213: House Robber II with explicit prefix optima.

Assume nonnegative integer values; empty input returns 0. No input mutation.
O(n + 1) time and O(n + 1) auxiliary stored integers under constant-cost
arithmetic. Returns the optimal amount, not a reconstructed house selection.
"""


def rob(nums: list[int]) -> int:
    """Compare two linear prefix tables that each omit a circular endpoint."""
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]

    def rob_range(start: int, stop: int) -> int:
        length = stop - start
        dp = [0] * (length + 1)
        dp[1] = nums[start]
        for count in range(2, length + 1):
            dp[count] = max(dp[count - 1], dp[count - 2] + nums[start + count - 1])
        return dp[-1]

    return max(rob_range(0, n - 1), rob_range(1, n))


class Solution:
    """LeetCode submission interface."""

    def rob(self, nums: list[int]) -> int:
        return rob(nums)
