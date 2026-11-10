# Longest Increasing Subsequence: Minimum Tails & Binary Search (Part 2 of 2) ⚡

In Part 1, we used O(n²) DP to find the best increasing subsequence ending at each index.

For the length-only problem, we can keep a more compact state.

---

### 💡 The Minimum-Tail Invariant

**`tails[k]` is the smallest ending value of any increasing subsequence of length k + 1 in the processed prefix.**

For equal-length subsequences, a smaller ending value leaves at least as much room for future extensions. We can discard larger tails without losing a possible future length.

The minimum tails are strictly increasing, so binary search can find where each new value belongs.

---

### 🚀 Process Each Value

Use **`bisect_left`** to find the first tail greater than or equal to the value.

1️⃣ **No Such Tail**:
The value is larger than every tail. Append it to extend the longest attainable length.

2️⃣ **An Existing Tail**:
Replace that tail with the new value. The length stays the same, while its ending value improves or stays equal.

All earlier tails are smaller than the new value, so it can extend a subsequence of the preceding length. Replacing a tail preserves the attainable lengths.

The answer is **`len(tails)`**.

---

### ⚠️ Two Details That Matter

**Duplicates**:
`bisect_left` replaces an equal tail. For `[2, 2, 2]`, the result stays 1.
Using `bisect_right` would instead compute a longest nondecreasing subsequence.

**Reconstruction**:
For `[3, 5, 6, 2, 4, 1]`, the final tails are `[1, 4, 6]`. Those values don't appear in that order in the input!

Their count correctly gives length **3**, but recovering an actual subsequence requires extra bookkeeping, such as predecessor indices.

---

### 📊 Complexity Comparison

- **Ending-at-Index DP**: O(n²) time, O(n) auxiliary space.
- **Minimum Tails**: O(n log n) time, O(n) worst-case auxiliary space.

More precisely, tails stores L values, where L is the LIS length. Both implementations leave the input unchanged. Bounds assume constant-cost comparisons.

---

### 🧪 Verification

**51 LIS tests passed; 191 passed across the complete suite.**

- **Exhaustive Inputs**: All 3,280 arrays of length 0 through 7 over `{-1, 0, 1}`, per implementation.
- **Independent Oracle**: Enumerate index subsets and directly check strict ordering.
- **Hypothesis Properties**: Append bounds, strictly increasing value transformations, and adjacent-duplicate invariance.
- **Boundaries**: Empty inputs, negatives, ties, and 2,500-element increasing/decreasing arrays.
- **Stress Cases**: The binary-search version handled 100,000-element increasing, decreasing, and equal-value arrays.

The quadratic implementation remains in a separate file for studying the recurrence. Minimum tails is my default when only the length is needed.

#LearningInPublic #Python #Algorithms #DynamicProgramming #BinarySearch #SoftwareTesting #Hypothesis #LeetCode
