# Longest Common Subsequence: Prefix States & Matching Characters (Part 1 of 2) 🧩

**The Problem**:
Given two strings, return the **length of their longest common subsequence**.

Characters may be skipped, but their relative order must stay the same.

For `"abcde"` and `"ace"`, the answer is **3**: `"ace"` appears in both, even though it isn't contiguous in the first string.

---

### 💡 Define the Prefix State

**`dp[i][j]` is the LCS length of `text1[:i]` and `text2[:j]`.**

An empty prefix shares only the empty subsequence with any string, so the first row and column are zero.

Then compare the final characters of the two prefixes.

1️⃣ **Matching Characters**:
An optimal common subsequence can use this match. Extend the optimum for the two shorter prefixes:
`dp[i][j] = dp[i - 1][j - 1] + 1`

2️⃣ **Different Characters**:
A common subsequence must omit at least one of these final characters. Keep the better result:
`dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`

Processing rows and columns in increasing order makes every dependency available before use.

---

### ⚠️ Two Common Confusions

**Subsequence vs. Substring**:
A substring must be contiguous. A subsequence may have gaps. Resetting a mismatch cell to zero would belong to the longest-common-substring recurrence, not this one.

**Repeated Characters**:
For `"a"` and `"aaaa"`, the answer is **1**. A character position can only be used once in a subsequence.

---

### 📊 Complexity & Quality

For nonempty strings of lengths m and n:
- **Time**: O(mn).
- **Auxiliary Space**: O(mn).

The original full-table implementation was correct, readable, and used independently allocated rows, avoiding shared-row aliasing.

The saved table alternative adds explicit state documentation, an empty-input early return, and a LeetCode wrapper. It still returns only the length; recovering a subsequence would need an additional traceback.

---

### 🚀 What's Next?

Each cell reads only **above, left, and the previous diagonal**. We can preserve those dependencies without retaining the full table.

Part 2 compresses the state into one row, uses the shorter string for columns, and checks update-order mistakes against independent subsequence enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Strings #LeetCode #CodingInterview #SoftwareEngineering
