# Uncrossed Lines: Ordered Matches Become LCS (Part 1 of 2) 🧩

**The Problem**:
Connect equal values in two arrays, using each position at most once. Maximize the number of lines **without crossings**.

For `[1, 4, 2]` and `[1, 2, 4]`, the answer is **2**. Matching all three would cross the lines for 4 and 2.

---

### 💡 Translate Geometry into Index Order

List the selected positions in the first array in increasing order.

For their connecting lines not to cross, the matched positions in the second array must also increase strictly.

The connected values therefore form a **common subsequence**. Conversely, matching the positions of any common subsequence gives legal uncrossed lines.

This is exactly the longest common subsequence problem already covered in this repository, now with integer arrays.

---

### 🧩 Define the Prefix State

**`dp[i][j]` is the maximum number of lines between the first i and j elements.**

Empty prefixes have zero matches.

1️⃣ **Equal Final Values**:
`dp[i][j] = dp[i - 1][j - 1] + 1`

An optimum can use this final pair. If an optimum matches one final position elsewhere, replace that match with the final pair without losing a line. Matching both final positions to different partners would cross.

2️⃣ **Different Final Values**:
`dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`

At least one final position must be unused. Consider skipping either one.

---

### ⚠️ Duplicates Are Positions, Not Just Values

For `[1]` and `[1, 1, 1]`, the answer is **1**. The single endpoint cannot support three lines.

For `[1, 2]` and `[2, 1]`, both values occur on both sides, but the answer is also **1** because their order is reversed.

Set intersection and frequency overlap alone don't enforce these constraints. Sorting would destroy the original order.

---

### 📊 Correctness & Quality

The original full-table implementation is correct and preserves both inputs.

For nonempty lengths m and n:
- **Time**: O(mn).
- **Auxiliary Space**: O(mn).

It also returns zero for empty inputs, but still allocates a table. An explicit empty-input guard avoids that work.

Suggested improvements are a documented prefix invariant, clearer dependency comments, and a LeetCode wrapper.

---

### 🚀 What's Next?

Part 2 saves only one DP row and compares an ordered-position algorithm that can exploit sparse matching pairs.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LCS #LeetCode #CodingInterview
