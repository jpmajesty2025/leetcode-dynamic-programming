# Minimum Falling Path Sum: Three Predecessors (Part 1 of 2) 🧩

**The Problem**:
Start anywhere in the first row. Move to the next row, either straight down or one column diagonally left/right. Return the **minimum total sum**.

For `[[2, 1, 3], [6, 5, 4], [7, 8, 9]]`, the answer is **13**, for example along values 1 → 5 → 7.

---

### 💡 Define the Cell State

**`dp[row][column]` is the minimum sum of a falling path ending at that cell.**

Initialize the first DP row with the matrix's first row. Every starting column is allowed, and its value contributes to the sum.

For each later cell, consider valid predecessors:
1️⃣ **Above Left**: Column j - 1.
2️⃣ **Directly Above**: Column j.
3️⃣ **Above Right**: Column j + 1.

Add the current cell's value to the cheapest predecessor.

---

### ⚠️ Edges Have Fewer Choices

At the left edge, there is no above-left predecessor. At the right edge, there is no above-right predecessor.

The original checks those bounds explicitly.

That matters in Python: an unchecked index of -1 would wrap to the last column, creating an illegal edge-to-edge jump.

There's also no zero-cost predecessor outside the matrix. Inventing one could undercount a positive path.

---

### 🧩 The Answer Can End Anywhere

Return **the minimum of the final DP row**, not just its last cell.

For `[[-19, 57], [-40, -5]]`, the answer is **-59**, ending in the first column.

A single-cell matrix returns its own value. Negative values need no special algorithm: each move advances a row, so cycles are impossible.

---

### 🚫 Row Minima Aren't Always Connected

For `[[0, 100, 100], [100, 100, 0], [100, 100, 0]]`, summing row minima gives zero.

But moving from column 0 to column 2 in one step is illegal. The correct minimum is **100**.

DP preserves the column compatibility that independent row choices lose.

---

### 📊 Complexity & Quality

For an n × n matrix:
- **Time**: O(n²), worst-case optimal.
- **Auxiliary Space**: O(n²).
- **Mutation**: The original preserves the input.

The original correctly copies the first row and allocates independent DP rows. Its main improvements are state documentation and reducing unnecessary storage.

---

### 🚀 What's Next?

Part 2 keeps only the preceding row, explains why a naive one-buffer overwrite is unsafe, and compares an explicitly mutating O(1)-auxiliary-space alternative.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
