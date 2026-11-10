# Solving Questions With Brainpower: Forward DP & Verification (Part 2 of 2) ⚡

In Part 1, backward DP asked: **What's the best score available from this question onward?**

Forward DP asks: **What's the best score we can carry to this available decision position?**

---

### 🚀 The Forward State

Let `dp[i]` hold the best accumulated score reaching available position i.

Process positions from left to right. Before processing i, all transitions into it have been handled, so its score is finalized.

There are two outgoing transitions:

1️⃣ **Skip**:
Carry `dp[i]` to position `i + 1`.

2️⃣ **Solve**:
Carry `dp[i] + points` to `i + brainpower + 1`.

Keep the maximum whenever multiple paths reach the same destination.

---

### 💡 One Terminal Position

Clamp every solve destination to **n**, the position past the final question.

A cooldown ending exactly at n and one ending beyond n both mean the exam is finished. Neither permits another score.

The answer is **`dp[n]`**.

Every position is reachable by skipping all earlier questions, so initializing the table to zero represents feasible scores. All transitions move forward, making this a longest-path computation on a directed acyclic graph.

---

### ⚠️ Greedy Choices Can Fail

For `[[8, 3], [5, 1], [1, 1], [5, 1]]`:

- Solving the first question earns 8 and blocks the rest.
- Skipping it allows questions 1 and 3, earning **10**.

A question's immediate score doesn't account for the opportunities its cooldown removes.

---

### 📊 Backward vs. Forward

- **Backward DP**: Compare the values of future suffixes.
- **Forward DP**: Propagate accumulated scores to future positions.
- **Both**: O(n) time, O(n) auxiliary space, with no input mutation.

Bounds assume constant-cost arithmetic. Neither implementation uses recursion, which avoids stack-depth issues at the **100,000-question** input limit.

My default remains the shorter backward recurrence. The forward alternative makes the decision graph and score propagation explicit.

---

### 🧪 Verification

**44 Brainpower tests passed; 235 passed across the complete suite.**

- **Exhaustive Inputs**: All 5,461 arrays of length 0 through 6 drawn from four point/cooldown pairs, per implementation.
- **Independent Oracle**: Enumerate selected index subsets and reject cooldown violations without using either DP recurrence.
- **Boundaries**: Empty/singleton inputs, exact-end jumps, beyond-end jumps, and greedy counterexamples.
- **Hypothesis Properties**: Score scaling, score monotonicity, and the fact that increasing a cooldown cannot improve the optimum.
- **State Safety**: Nested input preservation and repeated calls after input changes.
- **Maximum Size**: Both versions handled 100,000 questions, including a total of **5,000,000,000 points**.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
