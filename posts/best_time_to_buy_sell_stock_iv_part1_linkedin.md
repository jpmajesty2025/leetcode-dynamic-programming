# Best Time to Buy and Sell Stock IV: The Best Buy Balance (Part 1 of 2) 📈

**The Problem**:
Given daily stock prices and a budget of k transactions, return the **maximum profit**. Sell your current share before buying again.

For `k = 2` and `[3, 2, 6, 5, 0, 3]`, the answer is **7**: buy at 2, sell at 6, then buy at 0 and sell at 3.

---

### 💡 Define the Transaction-Prefix State

**`dp[t][d]` is the best realized profit through day d with at most t completed transactions.**

With zero transactions or only the first day available, profit is zero.

For each later day, choose between:
1️⃣ **Keep Yesterday's Profit**: `dp[t][d - 1]`.
2️⃣ **Sell Today**: Add today's price to the best balance after an earlier buy.

For a buy day b, that balance is:
`dp[t - 1][b] - prices[b]`

Scanning every earlier buy day for every cell would cost O(kn²).

---

### 🧩 Maintain the Best Buy Balance

Keep a running maximum called `max_diff`:
`dp[t][d] = max(dp[t][d - 1], prices[d] + max_diff)`

After calculating today's sale, update:
`max_diff = max(max_diff, dp[t - 1][d] - prices[d])`

**Calculate the sale first, then include today's buy candidate for future days.** This keeps the running maximum aligned with earlier buy days.

The recurrence allows a previous sale and repurchase on the same day. With no fee or cooldown, those trades can be merged without changing profit, so they cannot inflate the answer.

---

### 🚀 When the Transaction Cap Stops Binding

If **`k >= n // 2`**, there is enough budget for every useful transaction.

Sum the positive adjacent price differences, equivalent to collecting the gain from each rising run.

For `[1, 5, 2, 10]`:
- One transaction earns **9**.
- Two transactions earn **12**.

The shortcut applies only when the budget is sufficient.

---

### 📊 Complexity & Quality

For n days:
- **Constrained Case**: O(nk) time, O(nk) auxiliary space.
- **Unlimited Case**: O(n) time, O(1) auxiliary space.

The original implementation is correct for valid inputs and doesn't modify prices. An early return for zero budgets avoids allocating an unnecessary row.

---

### 🚀 What's Next?

Part 2 replaces the full table with **O(k)-space cash and holding states**, compares an O(n)-space rolling row, and checks all three implementations against independent transaction enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
