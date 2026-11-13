# Maximum Value of K Coins: One Row & Descending Updates (Part 2 of 2) ⚡

In Part 1, each pile offered a choice of prefixes. The full table combined those choices while tracking the number of coins selected.

For a value-only answer, **one row preserves the previous-pile dependencies**.

---

### 💡 Keep Exact Counts Explicit

**`dp[j]` is the best value of exactly j coins from the piles processed so far.**

Start with `dp[0] = 0`. All positive counts are unreachable, represented by `None`.

For each pile, build prefix sums for at most its first k coins. A longer prefix can never fit the budget.

Then consider each valid take count x:
`candidate = dp[j - x] + prefix[x]`

Skip unreachable source states and keep the best candidate, including the existing value for taking zero coins.

---

### ⚠️ Process Coin Counts Downward

Update j **from the largest reachable count down to 1**.

For x > 0, the smaller index `j - x` still belongs to the previous pile iteration. That prevents selecting the same pile's prefix multiple times.

For `[[10], [1]]` and `k = 2`, the correct answer is **11**. An ascending in-place loop can reuse the first pile's updated one-coin state and incorrectly produce **20**.

This is group knapsack: every pile contributes one prefix choice, not unlimited copies of that choice.

---

### 🚀 Bound the Useful Work

The compressed version also:
- Processes only counts reachable from the piles seen so far.
- Skips take counts that would require too many coins from earlier piles.
- Rejects negative k or a budget larger than the total coin count.

Both saved alternatives support zero and negative coin values while preserving exact-count semantics. Neither modifies the input.

---

### 📊 Complexity & Trade-Offs

For positive k under LeetCode's constraints, with M total coins:
- **Time**: O(kM), unchanged asymptotically.
- **Auxiliary Space**: **O(k)**, including the truncated prefix sums.

The separate exact-table implementation retains **O(nk)** space and keeps intermediate states visible. The compressed version returns only the maximum value; recovering the chosen prefixes would need additional bookkeeping or recomputation.

---

### 🧪 Independent Verification

The tests enumerate every combination of prefix lengths, retain combinations totaling exactly k coins, and take the largest value.

Coverage includes:
- **Exhaustive Small Inputs**: Up to three piles, each of length at most two, with coin values 1 or 2.
- **Hypothesis Properties**: Pile-order invariance, scaling, input preservation, and adding c to every coin increases the answer by exactly k × c.
- **Regressions**: Buried rewards, accidental pile reuse, empty inputs, invalid budgets, and signed-value exact counts.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Knapsack #SoftwareTesting #Hypothesis #LeetCode
