# Unique Paths: Grid States & One-Row DP (Part 1 of 2) 🧩

**The Problem**:
Count paths from the top-left to the bottom-right of an m × n grid, moving only **right or down**.

For `m = 3` and `n = 7`, the answer is **28**.

---

### 💡 Define the Cell State

**`dp[row][column]` is the number of paths reaching that cell.**

Every cell in the first row has exactly one path: keep moving right. Every cell in the first column also has one path: keep moving down.

For an interior cell, the final move must come from:
1️⃣ **Above**: `dp[row - 1][column]`.
2️⃣ **The Left**: `dp[row][column - 1]`.

These groups are disjoint, so add them:
`dp[row][column] = dp[row - 1][column] + dp[row][column - 1]`

A 1 × 1 grid has **one path**, the empty sequence of moves.

---

### 🧩 Keep Only One Row

Each update needs only the value above and the current row's left neighbor.

Initialize a row of ones. Before updating column j:
- **`dp[j]`** still belongs to the previous row.
- **`dp[j - 1]`** already belongs to the current row.

The transition becomes:
`dp[j] += dp[j - 1]`

**Process columns left to right** to preserve those meanings.

---

### ⚠️ Loop Direction Changes the Dependencies

For a 3 × 3 grid, the row starts as `[1, 1, 1]`.

The next two rows become:
- `[1, 2, 3]`.
- `[1, 3, 6]`.

A right-to-left update would read an old left neighbor, producing the wrong result.

The full-table original also correctly allocates independent rows with a comprehension, avoiding shared-row aliasing.

---

### 🚀 Use the Shorter Dimension

Swapping the grid dimensions preserves the path count: exchange right and down in every path.

Use **min(m, n)** columns for the rolling row.

For grids with both dimensions greater than one:
- **Time**: O(mn) additions.
- **Auxiliary Storage**: O(min(m, n)) integers, versus O(mn) in the original.

The saved rolling version returns 1 immediately for a single row or column and raises `ValueError` for nonpositive dimensions.

These operation bounds treat integer arithmetic as constant cost. Python keeps large counts exact, but their storage and arithmetic costs grow.

---

### 🚀 What's Next?

Every path contains a fixed number of right and down moves. Part 2 counts their arrangements directly with a **binomial coefficient**, avoiding a visit to every grid cell.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
