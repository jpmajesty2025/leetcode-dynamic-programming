# Min Cost Climbing Stairs: State Semantics & Rolling DP (Part 1 of 2) 🪜

**The Problem**:
You can start at step 0 or 1. Pay a step's cost, then climb one or two steps.
Return the **minimum cost to reach the position just past the last step**.

For `[10, 15, 20]`, the answer is **15**: start at step 1, pay 15, then jump to the top.

---

### 🧩 Reaching a Step vs. Paying for It

Define **`dp[k]` as the minimum cost to reach position k, before paying that position's cost**.

This gives two free starting states:
`dp[0] = dp[1] = 0`

To reach position k:
1. Come from k - 1 and pay `cost[k - 1]`.
2. Come from k - 2 and pay `cost[k - 2]`.

Take the cheaper option:
`dp[k] = min(dp[k - 1] + cost[k - 1], dp[k - 2] + cost[k - 2])`

Every valid path reaches k through one of these predecessors, so the recurrence covers every possibility.

---

### ⚠️ Two Common Mistakes

1️⃣ **Charging for the Top**:
The top is position `len(cost)`. It has no corresponding cost entry. Return the cost of reaching it!

2️⃣ **Choosing the Cheaper Starting Step Greedily**:
For `[1, 2, 100, 1]`, starting at the cheaper step 0 gives a best total of 4. Starting at step 1 costs only **3** overall.

---

### 💡 Compressing the State

My original implementation used a full DP table. Each update reads only two earlier entries.

Before computing position k:
- **`two_back`** holds the cost to reach k - 2.
- **`one_back`** holds the cost to reach k - 1.

Compute the current minimum, then shift both states forward. The input stays unchanged.

Empty and singleton inputs also return 0 as documented extensions beyond the problem's minimum length of 2.

---

### 📊 Complexity

- **DP Table**: O(n) time, O(n) auxiliary space.
- **Rolling States**: O(n) time, **O(1) auxiliary space**.

The time bound is worst-case optimal. On an all-positive input, changing an unread cost to zero can change the optimum for a suitable position.

Bounds use constant-cost arithmetic for the problem's bounded values.

---

### 🚀 What's Next?

Part 2 compares the explicit table with **top-down memoization using an explicit stack**, avoiding Python's recursion-depth limit. I'll also cover independent path enumeration and property-based tests.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
