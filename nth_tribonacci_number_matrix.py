"""LeetCode 1137: Tribonacci with binary matrix exponentiation.

Require a nonnegative integer index; negative indices raise ValueError.
O(log(n + 1)) arithmetic operations and a constant number of stored integers.
Exact large integers grow with n; this is not logarithmic bit time or
constant bit space. No floating-point arithmetic or recursion is used.
"""


def _multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    """Multiply two 3-by-3 integer matrices without changing either input."""
    return [
        [sum(first[row][k] * second[k][column] for k in range(3))
         for column in range(3)]
        for row in range(3)
    ]


def tribonacci(n: int) -> int:
    """Apply the recurrence transition n - 2 times to [T2, T1, T0]."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 0
    if n <= 2:
        return 1

    power = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
    result = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    exponent = n - 2
    while exponent:
        if exponent & 1:
            result = _multiply(result, power)
        exponent >>= 1
        if exponent:
            power = _multiply(power, power)

    # The initial vector is [1, 1, 0].
    return result[0][0] + result[0][1]


class Solution:
    """LeetCode submission interface."""

    def tribonacci(self, n: int) -> int:
        return tribonacci(n)
