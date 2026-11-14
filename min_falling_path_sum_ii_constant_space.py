"""Minimum non-zero-shift falling path using constant-size row summaries.

Preserve input. Support rectangular integer grids, including negatives.
Empty grids return 0. Ragged shapes and multirow single-column grids raise
ValueError. O(mn) time, O(1) auxiliary integer variables under constant-cost
arithmetic. Integer bit sizes grow with accumulated path sums.
"""


def min_falling_path_sum(grid: list[list[int]]) -> int:
    """Stream each row's two cheapest endpoint costs at distinct columns."""
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

    first = second = 0
    first_column = -1  # Virtual initial row: every starting column is legal.
    for row in grid:
        next_first: int | None = None
        next_second: int | None = None
        next_column = -1
        for column, value in enumerate(row):
            cost = value + (second if column == first_column else first)
            if next_first is None or cost < next_first:
                next_second = next_first
                next_first, next_column = cost, column
            elif next_second is None or cost < next_second:
                # A tie for first is a valid second entry at another column.
                next_second = cost
        assert next_first is not None and next_second is not None
        first, second, first_column = next_first, next_second, next_column
    return first


class Solution:
    """LeetCode submission interface."""

    def minFallingPathSum(self, grid: list[list[int]]) -> int:
        return min_falling_path_sum(grid)
