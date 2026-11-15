# Target Sum: Sign Assignments Become Subsets (Part 1 of 2) 🧩

**The Problem**:
Place + or - before every number and count expressions that evaluate to target.

For `[1, 1, 1, 1, 1]` and target 3, the answer is **5**: any one of the five positions can carry the minus sign.

---

### 💡 Split the Indices into Two Groups

Let P be the sum of numbers assigned + and N the sum assigned -.

With total S:
- **`P - N = target`**.
- **`P + N = S`**.

Therefore:
**`P = (S + target) // 2`**

Count index subsets with this sum. Every subset specifies exactly which positions receive +; all remaining positions receive -.

Equal values at different indices remain separate choices.

---

### ⚠️ Check Both Sides of the Reachable Range

A target is impossible if:
1️⃣ **`abs(target) > S`**.
2️⃣ **`S + target` is odd**.

---

### 🧩 Count Subsets with Descending Updates

**`dp[s]` counts subsets of processed indices whose values sum to s.**

Start with `dp[0] = 1`, representing the empty subset.

For each value, process sums downward:
`dp[s] += dp[s - value]`

Descending order keeps each positive-valued index available only once. Ascending order would allow repeated use of the current number.

---

### 🔍 Zeros Must Double the Count

For a zero value, the transition becomes:
**`dp[s] += dp[s]`**

That's correct: +0 and -0 are different sign choices even though they produce the same sum.

For `[0, 0, 1]` and target 1, there are **4** expressions.

Removing duplicate values or skipping zeros would lose valid assignments.

---

### 📊 Complexity & Quality

For n values and feasible subset size p:
- **Time**: O(n(p + 1)).
- **Auxiliary Space**: O(p + 1) stored integers.

These are pseudo-polynomial bounds: work depends on numeric sums, not just their encoded length. Python counts remain exact as they grow.

The range-check fix preserves the API and input list. The subset reduction assumes nonnegative values, as in LeetCode's contract.

---

### 🚀 What's Next?

Part 2 uses target symmetry to allocate for the smaller subset, then compares a sparse map that counts signed sums directly.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Knapsack #LeetCode #CodingInterview
