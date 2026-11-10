# Min Cost Climbing Stairs: Tables, Memoization & Testing (Part 2 of 2) ⚡

In Part 1, we reduced the prefix DP table to **two rolling states**, keeping O(n) time while using O(1) auxiliary space.

Here are two alternatives for studying the same problem.

---

### 🚀 Alternative 1: Prefix DP Table

**`dp[k]` is the minimum cost to reach position k before paying there.**

Start with `dp[0] = dp[1] = 0`, then fill positions 2 through n.

**Why keep the table?**
Every intermediate optimum is available to inspect. The stored values can also support a later traceback to recover a route, with a tie-breaking policy.

The current implementation returns only the minimum total.

---

### 💡 Alternative 2: Top-Down Memoization

Define **`best(i)` as the minimum remaining cost when leaving step i**.

Pay `cost[i]`, then choose the cheaper continuation from i + 1 or i + 2. Positions at or beyond the top contribute zero.

Since either starting position is allowed, return:
`min(best(0), best(1))`

Notice the state difference: this suffix value **includes the current step's payment**, while the prefix value measures arrival before payment.

---

### ⚠️ Python's Recursion Limit

The problem permits **1,000 steps**. A recursive memoized implementation can hit Python's recursion limit within that valid input range.

The saved top-down alternative uses an **explicit stack**:
1. Inspect the current state.
2. Evaluate any missing dependency.
3. Cache the state once both dependencies are available.

The memo dictionary belongs to each call, avoiding stale results across inputs. This keeps the suffix recurrence without changing the interpreter's recursion limit.

---

### 📊 Complexity

- **Rolling States**: O(n) time, **O(1) auxiliary space**.
- **Prefix Table**: O(n) time, O(n) auxiliary space.
- **Explicit-Stack Memoization**: O(n) time, O(n) auxiliary space.

All three leave the input unchanged. Bounds assume constant-cost arithmetic for bounded values.

---

### 🧪 Verification

**69 tests for this problem passed; 140 passed across the full suite.**

- **Boundaries**: Examples, empty/singleton extensions, zeros, ties, and 1,000-step inputs.
- **Exhaustive Inputs**: All 3,280 arrays of length 0 through 7 over `{0, 1, 2}`, per implementation.
- **Independent Oracle**: Enumerate legal paths without caching or the prefix recurrence.
- **Properties**: Nonnegative scaling and cost monotonicity, plus input preservation and repeated-call checks.
- **Stress Case**: All three handled 10,000 steps without recursion-limit changes.

For returning only the minimum total, **rolling states remain my default**. The table makes prefix states visible; explicit-stack memoization exposes the suffix dependencies at the cost of more machinery.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
