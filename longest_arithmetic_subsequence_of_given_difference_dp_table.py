"""LeetCode 1218: index-based reference DP.

Integer values and any integer difference are supported; empty input returns 0.
Input is not modified. O(n²) time and O(n) stored integers under constant-cost
arithmetic. Prefer value-keyed DP for large inputs.
"""


def longest_subsequence(arr: list[int], difference: int) -> int:
    """Track the longest valid subsequence ending at each input index."""
    lengths = [1] * len(arr)
    for end, value in enumerate(arr):
        for previous in range(end):
            if value - arr[previous] == difference:
                lengths[end] = max(lengths[end], lengths[previous] + 1)
    return max(lengths, default=0)


class Solution:
    """LeetCode submission interface."""

    def longestSubsequence(self, arr: list[int], difference: int) -> int:
        return longest_subsequence(arr, difference)
