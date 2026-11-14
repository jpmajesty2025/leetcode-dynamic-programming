"""LeetCode 309: stock trading with a one-day cooldown after selling.

Prices are nonnegative integers. Return realized profit without modifying input.
Fewer than two days return 0. O(n) time, O(1) auxiliary space under
constant-cost integer arithmetic.
"""


def max_profit(prices: list[int]) -> int:
    """Buy from the flat balance two days earlier, never yesterday's sale."""
    n = len(prices)
    if n < 2:
        return 0

    cash, hold = 0, -prices[0]
    cash_two_days_ago = 0  # Flat balance before the first day.
    for day in range(1, n):
        price = prices[day]
        cash, hold, cash_two_days_ago = (
            max(cash, hold + price),
            max(hold, cash_two_days_ago - price),
            cash,
        )
    return cash


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, prices: list[int]) -> int:
        return max_profit(prices)
