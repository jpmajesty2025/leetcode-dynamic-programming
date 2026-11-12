# House Robber: DP Invariants & Constant-Space Optimization (Part 1 of 2) 🏠

**The Problem**:
Given a list of houses, each containing some money. Robbing two adjacent houses triggers the alarm and you get caught!
Return the **maximum total you can rob from the houses without getting caught**.

For `[2, 7, 9, 3, 1]`, the answer is **12**: take `2 + 9 + 1`.

---

### 🧩 The Take-or-Skip Decision

My starting solution stored the best total up to each house in a DP table.

At the current house, there are two possibilities:
1. **Skip it**: Keep the optimum from the previous prefix.
2. **Take it**: Add its value to the optimum that excludes its neighbor.

The recurrence is:
`current_best = max(previous_best, two_back_best + amount)`

Every valid selection falls into one of these cases, so their maximum gives the optimum for the current prefix.

---

### ⚠️ Two Pitfalls to Watch

1️⃣ **Fixed Even/Odd Selection**:
For `[2, 1, 1, 2]`, either parity sums to 3. Choosing both ends gives **4**! An optimal selection can mix index parities.

2️⃣ **Updating State Too Early**:
Overwriting a previous total before computing the new optimum can accidentally count adjacent houses together.

---

### 💡 Two Totals Replace the Table

Before processing each house:

1️⃣ **`one_back`**: The optimum for the prefix already processed.
2️⃣ **`two_back`**: The optimum for that prefix without its final house.

Only these two states are read by the next update. **Older table entries can be discarded.**

Python's simultaneous assignment computes both new values from the old state. Starting both totals at zero also handles empty input without a separate branch.

The caller's list stays unchanged.

---

### 📊 Complexity

- **Original Table**: O(n) time, O(n) auxiliary space.
- **Rolling Totals**: O(n) time, improved **O(1) auxiliary space**.

Linear time is worst-case optimal: an unread house could change the answer. These bounds use the usual constant-cost arithmetic model for the problem's bounded values.

---

### 🚀 What's Next?

In Part 2, I'll compare:
1. **Prefix DP Table**: Explicit states that can support a later reconstruction step.
2. **Top-Down Memoization**: The same decision modeled recursively, with a cache scoped to each call.

#LearningInPublic #Python #Algorithms #DataStructures #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
