"""LeetCode 198: House Robber using a prefix DP table.

Accept nonnegative house values; return 0 for empty input.
Time: O(n). Auxiliary space: O(n). The input is not modified.
"""


def rob(nums: list[int]) -> int:
    """Let dp[k] be the best total from the first k houses."""
    dp = [0] * (len(nums) + 1)

    for k, amount in enumerate(nums, start=1):
        skip = dp[k - 1]
        take = amount + (dp[k - 2] if k >= 2 else 0)
        dp[k] = max(skip, take)

    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def rob(self, nums: list[int]) -> int:
        return rob(nums)
