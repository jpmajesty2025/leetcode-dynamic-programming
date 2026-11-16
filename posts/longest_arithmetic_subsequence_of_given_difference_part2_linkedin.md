# Longest Arithmetic Subsequence: State Compression & Verification (Part 2 of 2) ⚡

Part 1 used value-keyed DP. Two alternatives clarify its state and lookup trade-offs.

---

### 💡 Start with Index-Based DP

**`lengths[i]` is the longest valid subsequence ending at index i.**

Initialize every entry to one. For each earlier index j satisfying:
`arr[i] - arr[j] == difference`

consider:
`lengths[i] = max(lengths[i], lengths[j] + 1)`

This takes **O(n²) time and O(n) space**. It's useful as a readable reference, but unsuitable for the problem's largest inputs.

The original compresses these endpoint states because future elements care about the ending value, not which earlier index supplied it.

---

### 🧩 Coordinate Compression Without Reordering the Subsequence

The coordinate alternative:
1️⃣ Sorts a copy of the values and removes adjacent duplicates.
2️⃣ Allocates one DP entry per distinct coordinate.
3️⃣ Processes the original array in its original order.
4️⃣ Uses binary search to locate each value and its predecessor.

Sorting the coordinate lookup is safe. Sorting the sequence being processed would change the problem.

A coordinate can exist in the lookup before appearing in the processed prefix. Its DP value remains zero until that occurrence, so future positions aren't used early.

---

### ⚠️ Preserve Read-Before-Write for Difference Zero

When difference is zero, current and predecessor coordinates coincide.

Read the previous length first, add one, then write the new length. This counts each occurrence exactly once.

The dictionary update follows the same rule.

---

### 📊 Complexity & Default Choice

Under constant-cost comparison and arithmetic:
- **Original Dictionary**: Expected O(n) time, O(u) state.
- **Index DP**: O(n²) time, O(n) state.
- **Sorted Coordinates**: O(n log(n + 1)) worst-case time, O(n) peak storage.

The coordinate version's sorting copy matters: its peak storage isn't merely O(u), even when many input values repeat.

It avoids hash-collision dependence, but pays for sorting and binary searches. The original remains my default for ordinary integer inputs.

Large Python integers also make comparison, hashing, and arithmetic depend on bit length.

---

### 🧪 Independent Verification

The oracle enumerates index subsets, retains those with the required adjacent differences, and takes the longest length. It uses neither DP recurrence.

Coverage includes:
- **Exhaustive Inputs**: All lists of lengths 0 through 5 over `{-1, 0, 1}`, with differences -2 through 2.
- **Hypothesis Properties**: Translation, positive scaling, negation, and reversal with a negated difference.
- **Regressions**: Zero difference, repeated endpoints, negative differences, skipped positions, and original-order traps.
- **Scale Checks**: 100,000-element chains, repeated values, and reverse-direction cases for the efficient versions.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
