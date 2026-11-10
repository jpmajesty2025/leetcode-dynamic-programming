# House Robber: DP Tables, Memoization & Verification (Part 2 of 2) ⚡

In Part 1, we reduced House Robber's DP table to **two rolling totals**, reaching O(n) time and O(1) auxiliary space.

Keeping more state can still be useful when explaining the recurrence or extending the result beyond a maximum total.

---

### 🚀 Alternative 1: Prefix DP Table

Define **`dp[k]` as the best total from the first k houses**, with `dp[0] = 0`.

For each house, compare:
1. **Skip**: Keep `dp[k - 1]`.
2. **Take**: Add the current amount to `dp[k - 2]`, using zero when there's no earlier prefix.

**Why keep the table?**
Every prefix optimum is available to inspect. The stored values can also support a later traceback to recover selected houses, with a tie-breaking policy.

The current function returns only the total; reconstruction isn't implemented.

---

### 💡 Alternative 2: Top-Down Memoization

At index `i`, compare skipping to `i + 1` with taking the current amount and continuing at `i + 2`.

**The Cache Invariant**:
For a fixed input, the optimum from index `i` depends only on that suffix. Caching by index avoids evaluating the same subproblem repeatedly.

The cache lives **inside `rob()`**, so separate calls don't reuse stale results from different inputs.

**Python Caveat**:
The recursion stack grows with n. This version suits the problem's n <= 100 constraint; iteration is the safer default for large inputs.

---

### 📊 Complexity Comparison

- **Rolling Totals**: O(n) time, **O(1) auxiliary space**.
- **Prefix Table**: O(n) time, O(n) auxiliary space.
- **Memoization**: O(n) time, O(n) auxiliary space, including the recursion stack.

All three leave the input unchanged. Bounds assume constant-cost arithmetic for bounded values.

---

### 🧪 Verification

**71 pytest tests passed**, including Hypothesis checks.

- **Boundary Cases**: Empty input, singleton houses, zeros, ties, and maximum problem-size inputs.
- **Exhaustive Inputs**: All 1,093 arrays of length 0 through 6 over `{0, 1, 2}`, checked per implementation.
- **Independent Oracle**: Enumerate subsets and reject adjacent selections, without using the DP recurrence.
- **State Safety**: Input preservation and repeated calls, including changed input between calls.
- **Properties**: Reversal, zero padding, nonnegative scaling, and zero-separated additivity.

Both iterative implementations also passed a **10,000-house case**. The recursive version wasn't included in that large-input check.

---

### 🎯 Choosing an Implementation

Use **rolling totals** when only the maximum amount is needed. Keep the **table** for inspecting states or extending to reconstruction. Use **memoization** to study the recursive formulation, while accounting for stack depth.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode #SoftwareEngineering
