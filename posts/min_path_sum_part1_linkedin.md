# Minimum Path Sum: Weighted Grid States (Part 1 of 2) 🧩

**The Problem**:
Find the minimum sum from the top-left to the bottom-right of a grid, moving only **right or down**. Include both endpoint values.

For `[[1, 3, 1], [1, 5, 1], [4, 2, 1]]`, the answer is **7**, following values 1 → 3 → 1 → 1 → 1.

---

### 💡 Define the Cell State

**`dp[row][column]` is the minimum total cost of reaching that cell.**

Every path to an interior cell ends with a move from:
1️⃣ **Above**: `dp[row - 1][column]`.
2️⃣ **The Left**: `dp[row][column - 1]`.

Choose the cheaper predecessor, then include the current cell:
`dp[row][column] = min(above, left) + grid[row][column]`

The original implementation computes these dependencies in row-major order.

---

### ⚠️ Boundaries Are Cumulative Sums

Unlike Unique Paths, the first row and column aren't initialized to ones.

There is only one route to each boundary cell, so accumulate its costs:
- **First Row**: Add the cell to the previous column's total.
- **First Column**: Add the cell to the previous row's total.
- **Start**: Use `grid[0][0]`.

A single-cell grid returns that cell's value, not zero.

---

### 🚫 The Cheapest Next Cell Can Be Misleading

Consider:
`[[1, 1, 100], [2, 100, 100], [1, 1, 1]]`

Choosing the smaller immediate neighbor sends us right toward costly cells.

The optimum starts by moving down to 2 and totals **6**. DP compares complete prefix costs instead of committing to the cheapest next cell.

---

### 🔍 Nonnegative Values Aren't Essential to This DP

The recurrence also works with negative values.

Every move increases the row or column, so the movement graph has **no cycles**. A topological DP still works; there's no possibility of repeatedly looping through negative cells.

This doesn't justify using Dijkstra's algorithm with negative weights.

---

### 📊 Complexity & Quality

The original is correct for rectangular grids:
- **Time**: O(mn), optimal in the worst case.
- **Auxiliary Space**: O(mn).
- **Input Preservation**: The supplied grid isn't modified.
- **Empty Inputs**: Return 0.

The saved alternatives explicitly reject ragged grids. The original assumes a rectangle, which matches the problem contract.

---

### 🚀 What's Next?

Part 2 preserves the recurrence with **O(min(m, n)) auxiliary storage**, then compares an in-place version that trades input preservation for O(1) extra space.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
