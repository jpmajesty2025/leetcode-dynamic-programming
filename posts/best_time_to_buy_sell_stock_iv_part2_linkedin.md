# Best Time to Buy and Sell Stock IV: Cash & Holding States (Part 2 of 2) ⚡

In Part 1, the full table used O(nk) time and O(nk) auxiliary space.

For a profit-only answer, **cash and holding states for each transaction budget** reduce storage to O(k).

---

### 💡 Define the Two States

For each budget t:
- **`cash[t]`**: Best balance with no stock and at most t completed transactions.
- **`hold[t]`**: Best balance while holding stock, with at most t - 1 completed transactions.

Initialize cash to zero and each active holding state to `-prices[0]`. These are **at-most budgets**, so buying on the first day is valid for every positive budget.

Each new day offers two transitions:
1️⃣ **Sell**: `cash[t] = max(cash[t], hold[t] + price)`.
2️⃣ **Buy**: `hold[t] = max(hold[t], cash[t - 1] - price)`.

Return `cash[k]`; an unsold position doesn't count as realized profit.

---

### ⚠️ Preserve the Previous-Day Dependencies

Process budgets **from k down to 1**, updating cash before holding.

- Descending budgets leave `cash[t - 1]` at yesterday's value for the buy transition.
- Updating cash first lets the sell transition read yesterday's `hold[t]`.

Ascending updates can still give the same answer in this fee-free, no-cooldown problem because same-day trades can be merged. The saved ordering follows the previous-day recurrence explicitly; other stock variants need their own transition analysis.

---

### 📊 Complexity & an Alternative

For `0 < k < n // 2`:
- **Time**: O(nk).
- **Auxiliary Space**: O(k).

Keep the unlimited-transactions shortcut: **O(n) time, O(1) space** when `k >= n // 2`. Nonpositive budgets or fewer than two days return 0 immediately.

The separate **O(n)-space rolling-row version** follows the original recurrence more closely. Save each previous-row cell before overwriting it so the next best-buy update reads the correct transaction row.

---

### 🧪 Independent Verification

**522 tests passed across the complete repository suite.**

- **Exhaustive Inputs**: All price lists of lengths 0 through 6 over `{0, 1, 2}`, with budgets 0 through 4: 5,465 cases per implementation.
- **Independent Oracle**: Enumerate legal buy/sell endpoints and take the best profit, including no trades.
- **Hypothesis Properties**: Budget monotonicity, price-shift invariance, scaling, and input preservation.
- **Regressions**: Empty inputs, zero budgets, falling prices, repeated peaks, large profits, and shortcut boundaries.

For returning only profit, **the O(k)-space state machine is my default**.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
