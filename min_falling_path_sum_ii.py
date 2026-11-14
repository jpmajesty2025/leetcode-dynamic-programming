"""
Given an n x n integer matrix grid, return the minimum sum of a falling path with non-zero shifts.

A falling path with non-zero shifts is a choice of exactly one element from each row of grid such that 
no two elements chosen in adjacent rows are in the same column.
"""

def min_falling_path_sum(grid: list[list[int]]) -> int:
    """Return the minimum sum of a falling path with non-zero shifts through the given grid."""
    if not grid or not grid[0]:
        return 0

    n = len(grid)

    # Create a DP table to store the minimum falling path sums
    dp = [[0] * n for _ in range(n)]
    dp[0] = grid[0][:]  # Initialize the first row

    # Fill the DP table
    for i in range(1, n):
        for j in range(n):
            # Get the minimum value from the previous row's possible positions (excluding the same column)
            min_prev = dp[i - 1][0 if j != 0 else 1]
            for k in range(n):
                if k != j:
                    min_prev = min(min_prev, dp[i - 1][k])
            dp[i][j] = grid[i][j] + min_prev

    # The answer is the minimum value in the last row of the DP table
    return min(dp[-1])