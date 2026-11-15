# Pascal's Triangle: Binomial Rows & Safe Streaming (Part 2 of 2) ⚡

Part 1 used adjacent parent sums. Two alternatives change how we build or consume the triangle.

---

### 💡 Build a Row Without Its Predecessor

Entry j in zero-indexed row i is **`C(i, j)`**.

Start with coefficient 1, then calculate:
`coefficient = coefficient * (i - j + 1) // j`

For row 4, this produces:
**`1 → 4 → 6 → 4 → 1`**

Each division is exact because the result is the next binomial coefficient. Multiply before dividing; truncating an individual ratio first can lose information.

The saved binomial implementation uses integers throughout, without factorials or floating-point rounding.

---

### 📊 Same Output, Same Size Bound

Both the original and binomial versions return all r rows:
- **Arithmetic Operations**: Θ(r²).
- **Output Entries**: Θ(r²).
- **Auxiliary State Beyond Output**: O(1) variables.

The binomial formulation isn't an asymptotic speedup. It builds each row independently, using multiplication and division instead of parent additions.

For this full-output problem, the original addition-based implementation remains my default.

---

### 🚀 Stream Rows When the Consumer Can Discard Them

The separate `iter_rows(r)` interface yields one row at a time.

It needs **O(r) live integer entries internally**, rather than storing the complete triangle.

That benefit depends on consumption:
- Process and discard each row: linear live entry storage.
- Collect them with `list(...)`: quadratic output storage returns.

The saved `generate(r)` adapter materializes the iterator to preserve the original API.

---

### ⚠️ Yield Independent Snapshots

A generator can accidentally expose the list it will use to calculate the next row.

If the caller edits that list, future rows may change.

The saved iterator keeps its recurrence state private and yields a **copy**. Mutating or clearing a yielded row doesn't corrupt later output.

The copies add work but don't change the Θ(r²) total operation bound.

---

### 🔍 Integer Counts Aren't Bit Counts

Across the full triangle, exact coefficient values occupy Θ(r³) bits asymptotically. Streaming a constant number of rows needs O(r²) live value bits.

These statements distinguish growing Python integers from the simpler model that counts entries as constant-size objects.

---

### 🧪 Independent Verification

The small-input oracle enumerates subsets and counts them by cardinality, recovering each row without the parent-sum recurrence.

Coverage includes:
- **Exhaustive Small Outputs**: Row counts 0 through 10.
- **Reference Checks**: Python's `math.comb`.
- **Hypothesis Properties**: Symmetry, boundary ones, row sums of 2^i, and alternating sums.
- **Ownership**: Independent rows, independent calls, and mutation-safe yielded snapshots.
- **Boundaries**: Nonpositive counts, early stopping, and large exact coefficients.

#LearningInPublic #Python #Algorithms #Combinatorics #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
