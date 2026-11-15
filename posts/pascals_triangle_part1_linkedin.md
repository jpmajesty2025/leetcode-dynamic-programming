# Pascal's Triangle: Adjacent Sums & Output Size (Part 1 of 2) 🧩

**The Problem**:
Return the first r rows of Pascal's triangle. Every row starts and ends with **1**; each interior entry is the sum of its two parents.

For `r = 5`, the final row is:
**`[1, 4, 6, 4, 1]`**

The returned triangle includes all five rows, starting with `[1]`.

---

### 💡 Define the Row State

**`triangle[i][j]` is entry j of zero-indexed row i.**

Start with `[[1]]`.

For each later row:
1️⃣ Start a fresh list with 1.
2️⃣ Add each pair of adjacent entries from the preceding row.
3️⃣ Append the final 1 and store the completed row.

The interior recurrence is:
`triangle[i][j] = triangle[i - 1][j - 1] + triangle[i - 1][j]`

Only the preceding row is needed to construct the next, but the requested output retains every row.

---

### ⚠️ Small Rows Need Different Boundaries

The first row is **`[1]`**, not `[1, 1]`.

The original initializes it separately. For the second row, the interior loop is empty, leaving exactly the two boundary ones.

It also returns `[]` for zero or negative row counts, an explicit extension beyond LeetCode's positive-input contract.

---

### 🧩 Fresh Rows Prevent Aliasing

Each row must be a different mutable list.

Reusing and appending the same working list would make multiple stored rows refer to one object. Later updates could corrupt earlier rows.

The original creates a fresh row on every iteration and doesn't modify previously completed rows. Separate calls also return independent results.

---

### 📊 Complexity Depends on What We Return

The first r rows contain:
**`r × (r + 1) / 2` entries**

Under constant-cost integer arithmetic:
- **Time**: Θ(r²).
- **Returned Storage**: Θ(r²) entries.
- **Auxiliary State Beyond Output**: O(1) variables.

The current row becomes part of the returned triangle, so it isn't an extra retained table.

The original is already asymptotically optimal for explicitly returning every entry. A rolling-row explanation alone doesn't make this full-output interface O(r) space.

---

### 🔍 Quality & Large Integers

Suggested improvements are a documented row invariant, output-versus-auxiliary space accounting, clearer index names, and a LeetCode wrapper.

Python keeps coefficients exact. For unbounded r, central entries grow to Θ(r) bits, so constant-cost arithmetic is only a simplifying model.

---

### 🚀 What's Next?

Part 2 builds rows with exact binomial ratios and introduces a streaming iterator. Streaming saves live storage only when the caller doesn't retain the whole triangle.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
