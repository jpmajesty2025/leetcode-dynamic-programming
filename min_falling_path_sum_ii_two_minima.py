"""Minimum non-zero-shift falling path using two minima per preceding row.

Nonmutating. Accept rectangular integer grids, including negative values.
Empty grids return 0. Ragged grids and multirow single-column grids raise
ValueError. For m rows and n columns: O(mn) time, O(n) stored integers,
under constant-cost arithmetic.
"""


def min_falling_path_sum(grid: list[list[int]]) -> int:
    """Choose the cheapest preceding entry outside the current column."""
    if not grid:
        return 0
    columns = len(grid[0])
    if any(len(row) != columns for row in grid):
        raise ValueError("grid must be rectangular")
    if columns == 0:
        return 0
    if len(grid) == 1:
        return min(grid[0])
    if columns == 1:
        raise ValueError("no legal path through multiple single-column rows")

    previous = grid[0].copy()
    for row in range(1, len(grid)):
        first_column = min(range(columns), key=previous.__getitem__)
        first = previous[first_column]
        # Equal-valued entries at other columns remain eligible.
        second = min(previous[j] for j in range(columns) if j != first_column)
        previous = [
            grid[row][j] + (second if j == first_column else first)
            for j in range(columns)
        ]
    return min(previous)


class Solution:
    """LeetCode submission interface."""

    def minFallingPathSum(self, grid: list[list[int]]) -> int:
        return min_falling_path_sum(grid)
