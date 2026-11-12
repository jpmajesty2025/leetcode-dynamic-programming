"""LeetCode 188: Best Time to Buy and Sell Stock IV using O(k) space.

Prices are nonnegative integers. Return the maximum realized profit from
at most k nonoverlapping buy/sell pairs, without modifying prices.
A nonpositive budget or fewer than two days returns 0.

For n days and 0 < k < n // 2: O(nk) time, O(k) auxiliary space.
For k >= n // 2: O(n) time, O(1) auxiliary space.
"""


def max_profit(k: int, prices: list[int]) -> int:
    """Track cash and holding balances for each transaction budget."""
    n = len(prices)
    if k <= 0 or n < 2:
        return 0
    if k >= n // 2:
        return sum(max(prices[i] - prices[i - 1], 0) for i in range(1, n))

    # cash[t]: best flat balance with at most t completed transactions.
    # hold[t]: best balance while holding, with at most t - 1 completed.
    cash = [0] * (k + 1)
    hold = [-prices[0]] * (k + 1)

    for day in range(1, n):
        price = prices[day]
        # Descending budgets preserve yesterday's cash[t - 1].
        for t in range(k, 0, -1):
            cash[t] = max(cash[t], hold[t] + price)
            # Sell first so cash[t] reads yesterday's hold[t].
            hold[t] = max(hold[t], cash[t - 1] - price)
    return cash[k]


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, k: int, prices: list[int]) -> int:
        return max_profit(k, prices)
