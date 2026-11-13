"""
You are given an array prices where prices[i] is the price of a given stock on the ith day, and an integer fee 
representing a transaction fee.

Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the 
transaction fee for each transaction.

Note:

You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
The transaction fee is only charged once for each stock purchase and sale.
"""

def max_profit(prices: list[int], fee: int) -> int:
    n = len(prices)
    if n < 2:
        return 0

    cash, hold = 0, -prices[0]

    for i in range(1, n):
        cash = max(cash, hold + prices[i] - fee)
        hold = max(hold, cash - prices[i])

    return cash