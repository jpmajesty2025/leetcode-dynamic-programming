"""LeetCode 1218: sorted coordinates and binary-search predecessor lookup.

Input order is preserved. Empty input returns 0; any integer difference works.
O(n log(n + 1)) worst-case comparison/arithmetic operations and O(n) peak
auxiliary storage, including sorting. The final DP has u distinct-value cells.
Unlike hash DP, lookup uses binary search; integer costs can grow with bit size.
"""

from bisect import bisect_left


def longest_subsequence(arr: list[int], difference: int) -> int:
    """Use sorted unique coordinates, but process values in original order."""
    coordinates: list[int] = []
    for value in sorted(arr):
        if not coordinates or value != coordinates[-1]:
            coordinates.append(value)

    lengths = [0] * len(coordinates)
    best = 0
    for value in arr:
        index = bisect_left(coordinates, value)
        predecessor = value - difference
        previous = bisect_left(coordinates, predecessor)
        candidate = 1
        if previous < len(coordinates) and coordinates[previous] == predecessor:
            candidate += lengths[previous]
        # Read before writing, including when difference == 0.
        lengths[index] = candidate
        best = max(best, candidate)
    return best


class Solution:
    """LeetCode submission interface."""

    def longestSubsequence(self, arr: list[int], difference: int) -> int:
        return longest_subsequence(arr, difference)
