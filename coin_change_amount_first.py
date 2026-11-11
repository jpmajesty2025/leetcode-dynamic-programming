"""LeetCode 322 using amount-first dynamic programming.

Integers are assumed. Negative amounts and nonpositive coins raise ValueError.
Empty denominations are supported. The input is not modified.
Time: O(mA + m + A). Auxiliary space: O(A + 1).
Pseudo-polynomial bounds assume constant-cost integer arithmetic.
"""


def coin_change(coins: list[int], amount: int) -> int:
    """dp[x] is the minimum coin count for x, considering every final coin."""
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    if any(coin <= 0 for coin in coins):
        raise ValueError("coin denominations must be positive")

    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x:
                dp[x] = min(dp[x], dp[x - coin] + 1)

    return -1 if dp[amount] == unreachable else dp[amount]


class Solution:
    """LeetCode submission interface."""

    def coinChange(self, coins: list[int], amount: int) -> int:
        return coin_change(coins, amount)
