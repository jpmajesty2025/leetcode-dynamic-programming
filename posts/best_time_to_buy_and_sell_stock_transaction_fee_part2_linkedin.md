# Stock Trading with a Transaction Fee: Effective Buy Price (Part 2 of 2) ⚡

In Part 1, cash and holding states solved the problem in O(n) time and O(1) space.

A greedy formulation keeps **profit and an effective buy price**, with the same bounds.

---

### 💡 Include the Fee in the Buy Threshold

Initialize:
- **`profit = 0`**.
- **`effective_buy = prices[0] + fee`**.

For each later price p:
1️⃣ If `p + fee < effective_buy`, lower the threshold to `p + fee`.
2️⃣ Otherwise, if `p > effective_buy`, add `p - effective_buy` to profit and set `effective_buy = p`.

That second reset is important.

---

### ⚠️ A Profitable Rise May Continue

For `[1, 4, 7]` and `fee = 2`, the starting threshold is **3**.

At price 4:
- Add **1** to profit.
- Reset the effective buy price to **4**, not 6.

At price 7, add another **3**. Total profit is **4**, matching one trade from 1 to 7 with a single fee.

The reset is a **virtual re-entry**, not a literal second purchase. It preserves the option to extend the same trade without paying another fee.

Resetting to `p + fee` after every profitable rise would undercount that continuation.

---

### 🧩 When Does a New Trade Help?

For `[1, 5, 4, 8]` and `fee = 2`, the small dip doesn't justify a fresh fee. The answer is **5**, from holding between 1 and 8.

For `[1, 5, 1, 5]`, the deeper dip lowers the effective buy threshold. Two completed trades earn **4**.

The threshold tracks these choices without committing to a literal sale every time profit increases.

---

### 🔍 Connect Greedy Back to DP

The states satisfy:
**`profit = cash`**
**`effective_buy = cash - hold + fee`**

The DP sale transition becomes:
`new_profit = profit + max(0, p - effective_buy)`

The holding transition either lowers the threshold to `p + fee`, preserves it, or resets it to p after a profitable rise.

This gives the greedy rules a state-based justification.

---

### 📊 Complexity & Trade-Offs

- **Time**: O(n).
- **Auxiliary Space**: O(1).
- **Mutation**: Neither saved alternative changes prices.

The explicit previous-day DP is my default for readability. The greedy version offers a useful alternative interpretation, but its virtual reset needs explanation.

---

### 🧪 Independent Verification

The tests enumerate strictly ordered buy/sell endpoints, charge one fee per pair, and include choosing no trades.

Coverage includes:
- **Exhaustive Inputs**: Every list of length 0 through 6 over `{0, 1, 2}`, with fees 0 through 3.
- **Hypothesis Properties**: Higher fees can't improve profit, price shifts preserve profit, and scaling prices and fees scales profit.
- **Regressions**: Continuing rises, shallow and deep dips, fee-sized gains, empty inputs, and 50,000-day cases.

#LearningInPublic #Python #Algorithms #GreedyAlgorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
