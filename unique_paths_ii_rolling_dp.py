"""LeetCode 63: obstacle-aware path counting with shorter-dimension storage.

Input must be a rectangular binary grid. Empty grids return 0; ragged grids
raise ValueError. Input is not modified. O(mn) worst-case time and
O(min(m, n)) auxiliary stored integers for nonempty grids, assuming
constant-cost arithmetic. Python integers preserve exact large counts.
"""


def unique_paths_with_obstacles(obstacleGrid: list[list[int]]) -> int:
    """Combine predecessor counts, clearing any count at an obstacle."""
    if not obstacleGrid:
        return 0
    rows, columns = len(obstacleGrid), len(obstacleGrid[0])
    if any(len(row) != columns for row in obstacleGrid):
        raise ValueError("grid must be rectangular")
    if columns == 0:
        return 0
    if obstacleGrid[0][0] == 1 or obstacleGrid[-1][-1] == 1:
        return 0

    transposed = columns > rows
    outer, inner = (columns, rows) if transposed else (rows, columns)
    dp = [0] * inner
    dp[0] = 1  # Seed the single empty path at the open start.
    for i in range(outer):
        for j in range(inner):
            blocked = obstacleGrid[j][i] if transposed else obstacleGrid[i][j]
            if blocked == 1:
                dp[j] = 0
            elif j > 0:
                # Previous outer iteration plus updated current predecessor.
                dp[j] += dp[j - 1]
    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        return unique_paths_with_obstacles(obstacleGrid)
