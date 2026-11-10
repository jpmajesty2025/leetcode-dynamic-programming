"""LeetCode 300 using ending-at-index dynamic programming.

Time: O(n^2). Auxiliary space: O(n), assuming constant-cost comparisons.
Empty input returns 0. The input is not modified.
"""


def length_of_lis(nums: list[int]) -> int:
    """dp[i] is the longest strictly increasing subsequence ending at i."""
    if not nums:
        return 0

    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


class Solution:
    """LeetCode submission interface."""

    def lengthOfLIS(self, nums: list[int]) -> int:
        return length_of_lis(nums)
