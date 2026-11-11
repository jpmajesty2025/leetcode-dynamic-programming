"""LeetCode 322: Coin Change using denomination-first dynamic programming.

Return the fewest coins forming amount, or -1 if unreachable. Coins may
be reused without limit. Inputs are assumed to be integers; negative amounts
and nonpositive denominations raise ValueError, even when amount is zero.
Empty denominations return 0 for amount zero and -1 otherwise.
The input is not modified.

For m denominations and target A, time is O(mA + m + A), usually written
O(mA) for positive m and A. Auxiliary space is O(A + 1).
These are pseudo-polynomial bounds under constant-cost integer arithmetic.
"""


def coin_change(coins: list[int], amount: int) -> int:
    """After each coin, dp[x] is optimal using processed denominations."""
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    if any(coin <= 0 for coin in coins):
        raise ValueError("coin denominations must be positive")

    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        # Ascending order permits repeated use of the current denomination.
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return -1 if dp[amount] == unreachable else dp[amount]


class Solution:
    """LeetCode submission interface."""

    def coinChange(self, coins: list[int], amount: int) -> int:
        return coin_change(coins, amount)
