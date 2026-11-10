"""LeetCode 300: Longest Increasing Subsequence.

Return the length of a strictly increasing subsequence; equal values do not
extend it. Empty input returns 0, and the input is not modified.
Time: O(n log n). Auxiliary space: O(n), assuming constant-cost comparisons.
"""

from bisect import bisect_left


def length_of_lis(nums: list[int]) -> int:
    """Maintain the smallest possible tail for each attainable length.

    tails[k] is the minimum ending value of a subsequence of length k + 1
    in the processed prefix. The tails list is not necessarily a subsequence.
    """
    tails: list[int] = []
    for value in nums:
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)


class Solution:
    """LeetCode submission interface."""

    def lengthOfLIS(self, nums: list[int]) -> int:
        return length_of_lis(nums)
