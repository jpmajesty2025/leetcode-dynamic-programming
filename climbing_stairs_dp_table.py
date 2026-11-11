"""LeetCode 70 using an explicit DP table.

O(n) additions and O(n) integer entries. For unbounded n, the table
occupies O(n^2) bits and additions take O(n^2) total bit-time.
The input is assumed to be an integer; negative n raises ValueError.
"""


def climb_stairs(n: int) -> int:
    """dp[i] counts routes to stair i; dp[0] counts the empty route."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 1

    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


class Solution:
    """LeetCode submission interface."""

    def climbStairs(self, n: int) -> int:
        return climb_stairs(n)
