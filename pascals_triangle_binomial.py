"""Pascal's triangle via adjacent exact binomial coefficients.

Integer row counts <= 0 return [], matching the original API.
For r positive rows: Theta(r²) arithmetic operations and output entries,
with O(1) auxiliary integer variables beyond the returned output.
Integer operation costs and bit sizes grow with r.
"""


def generate(numRows: int) -> list[list[int]]:
    """Build each row independently using C(i, j + 1) from C(i, j)."""
    triangle: list[list[int]] = []
    for index in range(numRows):
        row = [1]
        coefficient = 1
        for column in range(1, index + 1):
            coefficient = coefficient * (index - column + 1) // column
            row.append(coefficient)
        triangle.append(row)
    return triangle


class Solution:
    """LeetCode submission interface."""

    def generate(self, numRows: int) -> list[list[int]]:
        return generate(numRows)
