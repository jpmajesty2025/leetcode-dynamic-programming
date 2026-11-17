"""LeetCode 1035: sparse matching with increasing-position tails.

Preserve both integer arrays; empty input returns 0 immediately.
For nonempty lengths m, n and r equal-value index pairs, expected time is
O(m + n + r * log(min(m, n) + 1)); auxiliary storage is O(min(m, n)).
Hash lookups are expected constant time; integer operation costs can grow.
Dense duplicates can make this slower than ordinary O(mn) prefix DP.
"""

from bisect import bisect_left


def max_uncrossed_lines(nums1: list[int], nums2: list[int]) -> int:
    """Visit matching positions backward to avoid reusing an input index."""
    if not nums1 or not nums2:
        return 0
    if len(nums1) < len(nums2):
        nums1, nums2 = nums2, nums1

    positions: dict[int, list[int]] = {}
    for index, value in enumerate(nums2):
        positions.setdefault(value, []).append(index)

    tails: list[int] = []
    for value in nums1:
        # Descending positions prevent two matches from this same occurrence.
        for position in reversed(positions.get(value, [])):
            length = bisect_left(tails, position)
            if length == len(tails):
                tails.append(position)
            else:
                tails[length] = position
    return len(tails)


class Solution:
    """LeetCode submission interface."""

    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:
        return max_uncrossed_lines(nums1, nums2)
