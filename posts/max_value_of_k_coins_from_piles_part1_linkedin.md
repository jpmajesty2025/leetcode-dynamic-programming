# Maximum Value of K Coins: Prefix Choices & Group Knapsack (Part 1 of 2) 🪙

**The Problem**:
Choose **exactly k coins** from several piles to maximize their total value. You can only remove the top coin from a pile.

For `[[1, 100, 3], [7, 8, 9]]` and `k = 2`, the answer is **101**: take the first two coins from the first pile.

---

### 💡 Each Pile Offers Prefix Choices

Taking x coins from a pile means taking its **first x coins**, in order.

For `[1, 100, 3]`, the prefix values are:
- Take 0: **0**.
- Take 1: **1**.
- Take 2: **101**.
- Take 3: **104**.

Each pile is one group of mutually exclusive choices. We select one prefix length per pile, including zero.

---

### 🧩 Define the Exact-Count State

**`dp[i][j]` is the maximum value of exactly j coins from the first i piles.**

For every feasible prefix length x from pile i:
`dp[i][j] = max(dp[i - 1][j - x] + prefix[x])`

The previous row supplies the other j - x coins. Prefix sums make each candidate value available in constant time.

For an explicit exact-count implementation, initialize `dp[0][0] = 0` and mark all other counts unreachable.

---

### ⚠️ Why the Original Zero Initialization Works Here

The original table initializes every cell to zero. Its state therefore means **at most j coins**, rather than exactly j.

The final answer is still correct under the problem's positive-value, feasible-k constraints: any selection with fewer than k coins can be extended by taking another exposed coin, increasing its value.

That argument fails for negative values. With `[[-5]]` and `k = 1`, an exact-count answer is **-5**, not zero. The saved exact-table alternative marks unreachable counts with `None`.

---

### 🚫 Greedy Can Miss a Valuable Buried Coin

For `[[1, 100], [50]]` and `k = 2`, repeatedly choosing the largest exposed coin gives **51**.

Taking the first pile's two-coin prefix gives **101**. Sorting coins would destroy the top-to-bottom constraint.

---

### 📊 Complexity & What's Next

Let M be the total number of coins and n the number of piles. Under the problem constraints, the original takes **O(kM) time** and **O(nk + L) auxiliary space**, where L is the longest pile.

Part 2 compresses the table to **O(k) space**, explains descending updates, and checks the implementations against independent prefix-choice enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #Knapsack #LeetCode #CodingInterview
