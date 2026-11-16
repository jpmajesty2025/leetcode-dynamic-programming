"""
You are a professional robber planning to rob houses along a street. Each house has a certain amount of 
money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor 
of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically 
contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of 
money you can rob tonight without alerting the police.
"""

def rob(nums: list[int]) -> int:
    """Return the maximum amount of money you can rob tonight without alerting the police."""
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    def rob_linear(houses: list[int]) -> int:
        """Helper function to rob houses in a linear arrangement."""
        prev, curr = 0, 0
        for amount in houses:
            prev, curr = curr, max(curr, prev + amount)
        return curr
    
    # Rob houses excluding the first house or excluding the last house
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))