"""LeetCode 62: Unique Paths with one-row dynamic programming.

Dimensions must be positive integers; nonpositive dimensions raise ValueError.
For m, n > 1: O(mn) additions and O(min(m, n)) stored integers.
One-dimensional grids return 1 immediately. Integer arithmetic is exact;
operation costs and integer sizes grow with the answer's bit length.
"""


def unique_paths(m: int, n: int) -> int:
    """Count right/down paths, preserving above and updated-left states."""
    if m <= 0 or n <= 0:
        raise ValueError("grid dimensions must be positive")
    if m == 1 or n == 1:
        return 1

    rows, columns = max(m, n), min(m, n)
    dp = [1] * columns
    for _ in range(1, rows):
        for column in range(1, columns):
            # dp[column] is above; dp[column - 1] is this row's left.
            dp[column] += dp[column - 1]
    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def uniquePaths(self, m: int, n: int) -> int:
        return unique_paths(m, n)
