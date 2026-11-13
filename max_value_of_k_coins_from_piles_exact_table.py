"""LeetCode 2218: full-table exact-k prefix knapsack.

Accept integer values, including zero and negatives; preserve input order.
Raise ValueError for negative k or fewer than k available coins.
For n piles, S = sum(min(len(pile), k) for pile in piles):
O(n(k + 1) + kS) time, O((n + 1)(k + 1)) auxiliary space.
"""


def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    """dp[i][count] is the best exact-count value from the first i piles."""
    if k < 0 or k > sum(map(len, piles)):
        raise ValueError("k must be between zero and the total coin count")
    if k == 0:
        return 0

    dp: list[list[int | None]] = [
        [None] * (k + 1) for _ in range(len(piles) + 1)
    ]
    dp[0][0] = 0
    for index, pile in enumerate(piles, start=1):
        prefix = [0]
        for position in range(min(len(pile), k)):
            prefix.append(prefix[-1] + pile[position])

        for count in range(k + 1):
            best = dp[index - 1][count]
            for take in range(1, min(len(prefix) - 1, count) + 1):
                previous = dp[index - 1][count - take]
                if previous is not None:
                    candidate = previous + prefix[take]
                    if best is None or candidate > best:
                        best = candidate
            dp[index][count] = best

    result = dp[-1][k]
    assert result is not None
    return result


class Solution:
    """LeetCode submission interface."""

    def maxValueOfCoins(self, piles: list[list[int]], k: int) -> int:
        return max_value_of_coins(piles, k)
