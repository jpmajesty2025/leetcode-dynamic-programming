# Minimum Falling Path Sum II: Exclude One Column (Part 1 of 2) 🧩

**The Problem**:
Choose exactly one value from every row, minimizing the sum. **Adjacent rows cannot use the same column.**

Unlike the first falling-path problem, a move can jump any distance horizontally. Only staying in the same column is forbidden.

For `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, the answer is **13**, along values 1 → 5 → 7.

---

### 💡 Define the Endpoint State

**`dp[row][column]` is the minimum valid prefix sum ending at that cell.**

Every first-row column is a valid start, so copy the first row.

For a later cell in column j:
`dp[row][j] = grid[row][j] + min(previous[k] for k != j)`

Return the minimum across the final row. Both the starting and ending columns are unrestricted.

Negative values work naturally because every move advances one row.

---

### ⚠️ The Original Repeats the Same Search

The original scans all previous columns for every current cell.

For n × n input:
- **Time**: O(n³).
- **Auxiliary Space**: O(n²).

The recurrence is correct, but its searches overlap heavily. Every cell asks for the cheapest previous endpoint after excluding just one column.

---

### 🚀 Keep the Two Cheapest Entries

For the previous row, record:
1️⃣ **First**: The cheapest cost and its column.
2️⃣ **Second**: The cheapest cost at a different column.

For a current column j:
- If j differs from the first minimum's column, use **first**.
- Otherwise, use **second**.

Finding these entries once per row makes every cell transition constant time.

The saved rolling version takes **O(n²) time and O(n) auxiliary space**.

---

### ⚠️ Second Entry Doesn't Mean Second Distinct Value

For previous costs `[1, 1, 9]`, the two cheapest entries are **1 and 1**, at different columns.

Excluding one minimum's column still leaves the other minimum available.

For `[[0, 0], [0, 100]]`, the correct answer is **0**. Discarding equal-valued minima would lose a valid predecessor.

The exclusion is about **column identity**, not distinct numeric values.

---

### 🔍 Quality Improvements

The original correctly copies the first row and preserves the input.

Suggested improvements include documenting the square-grid contract, using descriptive names, and replacing repeated predecessor scans with the two-minimum summary.

The saved alternatives also support rectangular grids and explicitly reject multirow single-column inputs, where no legal path exists.

---

### 🚀 What's Next?

Part 2 streams the two minima directly, reducing auxiliary storage to **O(1) variables without mutating the grid**, then verifies the result with independent path enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
