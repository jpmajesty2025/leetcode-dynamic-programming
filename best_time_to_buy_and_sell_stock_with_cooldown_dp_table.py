"""LeetCode 309: explicit per-day holding, sold, and resting states.

Prices are nonnegative integers; input is not modified. Fewer than two days
return 0. O(n) time and O(n) auxiliary space (constant-cost arithmetic).
The table is for inspection; this interface returns profit, not a trade plan.
"""


def max_profit(prices: list[int]) -> int:
    """Only yesterday's resting state may fund a purchase today."""
    n = len(prices)
    if n < 2:
        return 0

    hold = [0] * n
    sold: list[int | None] = [None] * n
    rest = [0] * n
    hold[0] = -prices[0]
    # sold[0] is unreachable: no share was held before day zero.
    for day in range(1, n):
        price = prices[day]
        hold[day] = max(hold[day - 1], rest[day - 1] - price)
        sold[day] = hold[day - 1] + price
        rest[day] = rest[day - 1]
        previous_sale = sold[day - 1]
        if previous_sale is not None:
            rest[day] = max(rest[day], previous_sale)

    final_sale = sold[-1]
    assert final_sale is not None  # n >= 2.
    return max(rest[-1], final_sale)


class Solution:
    """LeetCode submission interface."""

    def maxProfit(self, prices: list[int]) -> int:
        return max_profit(prices)
