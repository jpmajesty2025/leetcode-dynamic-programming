# Climbing Stairs: Last-Move Reasoning & Rolling DP (Part 1 of 2) 🪜

**The Problem**:
You can climb either one or two steps at a time. How many distinct ordered routes reach stair n?

For n = 3, the answer is **3**:
- 1 + 1 + 1
- 1 + 2
- 2 + 1

Order matters: the last two routes are different.

---

### 🧩 Classify Routes by Their Last Move

Every route to stair n ends with:
1. **One step** from stair n - 1.
2. **Two steps** from stair n - 2.

These groups are disjoint and cover every route, so:
`ways(n) = ways(n - 1) + ways(n - 2)`

This is the Fibonacci recurrence, shifted by one index: **ways(n) = F(n + 1)**, with F(0) = 0 and F(1) = 1.

---

### ⚠️ Base Cases Define the Contract

1️⃣ **Zero Stairs**:
There is **one empty route**, so ways(0) = 1. Together with ways(1) = 1, this gives ways(2) = 2 naturally.

2️⃣ **Negative Stairs**:
The saved implementations raise `ValueError` for negative n.

LeetCode specifies 1 <= n <= 45. My original solution was correct throughout that range; supporting zero and rejecting negatives are explicit changes outside the original problem contract.

---

### 💡 Keep Only Two Counts

The original DP table stores every earlier answer, but the recurrence reads only two of them.

Start with the counts for stairs 0 and 1. Each iteration adds the two previous counts and shifts the pair forward.

Simultaneous assignment ensures both new values use the old state. The public `climb_stairs(n)` interface stays the same, with a LeetCode wrapper added separately.

---

### 📊 Complexity

- **Table**: O(n) additions, O(n) integer entries.
- **Rolling DP**: O(n) additions, **O(1) integer variables**.

For the problem's small input range, these are commonly described as O(n) time and O(1) rolling space under constant-cost arithmetic.

For unrestricted n, the answer has O(n) bits. Rolling DP uses O(n) auxiliary bits and O(n²) bit-time with linear-time integer addition. A constant number of Python integers doesn't mean constant bit space!

---

### 🚀 What's Next?

Part 2 uses **exact-integer Fibonacci fast doubling** to reduce the arithmetic-operation count to O(log(n + 1)), then checks all implementations against independent combinatorial counting.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
