# Unique Paths II: Rolling Counts & Obstacle Resets (Part 2 of 2) ⚡

In Part 1, a full table counted legal paths to every cell.

For the final count alone, **one buffer preserves the needed predecessor counts**.

---

### 💡 Seed One Path, Then Propagate

Initialize the buffer to zeros and set `dp[0] = 1` for the open start.

During each traversal:
- **`dp[j]`** holds the previous outer iteration's count.
- **`dp[j - 1]`** holds the current iteration's already-updated predecessor.

For an open cell with j > 0:
`dp[j] += dp[j - 1]`

For an obstacle:
**`dp[j] = 0`**

Process the buffer left to right so both predecessor meanings remain correct.

---

### ⚠️ Skipping an Obstacle Leaves Stale Paths

Consider the single column `[[0], [1], [0]]`.

The buffer starts as `[1]`. At the obstacle, resetting it to zero gives:
**`[1] → [0] → [0]`**

Simply skipping the obstacle would leave the old count alive, incorrectly allowing a path through it.

The same reset removes paths from above at interior obstacles. Later open cells can still become reachable from their other predecessor.

---

### 🚀 Store the Shorter Dimension

The saved rolling implementation uses **min(m, n)** entries.

For wide grids, it reads cells in column-major order through `grid[j][i]`. For tall grids, it uses row-major order.

This is a logical transpose: no copied grid is allocated. Transposing obstacles maps each legal path to another with right and down exchanged.

---

### ⚠️ In-Place Counts Replace the Obstacle Map

The separate in-place version overwrites each cell with its reachable-path count.

For the center-blocked 3 × 3 example, the grid becomes:
`[[1, 1, 1], [1, 0, 1], [1, 1, 2]]`

The original binary map is lost. A second call would interpret some stored counts as obstacle markers, so the transformed grid must not be reused as fresh input.

Rows must be independently stored. Copying every row first preserves the original but costs O(mn) additional space.

---

### 📊 Complexity & Default Choice

Under constant-cost integer arithmetic:
- **Original Table**: O(mn) time, O(mn) auxiliary space.
- **Rolling DP**: O(mn) time, O(min(m, n)) auxiliary space.
- **In-Place DP**: O(mn) time, O(1) auxiliary variables.

Python integers keep counts exact, but their bit sizes can grow.

The nonmutating rolling implementation is my default.

---

### 🧪 Independent Verification

The oracle enumerates complete right/down paths and rejects any that visit an obstacle.

Coverage includes:
- **Exhaustive Inputs**: Every binary grid with 1 through 3 rows and columns.
- **Hypothesis Properties**: Transpose and 180-degree rotation invariance; adding obstacles can't increase the count.
- **Contracts**: Input preservation, full in-place output, empty rows, ragged-grid rejection, and keyword compatibility.
- **Regressions**: Blocked endpoints, boundary barriers, disconnected regions, and large exact counts.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
