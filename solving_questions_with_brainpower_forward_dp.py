"""LeetCode 2140 using forward dynamic programming.

For valid [points, brainpower] pairs with positive integer values.
Empty input returns 0. The nested input is not modified.
Time: O(n). Auxiliary space: O(n), assuming constant-cost arithmetic.
"""


def most_points(questions: list[list[int]]) -> int:
    """Propagate scores along skip and solve edges to available positions."""
    n = len(questions)
    dp = [0] * (n + 1)

    for i, (points, brainpower) in enumerate(questions):
        # All incoming edges to i have been processed; dp[i] is finalized.
        dp[i + 1] = max(dp[i + 1], dp[i])
        next_question = min(n, i + brainpower + 1)
        dp[next_question] = max(dp[next_question], dp[i] + points)

    return dp[n]


class Solution:
    """LeetCode submission interface."""

    def mostPoints(self, questions: list[list[int]]) -> int:
        return most_points(questions)
