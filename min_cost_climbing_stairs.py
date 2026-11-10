"""LeetCode 746: Min Cost Climbing Stairs.

Start at position 0 or 1 for free; pay cost[i] when leaving step i.
The top is position len(cost) and has no cost.

Constraints: 2 <= len(cost) <= 1000; 0 <= cost[i] <= 999.
Empty and singleton inputs also return 0. The input is not modified.
Time: O(n). Auxiliary space: O(1), for bounded-integer arithmetic.
"""


def min_cost_climbing_stairs(cost: list[int]) -> int:
    """Track minimum costs to reach the previous two positions."""
    two_back = one_back = 0

    for k in range(2, len(cost) + 1):
        current = min(one_back + cost[k - 1], two_back + cost[k - 2])
        two_back, one_back = one_back, current

    return one_back


class Solution:
    """LeetCode submission interface."""

    def minCostClimbingStairs(self, cost: list[int]) -> int:
        return min_cost_climbing_stairs(cost)
