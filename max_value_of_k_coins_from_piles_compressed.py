"""LeetCode 2218: exact-k prefix knapsack with O(k) auxiliary space.

Accept integer coin values, including zero and negatives; do not mutate piles.
Raise ValueError for negative k or fewer than k available coins.
For n piles, S = sum(min(len(pile), k) for pile in piles):
O(n(k + 1) + kS) time, O(k + 1) auxiliary space.
"""


def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    """Use None for unreachable counts and preserve previous-pile states."""
    if k < 0 or k > sum(map(len, piles)):
        raise ValueError("k must be between zero and the total coin count")
    if k == 0:
        return 0

    dp: list[int | None] = [0] + [None] * k
    available = 0
    for pile in piles:
        if not pile:
            continue
        prefix = [0]
        for index in range(min(len(pile), k)):
            prefix.append(prefix[-1] + pile[index])

        previous_available = available
        available = min(k, available + len(pile))
        # Smaller counts still belong to the previous pile iteration.
        for count in range(available, 0, -1):
            best = dp[count]  # Taking zero coins from this pile.
            lower = max(1, count - previous_available)
            for take in range(lower, min(len(prefix) - 1, count) + 1):
                previous = dp[count - take]
                if previous is not None:
                    candidate = previous + prefix[take]
                    if best is None or candidate > best:
                        best = candidate
            dp[count] = best

    result = dp[k]
    assert result is not None  # Feasibility was checked before allocating.
    return result


class Solution:
    """LeetCode submission interface."""

    def maxValueOfCoins(self, piles: list[list[int]], k: int) -> int:
        return max_value_of_coins(piles, k)
