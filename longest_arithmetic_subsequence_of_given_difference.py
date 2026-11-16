"""
Given an integer array arr and an integer difference, return the length of the longest subsequence in 
arr which is an arithmetic sequence such that the difference between adjacent elements in the subsequence 
equals difference.

A subsequence is a sequence that can be derived from arr by deleting some or no elements without changing 
the order of the remaining elements.
"""

def longest_subsequence(arr: list[int], difference: int) -> int:
    """Return the length of the longest subsequence in arr which is an arithmetic sequence with the given difference."""
    dp = {}
    max_length = 0

    for num in arr:
        # The previous number in the arithmetic sequence would be num - difference
        prev_num = num - difference
        # If prev_num is in dp, we can extend that subsequence; otherwise, start a new subsequence
        dp[num] = dp.get(prev_num, 0) + 1
        max_length = max(max_length, dp[num])

    return max_length