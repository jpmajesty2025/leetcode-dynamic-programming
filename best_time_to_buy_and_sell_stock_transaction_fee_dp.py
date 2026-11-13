"""LeetCode 714: stock trading with one nonnegative fee per completed trade.

Prices are nonnegative integers. Return realized profit without mutating input.
Empty or singleton inputs return 0. Negative fees raise ValueError.
O(n) time and O(1) auxiliary space (constant-cost integer arithmetic).
"""


def max_profit(prices: list[int], fee: int) -> int:
    """Keep the best flat and holding balances after each day."""
    if fee < 0:
        raise ValueError("fee must be nonnegative")
    n = len(prices)
    if n < 2:
        return 0

    cash, hold = 0, -prices[0]
    for day in range(1, n):
        price = prices[day]
        # Both right-hand sides read the previous day's states.
        cash, hold = max(cash, hold + price - fee), max(hold, cash - price)
    return cash


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, prices: list[int], fee: int) -> int:
        return max_profit(prices, fee)
