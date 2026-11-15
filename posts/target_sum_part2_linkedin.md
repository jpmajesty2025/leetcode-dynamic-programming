# Target Sum: Smaller Subsets & Sparse Signed Sums (Part 2 of 2) ⚡

Part 1 transformed sign assignments into subset counting and fixed a missing negative-target range check.

Two alternatives offer different storage trade-offs.

---

### 💡 Count the Smaller Sign Group

Flipping every sign maps target t expressions bijectively to target -t expressions.

After checking magnitude and parity, count subsets totaling:
**`q = (S - abs(target)) // 2`**

This uses the smaller of the two sign-group sums. Complementing a subset preserves the number of choices.

For twenty ones and target 20:
- The original positive-group formulation allocates 21 entries.
- The smaller-group formulation needs **one entry**.

Zeros still double the counts, even when q is zero.

---

### 🧩 Track Reachable Signed Sums Directly

The sparse alternative starts with:
**`ways = {0: 1}`**

For every number x, build a fresh map. A sum s with count c contributes:
1️⃣ c ways to **s + x**.
2️⃣ c ways to **s - x**.

Accumulate both contributions even if x is zero and the destination sums coincide.

Reading only the old map prevents reusing the current index. Unlike the subset version, this formulation also supports negative input values.

---

### ⚠️ Sparse Doesn't Always Mean Small

A dictionary stores only reachable sums, which helps when magnitudes are large but the number of reachable states is small.

It also adds hashing and object overhead. Some inputs create exponentially many distinct sums, so sparse DP isn't universally faster or smaller.

For the standard bounded-sum problem, **the smaller-subset DP is my default**. The sparse version is useful for a different state-density profile.

---

### 📊 Complexity & Input Policy

Under constant-cost arithmetic and expected dictionary operations:
- **Smaller Subset**: O(n(q + 1)) time, O(q + 1) stored integers.
- **Sparse Map**: Work proportional to the total states processed; storage proportional to the largest frontier.

Both preserve nums. The subset alternative rejects negative elements; the sparse alternative handles signed integers directly.

An empty list has **one assignment to zero**, the empty expression, and none to any other target.

Counts can reach 2^n, so integer bit sizes also matter.

---

### 🧪 Independent Verification

The oracle enumerates all sign vectors, evaluates each expression, and counts matches. It uses neither DP formulation.

Coverage includes:
- **Exhaustive Inputs**: Lists of length 0 through 4 over `{0, 1, 2}`, with feasible and out-of-range targets.
- **Hypothesis Properties**: Target symmetry, order invariance, scaling, and appending zero doubles the count.
- **Count Conservation**: Summing counts across all targets gives 2^n.
- **Regressions**: Negative target overflow, parity mismatch, zeros, duplicate indices, large counts, and input preservation.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Knapsack #SoftwareTesting #Hypothesis #LeetCode
