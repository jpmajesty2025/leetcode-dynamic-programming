"""LeetCode 62: count paths by choosing positions for the less frequent move.

Positive integer dimensions are required; nonpositive values raise ValueError.
Uses O(min(m, n)) arithmetic operations and a constant number of integer
variables. This is not constant bit space: the exact result and intermediate
values grow with the grid. No factorials or floating-point operations are used.
"""


def unique_paths(m: int, n: int) -> int:
    """Compute C(m + n - 2, min(m - 1, n - 1)) by exact division."""
    if m <= 0 or n <= 0:
        raise ValueError("grid dimensions must be positive")

    moves = m + n - 2
    chosen = min(m - 1, n - 1)
    paths = 1
    for count in range(1, chosen + 1):
        # After this iteration: C(moves - chosen + count, count).
        paths = paths * (moves - chosen + count) // count
    return paths


class Solution:
    """LeetCode submission interface."""

    def uniquePaths(self, m: int, n: int) -> int:
        return unique_paths(m, n)
