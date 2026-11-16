# Longest Arithmetic Subsequence: One Predecessor Value (Part 1 of 2) 🧩

**The Problem**:
Find the longest subsequence whose adjacent values differ by a given amount. Keep the original index order; elements don't need to be contiguous.

For `[1, 5, 7, 8, 5, 3, 4, 2, 1]` and difference -2, the answer is **4**, using 7 → 5 → 3 → 1.

---

### 💡 Compress Endpoint States by Value

An index-based DP could scan all earlier positions for each element, taking O(n²) time.

With a fixed difference d, a subsequence ending at x has only one possible predecessor **value**:
**`x - d`**

Define:
**`dp[x]` is the longest valid subsequence ending with value x in the processed prefix.**

Process the array in its original order:
`dp[x] = dp.get(x - d, 0) + 1`

A missing predecessor starts a singleton. Otherwise, append the current element to the best compatible subsequence.

---

### ⚠️ Why Overwriting an Existing Entry Is Safe

Does a later occurrence of x erase a better result?

For d != 0, the best length ending at x - d cannot decrease as the processed prefix grows. The new candidate for x is therefore at least as good as its earlier candidate.

For d = 0, the lookup reads the old `dp[x]` and adds one before assignment.

So the original doesn't need an extra maximum with the old `dp[x]`.

---

### 🧩 Zero Difference Counts Repeated Values

For `[7, 7, 7, 7]` and difference 0, each occurrence extends the preceding chain.

The answer is **4**, not 1. Deduplicating the input would lose valid positions.

For a nonzero difference, repeated equal values don't extend one another, but later copies can still provide endpoints for future values.

---

### 🚫 Sorting Changes the Problem

For `[3, 2, 1]` and difference 1, the answer is **1**.

Sorting it into `[1, 2, 3]` would incorrectly create a length-three sequence that doesn't exist in the original order.

The dictionary summarizes earlier positions; it doesn't remove the subsequence ordering constraint.

---

### 📊 Complexity & Quality

For n elements and u distinct values:
- **Expected Time**: O(n).
- **Auxiliary Space**: O(u) dictionary entries.
- **Empty Input**: Returns 0.
- **Mutation**: The input isn't changed.

These bounds assume expected constant-time dictionary operations and bounded-cost integer arithmetic. Pathological collisions can degrade hash-table performance.

The original is correct and remains my default. Suggested improvements are an explicit state invariant, a typed dictionary, and a LeetCode wrapper.

---

### 🚀 What's Next?

Part 2 compares the index-based reference with a binary-search coordinate alternative and checks all versions using independent index-subset enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
