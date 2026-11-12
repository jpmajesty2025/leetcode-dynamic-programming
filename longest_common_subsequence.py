"""LeetCode 1143: Longest Common Subsequence using one-row DP.

Return the length only; characters may be skipped but not reordered.
Empty strings return 0. No external state is modified.
For lengths m and n, nonempty inputs take O(mn) time and
O(min(m, n)) auxiliary space under constant-cost integer operations.
An empty input returns in O(1) time and space.
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Track prefix LCS lengths with shorter-string columns and an old diagonal."""
    if not text1 or not text2:
        return 0
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    dp = [0] * (len(text2) + 1)
    for character in text1:
        diagonal = 0
        for j, other in enumerate(text2, start=1):
            above = dp[j]  # Previous row, before overwriting this cell.
            if character == other:
                dp[j] = diagonal + 1
            else:
                dp[j] = max(above, dp[j - 1])
            diagonal = above
    return dp[-1]


class Solution:
    """LeetCode submission interface."""

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        return longest_common_subsequence(text1, text2)
