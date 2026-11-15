"""LeetCode 1137: Tribonacci using a full sequence table.

Require a nonnegative integer index; negative indices raise ValueError.
O(n + 1) arithmetic operations and stored integers. For unrestricted n,
integer sizes grow: these are not constant-cost bit-complexity bounds.
"""


def tribonacci(n: int) -> int:
    """Store the initial values and extend the three-term recurrence."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 0
    if n <= 2:
        return 1

    values = [0, 1, 1]
    for index in range(3, n + 1):
        values.append(values[index - 3] + values[index - 2] + values[index - 1])
    return values[n]


class Solution:
    """LeetCode submission interface."""

    def tribonacci(self, n: int) -> int:
        return tribonacci(n)
