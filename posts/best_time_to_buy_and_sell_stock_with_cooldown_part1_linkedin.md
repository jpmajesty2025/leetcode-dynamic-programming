# Stock Trading with Cooldown: Three States & Legal Transitions (Part 1 of 2) 📈

**The Problem**:
Maximize stock-trading profit while holding at most one share. After selling, **you cannot buy on the next day**.

For `[1, 2, 3, 0, 2]`, the answer is **3**:
Buy at 1, sell at 2, wait through price 3, buy at 0, and sell at 2.

---

### 💡 Separate the Two Ways to Own No Stock

After each day:
- **`hold`**: Best balance while holding a share.
- **`sold`**: Best balance after selling today.
- **`rest`**: Best balance with no stock and no sale today.

A sale today blocks buying tomorrow. Resting today makes buying tomorrow legal.

Combining both flat states too early would lose that distinction.

---

### 🧩 Define the Previous-Day Transitions

For today's price p:
1️⃣ **Hold or Buy**: `next_hold = max(hold, rest - p)`.
2️⃣ **Sell Today**: `next_sold = hold + p`.
3️⃣ **Rest Today**: `next_rest = max(rest, sold)`.

Buying reads yesterday's rest, so yesterday's sale cannot fund today's purchase.

Return **`max(rest, sold)`**. A final-day sale is valid; there's no requirement to complete its cooldown after the price sequence ends.

---

### ⚠️ Why the Original Saves Previous Cash

In the original, `cash` means rest and `cooldown` means sold today.

It saves `prev_cash` before merging yesterday's sale into today's rest. Buying then uses that saved value.

Using the newly merged cash would allow buying immediately after yesterday's sale.

For `[1, 2, 0, 2]`, unrestricted trading earns **3**, but the cooldown-constrained answer is **2**.

---

### 🔍 Initialization & Naming

The original starts `cooldown = 0`, although selling on the first day is unreachable.

That placeholder is harmless: it only competes with the already-valid zero resting balance, then gets overwritten by a real sale candidate.

The saved table version uses `None` for the unreachable first-day sale and names the states explicitly.

---

### 📊 Complexity & Quality

The original is correct and already optimal:
- **Time**: O(n).
- **Auxiliary Space**: O(1).
- **Mutation**: Prices aren't changed.
- **Empty or Singleton Inputs**: Return 0.

The main improvements are clearer state names, documented update dependencies, and a LeetCode wrapper.

---

### 🚀 What's Next?

Part 2 combines the flat states and enforces cooldown with **cash from two days earlier**, then checks all implementations using independent transaction enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
