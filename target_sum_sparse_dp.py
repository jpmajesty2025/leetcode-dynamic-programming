"""LeetCode 494: count assignments with a map of reachable signed sums.

Accept integer values, including negatives; input is not modified.
Empty nums have one assignment to zero. Work is O(n + 1 + sum(R_i)) where
R_i counts states before processing element i; space is O(max(R_i, R_n)).
These expected dictionary/arithmetic bounds are not polynomial in encoded
input size: state counts can grow exponentially and integer sizes can grow.
"""


def find_target_sum_ways(nums: list[int], target: int) -> int:
    """Accumulate both sign choices, even when zero makes their sums equal."""
    total = sum(abs(value) for value in nums)
    if abs(target) > total or (total - target) % 2:
        return 0

    ways = {0: 1}
    for value in nums:
        following: dict[int, int] = {}
        for subtotal, count in ways.items():
            plus, minus = subtotal + value, subtotal - value
            following[plus] = following.get(plus, 0) + count
            following[minus] = following.get(minus, 0) + count
        ways = following
    return ways.get(target, 0)


class Solution:
    """LeetCode submission interface."""

    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        return find_target_sum_ways(nums, target)
