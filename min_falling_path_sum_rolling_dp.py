"""LeetCode 931: minimum falling path sum with rolling rows.

Accept rectangular integer matrices, including negative values. Empty matrices
return 0; ragged matrices raise ValueError. Input is not modified.
For m rows and n columns, O(mn) time and O(n) auxiliary stored integers,
assuming constant-cost arithmetic. The movement rules are not transposed.
"""


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    """Keep every predecessor in the previous row until the new row is ready."""
    if not matrix:
        return 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("matrix must be rectangular")
    if columns == 0:
        return 0

    previous = matrix[0].copy()
    for row in range(1, len(matrix)):
        current = [0] * columns
        for column in range(columns):
            best = previous[column]
            if column > 0:
                best = min(best, previous[column - 1])
            if column + 1 < columns:
                best = min(best, previous[column + 1])
            current[column] = matrix[row][column] + best
        previous = current
    return min(previous)


class Solution:
    """LeetCode submission interface."""

    def minFallingPathSum(self, matrix: list[list[int]]) -> int:
        return min_falling_path_sum(matrix)
