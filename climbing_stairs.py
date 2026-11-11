"""LeetCode 70: Climbing Stairs using rolling dynamic programming.

Count ordered sequences of one- and two-step moves totaling n.
LeetCode specifies 1 <= n <= 45. As extensions, n = 0 returns 1
(the empty route) and negative n raises ValueError.

O(n) additions and O(1) integer variables. For unbounded n, the result
has O(n) bits: O(n^2) bit-time and O(n) auxiliary bits with linear-time
integer addition. The input is assumed to be an integer.
"""


def climb_stairs(n: int) -> int:
    """Return the route count, retaining only two consecutive counts."""
    if n < 0:
        raise ValueError("n must be nonnegative")

    previous, current = 1, 1  # Ways to reach stairs 0 and 1.
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


class Solution:
    """LeetCode submission interface."""

    def climbStairs(self, n: int) -> int:
        return climb_stairs(n)
