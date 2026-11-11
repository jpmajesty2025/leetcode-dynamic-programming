"""LeetCode 70 using Fibonacci fast doubling: ways(n) = F(n + 1).

O(log(n + 1)) arithmetic operations and O(1) large-integer variables.
This is not a logarithmic bit-time claim: integers have O(n + 1) bits,
so multiplication costs depend on their size. Auxiliary bit space is O(n + 1).
The input is assumed to be an integer; negative n raises ValueError.
"""


def climb_stairs(n: int) -> int:
    """Compute F(n + 1) by scanning its index from the highest bit."""
    if n < 0:
        raise ValueError("n must be nonnegative")

    target = n + 1
    a, b = 0, 1  # F(k), F(k + 1) for the index prefix processed so far.
    for shift in range(target.bit_length() - 1, -1, -1):
        even = a * (2 * b - a)  # F(2k)
        odd = a * a + b * b  # F(2k + 1)
        if (target >> shift) & 1:
            a, b = odd, even + odd
        else:
            a, b = even, odd
    return a


class Solution:
    """LeetCode submission interface."""

    def climbStairs(self, n: int) -> int:
        return climb_stairs(n)
