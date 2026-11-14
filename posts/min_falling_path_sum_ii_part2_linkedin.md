# Minimum Falling Path Sum II: Constant-Space Row Summaries (Part 2 of 2) ⚡

Part 1 replaced repeated column scans with two minima. We can also eliminate the full DP row.

---

### 💡 Retain Only What the Next Row Needs

Keep:
- **`first`**: The cheapest previous endpoint cost.
- **`first_column`**: A column achieving that cost.
- **`second`**: The cheapest endpoint cost at a different column.

For each current cell, calculate:
`cost = value + (second if column == first_column else first)`

Then feed that candidate into a new two-minimum summary.

All future queries exclude only one column, so the full list of endpoint costs is unnecessary.

---

### ⚠️ Don't Mix Two Different Rows

Keep the old summary fixed until every current cell is processed.

Build `next_first`, `next_second`, and `next_column` separately, then replace the old summary after finishing the row.

Updating the old minima immediately would let later cells read costs from their own row.

---

### 🧩 Preserve Ties When Updating Minima

When a candidate improves the first minimum:
1️⃣ Move the old first cost into second.
2️⃣ Record the new first cost and column.

Otherwise, compare the candidate with second.

A candidate equal to first can become second because it comes from another column. **Second is allowed to equal first.**

The implementation uses `None` for not-yet-seen candidates, keeping accumulated costs as integers.

---

### 🚀 Start Without a Special DP Row

Initialize both costs to zero and the first-column marker to -1.

No real column matches -1, so each first-row candidate is its own value. The normal invariant applies afterward.

A single-row input returns its smallest value immediately. Multiple rows with one column have no valid non-zero-shift path and are rejected.

---

### 📊 Complexity & Trade-Offs

For n × n input:
- **Original**: O(n³) time, O(n²) auxiliary space.
- **Two-Minimum Rolling DP**: O(n²) time, O(n) auxiliary space.
- **Streaming Summary**: O(n²) time, **O(1) auxiliary variables**.

The optimized time matches the worst-case cost of reading the matrix.

Both alternatives preserve the input, including aliased rows. Constant space counts variables, not bits; Python integers grow with accumulated sums.

The rolling version makes endpoint states visible. The streaming version is my default when returning only the minimum sum.

---

### 🧪 Independent Verification

The oracle enumerates complete column sequences and rejects equal columns in adjacent rows.

Coverage includes:
- **Exhaustive Inputs**: All 530 binary square matrices of sizes 1 through 3.
- **Hypothesis Properties**: Shared column permutations, row-order reversal, scaling, and cell-cost monotonicity.
- **Regressions**: Tied minima, forbidden same-column reuse, arbitrary-distance jumps, negatives, and large sums.
- **Contracts**: Nonmutation, rectangular extensions, and invalid-shape rejection.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
