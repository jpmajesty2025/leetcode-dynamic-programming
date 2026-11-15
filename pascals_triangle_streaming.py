"""Stream Pascal rows or materialize the complete triangle.

Integer row counts <= 0 produce no rows. iter_rows uses O(r) live integer
entries internally; consumers retaining all rows still use Theta(r²) entries.
Yielded lists are independent snapshots: caller edits cannot alter later rows.
All rows together take Theta(r²) arithmetic work, assuming constant-cost
integer arithmetic. Exact integer sizes grow with the row index.
"""

from collections.abc import Iterator


def iter_rows(numRows: int) -> Iterator[list[int]]:
    """Yield fresh row snapshots while privately retaining the previous row."""
    previous: list[int] = []
    for index in range(numRows):
        current = [1] * (index + 1)
        for column in range(1, index):
            current[column] = previous[column - 1] + previous[column]
        previous = current
        yield current.copy()


def generate(numRows: int) -> list[list[int]]:
    """Materialize the iterator to preserve the original return interface."""
    return list(iter_rows(numRows))


class Solution:
    """LeetCode submission interface."""

    def generate(self, numRows: int) -> list[list[int]]:
        return generate(numRows)
