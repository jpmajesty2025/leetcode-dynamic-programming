"""LeetCode 1143 using a full prefix DP table.

Return the length only, without modifying external state.
For nonempty strings of lengths m and n: O(mn) time and auxiliary space.
Empty inputs return 0 in O(1) time and space.
Bounds assume constant-cost integer operations.
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    """dp[i][j] is the LCS length of text1[:i] and text2[:j]."""
    if not text1 or not text2:
        return 0
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


class Solution:
    """LeetCode submission interface."""

    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        return longest_common_subsequence(text1, text2)
