"""LeetCode 188: Stock IV using a rolling transaction row.

Prices are nonnegative integers. Return profit only, without mutating input.
A nonpositive budget or fewer than two days returns 0.
The constrained case uses O(nk) time and O(n) auxiliary space.
The unlimited-transactions shortcut uses O(n) time and O(1) space.
"""


def max_profit(k: int, prices: list[int]) -> int:
    """Overwrite prefix profits while preserving the previous row's cell."""
    n = len(prices)
    if k <= 0 or n < 2:
        return 0
    if k >= n // 2:
        return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, n))

    profits = [0] * n
    for _ in range(k):
        best_buy_balance = -prices[0]
        for day in range(1, n):
            previous_row_profit = profits[day]
            profits[day] = max(
                profits[day - 1], prices[day] + best_buy_balance
            )
            # Save the previous transaction row before overwriting it.
            best_buy_balance = max(
                best_buy_balance, previous_row_profit - prices[day]
            )
    return profits[-1]


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, k: int, prices: list[int]) -> int:
        return max_profit(k, prices)
