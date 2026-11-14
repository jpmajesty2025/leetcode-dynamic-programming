"""Minimum path sum with O(min(m, n)) auxiliary storage.

Rectangular integer grids are required; signed values also work.
Empty grids return 0. Ragged grids raise ValueError. Input is not modified.
O(mn) time for nonempty m-by-n grids under constant-cost arithmetic.
"""


def min_path_sum(grid: list[list[int]]) -> int:
    """Track predecessor costs in the shorter grid dimension."""
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    if any(len(row) != n for row in grid):
        raise ValueError("grid must be rectangular")
    if n == 0:
        return 0

    transposed = n > m
    outer, inner = (n, m) if transposed else (m, n)
    dp = [0] * inner
    for i in range(outer):
        for j in range(inner):
            value = grid[j][i] if transposed else grid[i][j]
            if i == 0 and j == 0:
                dp[j] = value
            elif i == 0:
                dp[j] = dp[j - 1] + value
            elif j == 0:
                dp[j] += value
            else:
                dp[j] = min(dp[j], dp[j - 1]) + value
    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def minPathSum(self, grid: list[list[int]]) -> int:
        return min_path_sum(grid)
