"""LeetCode 2140: Solving Questions With Brainpower.

Each question is [points, brainpower]. Solve it and skip the next
brainpower questions, or skip it and consider the next question.
Return the maximum total score without modifying the nested input.

Constraints: 1 <= len(questions) <= 100_000; both values are in
[1, 100_000]. Empty input is also supported and returns 0.
Time: O(n). Auxiliary space: O(n), assuming constant-cost arithmetic.
"""


def most_points(questions: list[list[int]]) -> int:
    """dp[i] is the best score from the suffix starting at available index i."""
    n = len(questions)
    dp = [0] * (n + 1)

    # Every dependency is to the right, so evaluate suffixes backward.
    for i in range(n - 1, -1, -1):
        points, brainpower = questions[i]
        next_question = i + brainpower + 1
        # A resume position at or beyond the end contributes no more points.
        solve = points + (dp[next_question] if next_question < n else 0)
        dp[i] = max(dp[i + 1], solve)

    return dp[0]


class Solution:
    """LeetCode submission interface."""

    def mostPoints(self, questions: list[list[int]]) -> int:
        return most_points(questions)
