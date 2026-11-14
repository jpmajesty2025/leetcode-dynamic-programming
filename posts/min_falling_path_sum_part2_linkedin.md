# Minimum Falling Path Sum: Rolling Rows & Safe Dependencies (Part 2 of 2) ⚡

In Part 1, a full table stored the cheapest falling-path sum ending at every cell.

Only **the preceding row** is needed to compute the next one.

---

### 💡 Keep Previous and Current Rows Separate

Copy the matrix's first row into `previous`.

For each later row:
1️⃣ Create a fresh `current` buffer.
2️⃣ For each column, find the cheapest valid predecessor in `previous`.
3️⃣ Add the current cell's weight.
4️⃣ Replace `previous` only after completing the row.

Return the minimum value in the final buffer.

For n × n input, this keeps **O(n²) time and O(n) auxiliary space**.

---

### ⚠️ Neither Loop Direction Alone Protects One Buffer

Each cell may read both its previous-row left and right neighbors.

Updating a single buffer left to right destroys the old left value. Updating right to left destroys the old right value.

A one-buffer implementation is possible with saved old values, but simply reversing the loop doesn't fix the dependency problem.

The saved rolling implementation uses two buffers for clarity. Two rows still require only O(n) storage.

---

### 🧩 Don't Transpose to Shrink the Buffer

Unlike right/down grid paths, falling paths have a distinguished direction: every step advances one row.

Transposing the matrix changes which sequences are legal and can change the answer.

The alternatives support rectangular matrices with m rows and n columns:
- **Time**: O(mn).
- **Rolling Storage**: O(n), based on the column count.

They don't claim an O(min(m, n)) guarantee by swapping dimensions.

---

### ⚠️ In-Place DP Changes the Input

The separate in-place version overwrites each later row with its minimum prefix costs.

For the standard example, the matrix becomes:
`[[2, 1, 3], [7, 6, 5], [13, 13, 14]]`

All predecessors live in the completed row above, so the current row can be updated directly.

This uses **O(1) auxiliary variables**, but destroys the original weights. Rows must be independently stored; aliased rows aren't supported.

Copying the matrix first costs O(mn) additional space. Reusing an already-transformed matrix also solves a different problem.

The nonmutating rolling version is my default.

---

### 🧪 Independent Verification

The oracle enumerates complete column sequences, rejects jumps larger than one, and minimizes their total weight.

Coverage includes:
- **Exhaustive Inputs**: All binary square matrices of sizes 1 through 3.
- **Hypothesis Properties**: Horizontal reflection, row-order reversal, scaling, and cell-cost monotonicity.
- **Fixed Row Visits**: Adding c to one entire row shifts the answer by exactly c.
- **Contracts**: Nonmutation, complete in-place output, rectangular extensions, and ragged-input rejection.
- **Regressions**: Negative weights, diagonal paths, illegal wrapping, and large sums.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
