def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    if n in memo:
        return memo[n]
    
    memo[n] = fibonacci(n - 1) + fibonacci(n - 2)
    return memo[n]

memo = {}