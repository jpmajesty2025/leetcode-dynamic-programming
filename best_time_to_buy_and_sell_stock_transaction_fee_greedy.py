"""LeetCode 714: effective-buy-price greedy stock trading.

Prices are nonnegative integers; fee must be nonnegative or ValueError is raised.
Return realized profit without modifying prices. Fewer than two days return 0.
O(n) time and O(1) auxiliary space (constant-cost integer arithmetic).
"""


def max_profit(prices: list[int], fee: int) -> int:
    """Book profitable rises while keeping the option to extend a trade."""
    if fee < 0:
        raise ValueError("fee must be nonnegative")
    n = len(prices)
    if n < 2:
        return 0

    profit = 0
    effective_buy = prices[0] + fee
    for day in range(1, n):
        price = prices[day]
        if price + fee < effective_buy:
            effective_buy = price + fee
        elif price > effective_buy:
            profit += price - effective_buy
            # A virtual re-entry extends this rise without a second fee.
            effective_buy = price
    return profit


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, prices: list[int], fee: int) -> int:
        return max_profit(prices, fee)
