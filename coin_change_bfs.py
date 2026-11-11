"""LeetCode 322 as a shortest-path search over amounts.

Integers are assumed. Negative amounts and nonpositive coins raise ValueError.
Empty denominations are supported. The input is not modified.
Worst-case time: O(mA + m + A). Auxiliary space: O(A + 1).
Pseudo-polynomial bounds assume constant-cost integer arithmetic.
"""

from collections import deque


def coin_change(coins: list[int], amount: int) -> int:
    """Return the depth of the first BFS arrival at the target amount."""
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    if any(coin <= 0 for coin in coins):
        raise ValueError("coin denominations must be positive")
    if amount == 0:
        return 0

    visited = bytearray(amount + 1)
    visited[0] = 1
    queue = deque([(0, 0)])

    while queue:
        total, count = queue.popleft()
        for coin in coins:
            following = total + coin
            if following == amount:
                return count + 1
            if following < amount and not visited[following]:
                visited[following] = 1
                queue.append((following, count + 1))
    return -1


class Solution:
    """LeetCode submission interface."""

    def coinChange(self, coins: list[int], amount: int) -> int:
        return coin_change(coins, amount)
