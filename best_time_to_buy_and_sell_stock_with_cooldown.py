"""
You are given an array prices where prices[i] is the price of a given stock on the ith day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell 
one share of the stock multiple times) with the following restrictions:

After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

Example 1:

Input: prices = [1,2,3,0,2]
Output: 3
Explanation: transactions = [buy, sell, cooldown, buy, sell]
Example 2:

Input: prices = [1]
Output: 0
"""

def max_profit( prices: list[int]) -> int:
    n = len(prices)
    if n < 2:
        return 0

    cash, hold, cooldown = 0, -prices[0], 0

    for i in range(1, n):
        prev_cash = cash
        cash = max(cash, cooldown)
        cooldown = hold + prices[i]
        hold = max(hold, prev_cash - prices[i])

    return max(cash, cooldown)