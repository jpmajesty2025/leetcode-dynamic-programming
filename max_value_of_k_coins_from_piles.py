"""
There are n piles of coins on a table. Each pile consists of a positive number of coins of assorted denominations.

In one move, you can choose any coin on top of any pile, remove it, and add it to your wallet.

Given a list piles, where piles[i] is a list of integers denoting the composition of the ith pile from top to bottom, 
and a positive integer k, return the maximum total value of coins you can have in your wallet if you choose exactly 
k coins optimally.
"""

def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    n = len(piles)
    dp = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        prefix_sum = [0]
        for coin in piles[i - 1]:
            prefix_sum.append(prefix_sum[-1] + coin)

        for j in range(k + 1):
            dp[i][j] = dp[i - 1][j]
            for x in range(min(len(piles[i - 1]), j) + 1):
                dp[i][j] = max(dp[i][j], dp[i - 1][j - x] + prefix_sum[x])

    return dp[n][k]