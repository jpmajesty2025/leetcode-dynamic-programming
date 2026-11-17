"""LeetCode 1035: Uncrossed Lines using one-row LCS dynamic programming.

Return the count only; do not modify either integer array. Empty inputs return
0 in O(1) time and space. Nonempty lengths m, n take O(mn) time and
O(min(m, n)) auxiliary stored integers under constant-cost arithmetic.
"""


def max_uncrossed_lines(nums1: list[int], nums2: list[int]) -> int:
    """Preserve above, updated-left, and previous-diagonal prefix optima."""
    if not nums1 or not nums2:
        return 0
    if len(nums1) < len(nums2):
        nums1, nums2 = nums2, nums1

    dp = [0] * (len(nums2) + 1)
    for value in nums1:
        diagonal = 0
        for column, other in enumerate(nums2, start=1):
            above = dp[column]
            if value == other:
                dp[column] = diagonal + 1
            else:
                dp[column] = max(above, dp[column - 1])
            diagonal = above
    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:
        return max_uncrossed_lines(nums1, nums2)
