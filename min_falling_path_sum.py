"""
Given an n x n array of integers matrix, return the minimum sum of any falling path through matrix.

A falling path starts at any element in the first row and chooses the element in the next row that is either 
directly below or diagonally left/right. Specifically, the next element from position (row, col) will be 
(row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).
"""

def min_falling_path_sum(matrix: list[list[int]]) -> int:
    """Return the minimum sum of any falling path through the given matrix."""
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)

    # Create a DP table to store the minimum falling path sums
    dp = [[0] * n for _ in range(n)]
    dp[0] = matrix[0][:]  # Initialize the first row

    # Fill the DP table
    for i in range(1, n):
        for j in range(n):
            # Get the minimum value from the previous row's possible positions
            min_prev = dp[i - 1][j]
            if j > 0:
                min_prev = min(min_prev, dp[i - 1][j - 1])
            if j < n - 1:
                min_prev = min(min_prev, dp[i - 1][j + 1])
            dp[i][j] = matrix[i][j] + min_prev

    # The answer is the minimum value in the last row of the DP table
    return min(dp[-1])