# Nth Tribonacci Number: Exponentiate the Transition (Part 2 of 2) ⚡

Part 1 advanced a three-value window one term at a time.

For large indices, we can apply many recurrence steps together using **binary matrix exponentiation**.

---

### 💡 Package the State into a Vector

Use the column vector:
**`[T[i], T[i - 1], T[i - 2]]`**

One step multiplies it by:
`M = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]`

The first row adds the three terms. The other rows shift the old values down.

For n >= 2:
**`[T[n], T[n - 1], T[n - 2]] = M^(n - 2) × [1, 1, 0]`**

That exponent is n - 2 because the starting vector already ends at T2.

---

### 🧩 Use the Exponent's Binary Digits

Start the accumulated matrix as the **identity**, representing zero transitions.

For each exponent bit:
1️⃣ If the bit is set, multiply the accumulator by the current power.
2️⃣ Shift the exponent right.
3️⃣ If bits remain, square the current power.

Successive powers represent 1, 2, 4, 8, ... recurrence steps.

Only O(log(n + 1)) iterations are needed, and each matrix is always 3 × 3.

---

### ⚠️ Keep the Computation Exact

The saved implementation uses integer multiplication and addition throughout.

A floating-point formula involving the recurrence's characteristic roots can accumulate rounding error. Exact matrix arithmetic avoids that risk.

Base cases still matter: handle n = 0, 1, and 2 before constructing an exponent that might be negative.

---

### 📊 Compare the Trade-Offs

Under a constant-cost arithmetic model:
- **Original Rolling Loop**: O(n + 1) operations, O(1) integer variables.
- **Saved DP Table**: O(n + 1) operations, O(n + 1) stored integers.
- **Matrix Version**: O(log(n + 1)) operations, a constant number of integer entries.

The table exposes intermediate terms. Matrix exponentiation supports much larger indices with fewer arithmetic operations.

These aren't bit-time bounds. Tn has Θ(n) bits, and matrix operations multiply increasingly large integers. Returning the exact answer alone requires linear-sized output.

For n <= 37, the rolling loop remains the clearest choice. Fewer arithmetic operations don't guarantee a faster implementation at small inputs.

---

### 🧪 Independent Verification

For n >= 1, Tn counts ordered compositions of **n - 1** using parts 1, 2, and 3.

The oracle enumerates multiplicities of each part and counts their distinct arrangements with binomial coefficients. It uses neither the rolling recurrence nor matrix powers.

Coverage includes:
- **Exhaustive Indices**: 0 through 100, per implementation.
- **Hypothesis Properties**: The recurrence, nonnegativity, and growth.
- **Regressions**: Base cases, exponent-bit boundaries, negatives, and repeated calls.
- **Large Exact Values**: Agreement at n = 1,000 and n = 10,000.

#LearningInPublic #Python #Algorithms #DynamicProgramming #MatrixExponentiation #SoftwareTesting #Hypothesis #LeetCode
