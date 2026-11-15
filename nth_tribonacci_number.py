"""
The Tribonacci sequence Tn is defined as follows: 

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

Given n, return the value of Tn.
"""

def tribonacci(n: int) -> int:
    """Return the nth Tribonacci number."""
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1

    # Initialize the first three Tribonacci numbers
    t0, t1, t2 = 0, 1, 1

    # Calculate Tribonacci numbers iteratively
    for _ in range(3, n + 1):
        t_next = t0 + t1 + t2
        t0, t1, t2 = t1, t2, t_next

    return t2