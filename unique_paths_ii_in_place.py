"""LeetCode 63: overwrite obstacles and open cells with reachable path counts.

MUTATES the supplied rectangular binary grid. Rows must be distinct mutable
lists, not aliases. Empty grids return 0. Ragged grids raise ValueError before
mutation. O(mn) time and O(1) auxiliary variables under constant-cost integer
arithmetic; copying the input first would cost O(mn) additional storage.
"""


def unique_paths_with_obstacles(obstacleGrid: list[list[int]]) -> int:
    """Replace each cell with the number of legal paths reaching it."""
    if not obstacleGrid:
        return 0
    columns = len(obstacleGrid[0])
    if any(len(row) != columns for row in obstacleGrid):
        raise ValueError("grid must be rectangular")
    if columns == 0:
        return 0

    for row in range(len(obstacleGrid)):
        for column in range(columns):
            if obstacleGrid[row][column] == 1:
                obstacleGrid[row][column] = 0
            elif row == 0 and column == 0:
                obstacleGrid[row][column] = 1
            else:
                above = obstacleGrid[row - 1][column] if row > 0 else 0
                left = obstacleGrid[row][column - 1] if column > 0 else 0
                obstacleGrid[row][column] = above + left
    return obstacleGrid[-1][-1]


class Solution:
    """LeetCode submission interface; overwrites the supplied grid."""

    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        return unique_paths_with_obstacles(obstacleGrid)
