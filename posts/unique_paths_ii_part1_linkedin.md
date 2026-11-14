# Unique Paths II: Obstacles & Reachability (Part 1 of 2) 🧩

**The Problem**:
Count paths from the top-left to the bottom-right of a binary grid. Move only **right or down**, and never enter an obstacle.

A 0 marks open space; a 1 marks an obstacle.

For `[[0, 0, 0], [0, 1, 0], [0, 0, 0]]`, the answer is **2**.

---

### 💡 Define the Cell State

**`dp[row][column]` is the number of legal paths reaching that cell.**

For an open interior cell, the final move comes from:
1️⃣ **Above**: `dp[row - 1][column]`.
2️⃣ **The Left**: `dp[row][column - 1]`.

These groups are disjoint, so add their counts.

For a blocked cell, the count is **zero**, regardless of its predecessors.

---

### ⚠️ Boundaries Stop at the First Obstacle

In obstacle-free Unique Paths, every first-row and first-column cell has one path.

Here, an obstacle breaks that propagation.

For the single row `[0, 1, 0]`, reachable counts are:
**`[1, 0, 0]`**

The final open cell is unreachable. Initializing the whole boundary to ones would create a path through the obstacle.

The original correctly copies the previous boundary count only when the current cell is open.

---

### 🧩 Start and Destination Matter

- **Open 1 × 1 Grid**: One path, requiring no moves.
- **Blocked Start**: Zero paths.
- **Blocked Destination**: Zero paths.
- **Open but Isolated Destination**: Still zero paths.

The original returns early for a blocked start. Its zero-initialized table also handles a blocked destination correctly.

It preserves the grid and allocates independent DP rows.

---

### 🔍 Why the Binomial Formula Isn't Enough

For an obstacle-free m × n grid, we can count arrangements of right and down moves.

Obstacles make some arrangements invalid. Their locations matter, not just how many blocked cells there are.

For a 3 × 3 grid, blocking the center leaves **2** paths; blocking the top-middle cell leaves **3**.

The local reachability recurrence handles both cases.

---

### 📊 Complexity & Quality

- **Time**: O(mn), worst-case optimal for an explicit grid.
- **Auxiliary Space**: O(mn).
- **Mutation**: The input isn't changed.

The original is correct for nonempty rectangular binary grids. It handles `[]`, but `[[]]` raises an indexing error outside LeetCode's contract.

The saved alternatives handle empty rows and explicitly reject ragged grids.

---

### 🚀 What's Next?

Part 2 compresses the counts into **O(min(m, n)) storage**, explains why obstacles must clear stale state, and compares an explicitly mutating alternative.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
