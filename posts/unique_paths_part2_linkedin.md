# Unique Paths: Count Move Arrangements (Part 2 of 2) ⚡

In Part 1, one-row DP counted paths in O(mn) additions using O(min(m, n)) stored integers.

For an obstacle-free grid, **every path has the same multiset of moves**. We can count their arrangements directly.

---

### 💡 Choose the Down-Move Positions

An m × n grid requires:
- **m - 1 down moves**.
- **n - 1 right moves**.

There are m + n - 2 positions in the move sequence. Choose which positions contain the down moves:
**`C(m + n - 2, m - 1)`**

For a 3 × 7 grid, choose 2 positions from 8:
`C(8, 2) = 28`

Every arrangement stays inside the grid: no prefix can use more down or right moves than the complete sequence contains.

---

### 🧩 Compute the Coefficient Exactly

By symmetry, choose the less frequent move:
`r = min(m - 1, n - 1)`

Let `N = m + n - 2`. Start with `paths = 1` and repeat for i from 1 through r:
`paths = paths * (N - r + i) // i`

After iteration i, the value is **`C(N - r + i, i)`**.

That invariant guarantees exact division at every step. Multiplication must come before integer division; dividing a factor prematurely can discard information.

For everyday Python, **`math.comb(N, r)`** is the concise standard-library option. The saved implementation spells out the product to expose the reasoning.

---

### ⚠️ Avoid Floating-Point Factorials

Computing factorial ratios through floating-point division can lose precision or overflow intermediate conversions.

The integer product uses neither floats nor full factorials. Python's arbitrary-precision integers preserve the exact result, even beyond the prompt's answer cap.

---

### 📊 Complexity & Trade-Offs

The saved product uses:
- **O(min(m, n)) arithmetic operations**.
- **A constant number of integer variables**.

That is not constant bit space. The result and intermediate integers grow, and multiplication and division cost more as they grow.

For this obstacle-free problem, combinatorial counting is my default. The rolling DP is a useful foundation for variants with blocked cells, where this simple formula no longer applies.

---

### 🧪 Independent Verification

The small-grid oracle enumerates every right/down move word and counts those reaching the destination.

Coverage includes:
- **Exhaustive Grids**: All 36 dimension pairs from 1 through 6, per implementation.
- **Hypothesis Properties**: Symmetry, boundary counts, monotonicity, and the grid recurrence.
- **Reference Checks**: Python's `math.comb`.
- **Regressions**: 1 × 1, long thin grids, invalid dimensions, repeated calls, and large exact counts.

#LearningInPublic #Python #Algorithms #Combinatorics #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
