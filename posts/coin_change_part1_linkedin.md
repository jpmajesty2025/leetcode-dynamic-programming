# Coin Change: Unlimited Reuse & Loop Direction (Part 1 of 2) 🪙

**The Problem**:
Given positive coin denominations and a target amount, return the **fewest coins** needed to make that amount. Each denomination can be used without limit. Return -1 if it's impossible.

For `[1, 2, 5]` and amount 11, the answer is **3**: 5 + 5 + 1.

---

### 🧩 Define the Denomination-Prefix State

After processing each denomination, **`dp[x]` is the minimum coin count for x using the denominations processed so far**.

Start with `dp[0] = 0`. All other amounts are initially unreachable.

For each coin and each amount x that can include it:
`dp[x] = min(dp[x], dp[x - coin] + 1)`

The existing value covers solutions without another current coin. The candidate adds one current coin to an optimal solution for x - coin.

---

### 💡 Why Amounts Must Ascend

For coin 3 and target 9, processing amounts upward allows:
1. Amount 3 to use the current coin once.
2. Amount 6 to reuse the updated state for 3.
3. Amount 9 to reuse the updated state for 6.

**Ascending order enables unlimited reuse.** Descending order would allow each processed coin entry at most once, solving a different availability problem.

---

### ⚠️ Greedy Isn't Enough

For `[1, 3, 4]` and amount 6:
- Taking the largest coin first gives 4 + 1 + 1: three coins.
- The optimum is **3 + 3: two coins**.

The DP compares alternatives instead of assuming that the largest available denomination belongs in an optimum.

---

### 🛠️ Unreachable States & Input Policy

The original implementation was correct. I replaced floating-point infinity with the integer sentinel **amount + 1**: any feasible solution uses at most amount positive-value coins.

The saved versions also:
- Return 0 for amount zero and -1 for unreachable amounts.
- Support empty denomination lists without modifying the input.
- Raise `ValueError` for negative amounts or nonpositive denominations, even when the amount is zero.

Those validation rules make behavior outside LeetCode's contract explicit.

---

### 📊 Complexity

For m denominations and positive target A: **O(mA) time, O(A) auxiliary space**. Including empty/zero cases, the bounds are O(mA + m + A) time and O(A + 1) space.

This is **pseudo-polynomial**: work depends on the numeric target, not just its encoded length. Bounds assume constant-cost integer arithmetic.

---

### 🚀 What's Next?

Part 2 compares amount-first DP with **BFS over reachable amounts**, then checks all three versions using independent coin-count enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
