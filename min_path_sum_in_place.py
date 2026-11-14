"""Minimum path sum by overwriting grid cells with prefix-optimal costs.

MUTATES the input. Rows must be distinct, independently stored mutable lists.
Rectangular integer grids are required; signed values also work.
Empty grids return 0; ragged grids raise ValueError before any mutation.
O(mn) time and O(1) auxiliary space under constant-cost arithmetic.
Copying the grid to preserve it would require O(mn) extra storage.
"""


def min_path_sum(grid: list[list[int]]) -> int:
    """Replace each cell with its minimum reachable prefix cost."""
    if not grid:
        return 0
    n = len(grid[0])
    if any(len(row) != n for row in grid):
        raise ValueError("grid must be rectangular")
    if n == 0:
        return 0

    for row in range(len(grid)):
        for column in range(n):
            if row == 0 and column == 0:
                continue
            if row == 0:
                grid[row][column] += grid[row][column - 1]
            elif column == 0:
                grid[row][column] += grid[row - 1][column]
            else:
                grid[row][column] += min(
                    grid[row - 1][column], grid[row][column - 1]
                )
    return grid[-1][-1]


class Solution:
    """LeetCode submission interface; overwrites the supplied grid."""

    def minPathSum(self, grid: list[list[int]]) -> int:
        return min_path_sum(grid)
