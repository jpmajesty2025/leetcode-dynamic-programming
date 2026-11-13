# Stock Trading with a Transaction Fee: Cash & Holding States (Part 1 of 2) 📈

**The Problem**:
Maximize profit from as many stock transactions as you like, holding at most one share at a time. Pay **one fee per completed buy/sell pair**.

For `[1, 3, 2, 8, 4, 9]` and `fee = 2`, the answer is **8**:
- Buy at 1, sell at 8: profit **5**.
- Buy at 4, sell at 9: profit **3**.

---

### 💡 Define the Two States

After each day:
- **`cash`**: Best balance with no stock.
- **`hold`**: Best balance while holding one share.

Start with `cash = 0` and `hold = -prices[0]`.

For today's price p, use the previous day's states:
1️⃣ **Stay Flat or Sell**: `next_cash = max(cash, hold + p - fee)`.
2️⃣ **Keep Holding or Buy**: `next_hold = max(hold, cash - p)`.

Return cash. An unsold position isn't realized profit.

---

### ⚠️ Is Reusing Updated Cash a Bug?

The original updates cash first, then uses that new value to update hold.

Substituting the cash update gives:
`new_hold = max(old_hold, old_cash - p, old_hold - fee)`

Because **fee >= 0**, the extra `old_hold - fee` candidate can never improve on `old_hold`.

So the original is correct. Its sequential updates produce the same states as the previous-day recurrence.

The saved DP alternative uses simultaneous assignment to make those dependencies explicit. This is a clarity change, not a correctness fix.

---

### 🧩 Charge the Fee Once

Charging on sale, as above, is convenient. Charging on purchase also works if the initialization and holding-state meaning are adjusted consistently.

Subtracting the fee on both transitions would charge twice per transaction.

Summing positive adjacent differences also fails with a fee: small rises may not cover it, while holding through a small dip can avoid paying again.

---

### 📊 Complexity & Quality

- **Time**: O(n).
- **Auxiliary Space**: O(1).
- **Input Preservation**: Prices aren't modified.
- **Empty or Singleton Inputs**: Return 0.

The original is already asymptotically optimal for the general problem. Suggested improvements are state documentation, an explanation of update order, and a LeetCode wrapper.

The saved alternatives reject negative fees explicitly; those are outside the problem's contract.

---

### 🚀 What's Next?

Part 2 derives an **effective-buy-price greedy solution** with the same complexity and verifies all three implementations using independent transaction enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
