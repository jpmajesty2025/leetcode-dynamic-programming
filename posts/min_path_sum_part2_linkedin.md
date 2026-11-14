# Minimum Path Sum: Rolling State & Mutation Trade-Offs (Part 2 of 2) ⚡

In Part 1, a full table stored the cheapest cost of reaching every grid cell.

For a sum-only answer, **only the active predecessor costs need to remain in memory**.

---

### 💡 Compress the Table into One Buffer

Before updating position j:
- **`dp[j]`** is the previous outer iteration's cost.
- **`dp[j - 1]`** is the current iteration's already-updated predecessor.

For an interior cell:
`dp[j] = min(dp[j], dp[j - 1]) + value`

Process the buffer **left to right**. Boundary cells have only one predecessor and need separate handling.

The start contributes its own value exactly once.

---

### 🚀 Store the Shorter Dimension

Use a buffer of length **min(m, n)**.

For a wide grid, the saved implementation traverses columns outside and rows inside, reading `grid[j][i]`. For a tall grid, it uses ordinary row-major traversal.

This is a logical transpose: **no transposed grid is allocated**.

Transposing a weighted grid preserves the optimum because each path maps to one with the same cell values and exchanged right/down moves.

---

### ⚠️ O(1) Extra Space Changes the Contract

The separate in-place alternative overwrites every cell with its best prefix cost.

For `[[1, 2], [3, 4]]`, the stored result becomes:
`[[1, 3], [4, 7]]`

That saves auxiliary storage, but callers lose the original weights. Calling it again processes the modified costs, not the original problem.

Rows must also be independently stored. An aliased construction such as `[row] * m` doesn't meet the in-place version's contract.

Copying all rows first preserves the original but costs **O(mn) extra storage**.

---

### 📊 Complexity & Default Choice

Under constant-cost integer arithmetic:
- **Original Table**: O(mn) time, O(mn) auxiliary space.
- **Rolling DP**: O(mn) time, O(min(m, n)) auxiliary space.
- **In-Place DP**: O(mn) time, O(1) auxiliary space.

Python integers remain exact; arithmetic and storage costs grow with integer size.

The nonmutating rolling version is my default. Use in-place DP when overwriting the grid is explicitly acceptable.

---

### 🧪 Independent Verification

The oracle enumerates legal move sequences, sums every visited cell, and chooses the smallest total.

Coverage includes:
- **Exhaustive Inputs**: Every binary-valued grid with 1 through 3 rows and columns.
- **Hypothesis Properties**: Transpose invariance, 180-degree rotation, nonnegative scaling, and cell-cost monotonicity.
- **Fixed Path Length**: Adding c to every cell shifts the optimum by `(m + n - 1) × c`.
- **Contracts**: Nonmutation, exact in-place updates, ragged-grid rejection, and aliased rows for nonmutating versions.
- **Boundaries**: Empty grids, single rows/columns, negative values, and large sums.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
