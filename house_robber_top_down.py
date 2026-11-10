"""LeetCode 198: House Robber using top-down memoization.

Accept nonnegative house values; return 0 for empty input.
Time: O(n). Auxiliary space: O(n), including cache and recursion stack.
The input is not modified. Intended for the problem's n <= 100 constraint;
use an iterative implementation for inputs near Python's recursion limit.
"""

from functools import cache


def rob(nums: list[int]) -> int:
    """At index i, either skip this house or take it and skip its neighbor."""

    @cache
    def best_from(i: int) -> int:
        if i >= len(nums):
            return 0
        return max(best_from(i + 1), nums[i] + best_from(i + 2))

    # The cache belongs to this invocation, never to another caller's input.
    return best_from(0)


class Solution:
    """LeetCode submission interface."""

    def rob(self, nums: list[int]) -> int:
        return rob(nums)
