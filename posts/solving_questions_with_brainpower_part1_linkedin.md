# Solving Questions With Brainpower: Suffix DP & Cooldown Jumps (Part 1 of 2) 🧠

**The Problem**:
Each question gives `[points, brainpower]`.
Solve it to earn points, but skip the next `brainpower` questions. Or skip it and consider the next question.

Return the **maximum total score** while processing questions in order.

For `[[3, 2], [4, 3], [4, 4], [2, 5]]`, the answer is **5**: solve questions 0 and 3.

---

### 🧩 Define the Suffix State

**`dp[i]` is the best score from questions i onward, when question i is available.**

At each index:
1. **Skip**: Keep `dp[i + 1]`.
2. **Solve**: Earn the current points and continue after the cooldown.

The first available question is:
`next_question = i + brainpower + 1`

Take the better option:
`dp[i] = max(dp[i + 1], points + future_score)`

Every valid selection either skips or solves question i, so these cases cover every possibility.

---

### ⚠️ Two Indexing Details

1️⃣ **Include the Extra +1**:
Solving question 0 with brainpower 2 blocks questions 1 and 2. The next available question is **3**, not 2.

2️⃣ **Handle the End of the Exam**:
A resume index at or beyond n contributes zero future points. There is no requirement to finish the cooldown inside the array.

---

### 💡 Why Traverse Backward?

Both dependencies are to the right: `i + 1` and the resume index.

Processing from n - 1 down to 0 makes those suffix optima available before computing `dp[i]`. The empty suffix contributes zero, and the answer is **`dp[0]`**.

The original implementation already had this recurrence right. The changes clarify the invariant, document the bounds, and add tests and a submission wrapper.

---

### 📊 Complexity

- **Time**: O(n), worst-case optimal because an unread question could change the answer.
- **Auxiliary Space**: O(n).
- **Input Preservation**: The nested list stays unchanged.

Unlike House Robber, dependencies can jump to arbitrarily distant suffixes. **Two rolling states don't capture the required information.**

Bounds assume constant-cost arithmetic for the problem's bounded values. Empty input returns 0 as a documented extension.

---

### 🚀 What's Next?

Part 2 evaluates the same choices in the opposite direction: **forward DP that propagates scores to available positions**.

I'll also cover independent subset enumeration, cooldown properties, and 100,000-question boundary tests.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
