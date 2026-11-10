# Longest Increasing Subsequence: Ending-at-Index DP (Part 1 of 2) 📈

**The Problem**:
Given an integer array, return the length of its **longest strictly increasing subsequence**.

Elements can be skipped, but their original order must be preserved.

For `[10, 9, 2, 5, 3, 7, 101, 18]`, the answer is **4**. One valid subsequence is `[2, 3, 7, 18]`.

---

### 🧩 Define the State Precisely

**`dp[i]` is the length of the longest increasing subsequence ending at index i.**

Every element forms a subsequence of length 1, so initialize every entry to 1.

For each earlier index j:
1. Check that `nums[j] < nums[i]`.
2. Extend the best subsequence ending at j.
3. Keep the largest candidate for `dp[i]`.

The update is:
`dp[i] = max(dp[i], dp[j] + 1)`

Every longer subsequence ending at i has an earlier, smaller predecessor. Checking all such predecessors covers every valid extension.

---

### ⚠️ Three Pitfalls to Watch

1️⃣ **Strictly Increasing Means No Equal Neighbors**:
For `[7, 7, 7]`, the answer is **1**, not 3. The comparison must be strict.

2️⃣ **The Optimum May End Early**:
For `[1, 2, 3, 0]`, the answer is **3**. Return `max(dp)`, not just the final entry.

3️⃣ **Subsequence Isn't Subarray**:
For `[1, 3, 5, 2, 4, 6]`, `[1, 3, 5, 6]` has length **4** even though its elements aren't contiguous.

---

### 📊 Complexity & Quality

- **Time**: O(n²), from checking every earlier index.
- **Auxiliary Space**: O(n).
- **Input Preservation**: The caller's list stays unchanged.
- **Empty Input**: Returns 0 as an extension beyond LeetCode's nonempty-input constraint.

My original implementation was correct and already documented these bounds. The improvement is algorithmic: reduce the work needed to find a useful predecessor.

---

### 🚀 What's Next?

Could we keep just the **smallest possible ending value for each subsequence length**?

A smaller tail leaves at least as much room for future extensions. Part 2 uses that observation with binary search to reach **O(n log n) time**.

There's an important catch: the resulting tail array isn't necessarily an actual subsequence!

#LearningInPublic #Python #Algorithms #DataStructures #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
