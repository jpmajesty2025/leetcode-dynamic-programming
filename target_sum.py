"""
You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in 
nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build 
the expression "+2-1".
Return the number of different expressions that you can build, which evaluates to target.
"""

def find_target_sum_ways(nums: list[int], target: int) -> int:
    """Return the number of different expressions that evaluate to target."""
    total_sum = sum(nums)
    
    # The sum of the positive numbers must be (target + total_sum) / 2
    if abs(target) > total_sum or (target + total_sum) % 2 != 0:
        return 0
    
    positive_sum = (target + total_sum) // 2
    
    # Initialize a dp array where dp[i] is the number of ways to reach sum i
    dp = [0] * (positive_sum + 1)
    dp[0] = 1  # There's one way to reach sum 0: use no numbers

    cnt = 0
    for num in nums:
        print(f"iter: {cnt} Processing number: {num} \n begin inner loop...")
        for j in range(positive_sum, num - 1, -1):
            print(f'j: {j}, before dp[{j}] = {dp[j]}')
            dp[j] += dp[j - num]
            print(f'after dp[{j}] = {dp[j]}')
        print('\n***end inner loop***\n')
        cnt += 1
    
    return dp[positive_sum]

nums = [1,2,3,4]
target = 4
res = find_target_sum_ways(nums, target)
print(f"Number of different expressions that evaluate to {target}: {res}")