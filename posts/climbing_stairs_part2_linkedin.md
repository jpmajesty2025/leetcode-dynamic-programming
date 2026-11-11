# Climbing Stairs: Exact Fibonacci Fast Doubling (Part 2 of 2) ⚡

In Part 1, rolling DP counted routes using only two consecutive answers.

Since **ways(n) = F(n + 1)**, Fibonacci identities give us another exact-integer implementation.

---

### 💡 Double the Index

Maintain a pair:
`a = F(k), b = F(k + 1)`

The doubling identities are:
- **F(2k)** = a × (2b - a)
- **F(2k + 1)** = a² + b²

These let us advance from index k to either 2k or 2k + 1.

---

### 🚀 Read the Target Index in Binary

Scan the bits of **n + 1**, from highest to lowest, starting with the pair F(0), F(1).

1️⃣ **Bit 0**:
Keep the pair F(2k), F(2k + 1).

2️⃣ **Bit 1**:
Keep F(2k + 1), F(2k + 2), where the second value is the sum of the two doubling results.

Each processed bit extends the index prefix. After the final bit, the first value is **F(n + 1)**, the required route count.

The implementation is iterative and uses integer arithmetic throughout. It needs neither recursive calls nor floating-point rounding.

---

### 📊 Choose the Complexity Model

- **DP Table**: O(n) additions, O(n) integer entries.
- **Rolling DP**: O(n) additions, O(1) integer variables.
- **Fast Doubling**: O(log(n + 1)) arithmetic operations, O(1) large-integer variables.

**Arithmetic operations aren't constant-cost for unbounded integers.** The answer has O(n) bits, and fast doubling multiplies growing integers. Its logarithmic operation count is not a logarithmic bit-time guarantee.

For LeetCode's n <= 45, rolling DP remains my default because its recurrence and state are simpler. Fast doubling is useful when exploring much larger exact results.

---

### 🧪 Independent Verification

**58 Climbing Stairs tests passed; 293 passed across the complete suite.**

The combinatorial oracle counts routes by their number k of two-step moves:
`sum(comb(n - k, k) for k in range(n // 2 + 1))`

Why? With k two-step moves, there are n - 2k one-step moves and n - k moves overall. Choose which k positions contain the two-step moves.

The tests cover:
- **Every valid input** from 1 through 45, per implementation.
- **Explicit route enumeration** for n = 0 through 15.
- **Boundary policy**: One empty route at zero; negative inputs raise `ValueError`.
- **Hypothesis checks** against combinatorial counts, plus recurrence and monotonicity properties.
- **Exact results** at n = 1,000 and repeated-call/wrapper behavior.

Fast doubling also matched rolling DP at **n = 100,000**, without converting the large result to floating point.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Fibonacci #SoftwareTesting #Hypothesis #LeetCode
