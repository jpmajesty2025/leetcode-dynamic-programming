# Longest Common Subsequence: One Row & a Saved Diagonal (Part 2 of 2) ⚡

In Part 1, the full prefix table computed LCS lengths in O(mn) time and O(mn) auxiliary space.

For the length-only interface, **one row and a saved diagonal** preserve every dependency.

---

### 💡 Three Values, Two Different Rows

Before updating column j:
- **`dp[j]`** is the previous row's value above.
- **`dp[j - 1]`** is the current row's value to the left.
- **`diagonal`** is the previous row's value at column j - 1.

These meanings depend on processing columns **left to right**.

1️⃣ Save the old `dp[j]` as `above`.
2️⃣ On a match, write `diagonal + 1`; otherwise write `max(above, dp[j - 1])`.
3️⃣ Set `diagonal = above` for the next column.

Reset the diagonal to zero at the start of every row, matching the empty-prefix boundary.

---

### ⚠️ Don't Reuse the Updated Cell as the Diagonal

The next diagonal must come from the **previous row**, not the value just computed.

For `"a"` and `"aaaa"`, incorrectly carrying the new value into the diagonal can reuse the same character and inflate the result.

The correct answer remains **1**.

---

### 🚀 Put the Shorter String in Columns

LCS is symmetric, so swapping the local string references doesn't change the answer.

Using the shorter string for columns gives:
- **Time**: O(mn).
- **Auxiliary Space**: **O(min(m, n))** for nonempty inputs.
- **Empty Inputs**: Return 0 in O(1) time and space.

The bounds assume constant-cost integer operations. No string copies are needed for the swap, and no external state is modified.

This reduces storage, not the asymptotic running time. Specialized LCS algorithms can exploit sparse matches or bit-parallel operations; this implementation stays with the general prefix recurrence.

---

### 🧪 Independent Verification

**49 LCS tests passed; 432 passed across the complete suite.**

- **Exhaustive Inputs**: All 961 pairs of binary strings of lengths 0 through 4, per implementation.
- **Independent Oracle**: Enumerate subsequences of both strings, intersect their sets, and take the maximum length.
- **Regressions**: Empty strings, repeated characters, disjoint alphabets, Unicode, and noncontiguous matches.
- **Hypothesis Properties**: Symmetry, identity, length bounds, reversal of both inputs, and appending a shared character.
- **Boundaries**: 1,000-character cases for both versions; 100,000-versus-1-character cases for the compressed version.

For returning only the length, **one-row DP is my default**. The separate full-table version keeps intermediate states visible and can support a later traceback implementation.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Strings #SoftwareTesting #Hypothesis #LeetCode
