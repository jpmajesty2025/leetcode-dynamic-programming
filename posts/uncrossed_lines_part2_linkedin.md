# Uncrossed Lines: One Row & Sparse Matches (Part 2 of 2) ⚡

Part 1 reduced uncrossed lines to longest common subsequence. Two alternatives preserve the index-order constraint with different state representations.

---

### 💡 Keep One Row and an Old Diagonal

Before updating column j:
- **`dp[j]`** is the old value above.
- **`dp[j - 1]`** is the updated value to the left.
- **`diagonal`** is the old upper-left value.

Save the old `dp[j]` before overwriting it. On equal values, write `diagonal + 1`; otherwise take the maximum of above and left. Carry the saved old value into the next diagonal.

Process columns left to right and reset the diagonal for each row.

Using the shorter array for columns gives **O(mn) time and O(min(m, n)) space**, consistent with the repository's string LCS implementation.

---

### 🧩 Process Only Equal-Value Pairs

The sparse alternative indexes each value's positions in the second array.

Process the first array in order. For each value, visit its matching second-array positions and maintain tails of strictly increasing position sequences using binary search.

An increasing position sequence corresponds to ordered, noncrossing matches.

---

### ⚠️ Visit Each Position Group Backward

For first array `[1]` and second array `[1, 1]`, the matching positions are 0 and 1.

Visiting them in increasing order could create a false length-two sequence using the same first-array occurrence twice.

Process the group as **1, 0** instead. No strictly increasing subsequence can take two positions from this decreasing group.

Use `bisect_left`, not `bisect_right`, so the same second-array position cannot extend a sequence twice either.

---

### 📊 Choose by Match Density

Let r be the number of equal-value index pairs and k the shorter length.

- **Rolling DP**: O(mn) time, O(k) auxiliary space.
- **Sparse Matches**: Expected O(m + n + r log(k + 1)) time, O(k) auxiliary space.

The sparse version streams position groups instead of building a list of all r matches. Dictionary lookups use expected constant time.

For dense duplicates, r can equal mn and the extra binary searches can make sparse matching worse. The rolling version is my default for the standard constraints; sparse matching is useful when relatively few pairs match.

---

### 🧪 Independent Verification

The oracle enumerates subsequences of both arrays, intersects their sets, and takes the longest length. It uses neither implementation recurrence.

Coverage includes:
- **Exhaustive Inputs**: All 961 pairs of binary arrays of lengths 0 through 4.
- **Hypothesis Properties**: Symmetry, identity, reversal of both arrays, and appending a common value.
- **Regressions**: Reused endpoints, crossing pairs, duplicates, and disjoint values.
- **Scale Checks**: Dense 500-element cases, unequal lengths, and large sparse matches.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LCS #SoftwareTesting #Hypothesis #LeetCode
