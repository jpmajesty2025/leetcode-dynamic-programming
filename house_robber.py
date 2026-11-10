"""LeetCode 198: House Robber.
https://leetcode.com/problems/house-robber/

Return the maximum sum of nonadjacent house values without changing nums.
The problem specifies 1 <= len(nums) <= 100 and 0 <= nums[i] <= 400.
An empty list is also supported and returns 0.

Time: O(n). Auxiliary space: O(1), under the usual bounded-integer model.
"""


def rob(nums: list[int]) -> int:
    """Find the best total using only the previous two prefix optima."""
    two_back = one_back = 0

    for amount in nums:
        # Both right-hand values use the state before this house.
        two_back, one_back = one_back, max(one_back, two_back + amount)

    return one_back


class Solution:
    """LeetCode submission interface."""

    def rob(self, nums: list[int]) -> int:
        return rob(nums)
