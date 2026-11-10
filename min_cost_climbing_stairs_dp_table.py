"""LeetCode 746 using a prefix DP table.

For nonnegative costs, including empty/singleton inputs (result 0).
Time: O(n). Auxiliary space: O(n). Does not modify the input.
"""


def min_cost_climbing_stairs(cost: list[int]) -> int:
    """dp[k] is the minimum cost to reach k, before paying cost[k]."""
    dp = [0] * (len(cost) + 1)

    for k in range(2, len(cost) + 1):
        dp[k] = min(dp[k - 1] + cost[k - 1], dp[k - 2] + cost[k - 2])

    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def minCostClimbingStairs(self, cost: list[int]) -> int:
        return min_cost_climbing_stairs(cost)
