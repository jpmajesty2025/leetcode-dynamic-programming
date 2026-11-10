"""LeetCode 746 using top-down memoization with an explicit stack.

Evaluate the suffix recurrence without Python recursion: n can be 1000.
For nonnegative costs, including empty/singleton inputs (result 0).
Time: O(n). Auxiliary space: O(n). Does not modify the input.
"""


def min_cost_climbing_stairs(cost: list[int]) -> int:
    """Memoize the minimum remaining cost when leaving each step."""
    n = len(cost)
    if n < 2:
        return 0

    memo = {n: 0, n + 1: 0}
    for start in (0, 1):
        stack = [start]
        while stack:
            i = stack[-1]
            if i in memo:
                stack.pop()
            elif i + 1 not in memo:
                stack.append(i + 1)
            elif i + 2 not in memo:
                stack.append(i + 2)
            else:
                memo[i] = cost[i] + min(memo[i + 1], memo[i + 2])
                stack.pop()

    return min(memo[0], memo[1])


class Solution:
    """LeetCode submission interface."""

    def minCostClimbingStairs(self, cost: list[int]) -> int:
        return min_cost_climbing_stairs(cost)
