# Nth Tribonacci Number: Three Values Are Enough (Part 1 of 2) 🧩

**The Problem**:
Return Tn, where **T0 = 0, T1 = 1, T2 = 1**, and every later term is the sum of its three predecessors.

The sequence begins:
`0, 1, 1, 2, 4, 7, 13, 24`

For `n = 4`, the answer is **4**.

---

### 💡 Define the Rolling State

A full DP table could store every term:
`T[i] = T[i - 3] + T[i - 2] + T[i - 1]`

But the next term only needs the last three values.

Before calculating term i, keep:
- **`t0 = T[i - 3]`**.
- **`t1 = T[i - 2]`**.
- **`t2 = T[i - 1]`**.

Initialize them to **0, 1, 1** before processing i = 3.

---

### 🧩 Advance the Window

First calculate:
`t_next = t0 + t1 + t2`

Then shift:
`t0, t1, t2 = t1, t2, t_next`

The new window ends at Ti, ready for the next iteration.

After processing through n, **t2 is Tn**. The original handles indices 0, 1, and 2 separately, so the loop starts exactly where the recurrence becomes applicable.

---

### ⚠️ Preserve the Old Values

Python's simultaneous assignment evaluates the right-hand side before assigning the new values.

Overwriting t0, then t1, and only afterward calculating the sum would mix different sequence positions.

The original avoids that problem by calculating the new term first and then shifting the window.

---

### 📊 Complexity & Quality

Under constant-cost integer arithmetic:
- **Time**: O(n + 1).
- **Auxiliary Storage**: O(1) integer variables.

The original is correct for nonnegative integer indices and retains no state between calls.

For the usual LeetCode range, **0 through 37**, this is my default: a short loop with a direct correctness argument.

Negative indices currently return 1 because the loop is skipped. That's outside the problem contract; the saved alternatives explicitly raise `ValueError`.

Suggested improvements are a documented invariant, an explicit input policy, and a LeetCode wrapper.

---

### 🔍 Constant Variables Aren't Constant Bits

For unrestricted n, Tribonacci values have **Θ(n) bits**.

The loop still keeps only a few integers, but their size grows. With ordinary big-integer addition, the iterative computation takes Θ(n²) bit work and Θ(n) live integer bits.

---

### 🚀 What's Next?

Part 2 expresses one recurrence step as a matrix and uses binary exponentiation to reduce the number of arithmetic operations for large indices.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
