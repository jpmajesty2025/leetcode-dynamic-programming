"""LeetCode 931: overwrite matrix cells with minimum falling-prefix costs.

MUTATES the input. Rows must be distinct mutable lists, not aliases.
Rectangular integer matrices are supported. Empty matrices return 0;
ragged matrices raise ValueError before mutation. O(mn) time and O(1)
auxiliary variables under constant-cost arithmetic. Copying the input to
preserve it would require O(mn) additional storage.
"""


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    """Accumulate costs using only the already-completed preceding row."""
    if not matrix:
        return 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("matrix must be rectangular")
    if columns == 0:
        return 0

    for row in range(1, len(matrix)):
        for column in range(columns):
            best = matrix[row - 1][column]
            if column > 0:
                best = min(best, matrix[row - 1][column - 1])
            if column + 1 < columns:
                best = min(best, matrix[row - 1][column + 1])
            matrix[row][column] += best
    return min(matrix[-1])


class Solution:
    """LeetCode submission interface; overwrites the supplied matrix."""

    def minFallingPathSum(self, matrix: list[list[int]]) -> int:
        return min_falling_path_sum(matrix)
