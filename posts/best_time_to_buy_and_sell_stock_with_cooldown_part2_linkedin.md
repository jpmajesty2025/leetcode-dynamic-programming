# Stock Trading with Cooldown: Cash from Two Days Earlier (Part 2 of 2) ⚡

In Part 1, holding, sold-today, and resting states made the cooldown rule explicit.

Another O(1)-space formulation tracks **cash, holding balance, and one delayed cash value**.

---

### 💡 Combine the Flat States

Let:
- **`cash[d]`**: Best profit through day d while owning no stock, including a sale today.
- **`hold[d]`**: Best balance through day d while holding one share.

Selling today can use yesterday's holding state:
`cash[d] = max(cash[d - 1], hold[d - 1] + prices[d])`

Buying today must skip yesterday's possible sale:
`hold[d] = max(hold[d - 1], cash[d - 2] - prices[d])`

**The two-day cash dependency encodes the cooldown.**

---

### ⚠️ Preserve the Delayed Value

Before processing a day, keep:
- Yesterday's cash.
- Yesterday's holding balance.
- Cash from two days earlier.

Calculate both new states from those old values, then move yesterday's cash into the delayed slot.

The saved implementation uses simultaneous assignment so none of these dependencies is overwritten early.

For day 1, the delayed cash is **0**, representing the flat balance before day 0.

---

### 🧩 One Extra Rest Day Changes the Answer

For `[0, 5, 0, 5]`, the answer is **5**. Selling on day 1 blocks buying at day 2's zero price.

For `[0, 5, 0, 0, 5]`, the answer is **10**. There is now a legal rest day before the second purchase.

A fee-free unlimited-transactions sum would incorrectly return 10 for both inputs.

---

### 📊 Complexity & Trade-Offs

- **Original Three-State Version**: O(n) time, O(1) auxiliary space.
- **Lagged-Cash Alternative**: O(n) time, O(1) auxiliary space.
- **Explicit State Table**: O(n) time, O(n) auxiliary space.

The lagged version changes the interpretation, not the asymptotic efficiency. The table keeps intermediate states visible but returns only profit; recovering a trade plan needs additional traceback logic.

All three preserve the input.

---

### 🧪 Independent Verification

The oracle enumerates ordered buy/sell endpoints and rejects schedules where a purchase occurs the day after a sale.

Coverage includes:
- **Exhaustive Inputs**: All 3,280 lists of lengths 0 through 7 over `{0, 1, 2}`, per implementation.
- **Hypothesis Properties**: Price-shift invariance, scaling, appended-day monotonicity, and input preservation.
- **Regressions**: Immediate repurchases, final-day sales, exact cooldown gaps, flat and falling prices, and large profits.
- **Scale Checks**: 50,000-day rising prices and a 60,000-day repeating sequence.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
