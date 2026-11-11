# Coin Change: Final-Coin DP & Shortest-Path BFS (Part 2 of 2) ⚡

In Part 1, denomination-first DP used ascending amount updates to allow unlimited coin reuse.

Two alternatives give us different ways to reason about the same minimum count.

---

### 💡 Alternative 1: Amount-First DP

**`dp[x]` is the minimum number of coins forming amount x.**

Process amounts from 1 through the target. At each amount, try every denomination that fits as the **final coin**.

If that final coin is c, the candidate is:
`dp[x - c] + 1`

Every solution has a final coin, and x - c is smaller than x because denominations are positive. Its optimum is already available when needed.

Both DP loop orders minimize the same objective. Their state interpretations explain why the updates are valid; changing loop order in other coin problems, such as counting arrangements, can change what gets counted.

---

### 🚀 Alternative 2: Breadth-First Search

View each amount from 0 to the target as a graph vertex. Adding one coin creates an edge to the resulting amount, provided it doesn't exceed the target.

**Every edge costs one coin.** BFS visits vertices in nondecreasing edge distance, so the first arrival at the target gives the minimum count.

1️⃣ Start at amount 0 with count 0.
2️⃣ Add each denomination to generate neighbors.
3️⃣ Mark amounts visited when enqueuing them, preventing repeated expansion.

If the queue empties without reaching the target, return **-1**. For target zero, return 0 after validating the inputs.

---

### 📊 Trade-offs

For m denominations and positive target A, all three have **O(mA) worst-case time and O(A) auxiliary space**.

Including input validation and empty/zero cases: O(mA + m + A) time and O(A + 1) space. These are pseudo-polynomial bounds under constant-cost arithmetic.

BFS can stop when it finds the target, but adds queue and visited-state bookkeeping. It isn't a guaranteed speedup.

My default remains the compact denomination-first DP. Amount-first DP exposes the final-coin argument; BFS exposes the shortest-path structure.

---

### 🧪 Independent Verification

**90 Coin Change tests passed; 383 passed across the complete suite.**

- **Exhaustive Cases**: All subsets of denominations `{1, 2, 3, 4, 5}` with targets 0–20: 672 cases per implementation.
- **Independent Oracle**: Enumerate denomination multiplicities and minimize their sum, without DP or BFS.
- **Regressions**: Unlimited reuse, greedy counterexamples, duplicates, empty inputs, unreachable targets, and target 10,000.
- **Hypothesis Properties**: Denomination-order and duplicate invariance, scaling denominations and target together, and adding denominations without worsening a feasible solution.
- **API Checks**: Invalid-value rejection, input preservation, repeated calls, and LeetCode wrappers.

#LearningInPublic #Python #Algorithms #DynamicProgramming #BreadthFirstSearch #SoftwareTesting #Hypothesis #LeetCode
