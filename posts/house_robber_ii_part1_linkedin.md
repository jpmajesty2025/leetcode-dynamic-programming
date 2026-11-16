# House Robber II: Break the Circle into Two Paths (Part 1 of 2) 🏠

**The Problem**:
Choose houses to maximize the total stolen without choosing adjacent houses. This time, **the first and last houses are neighbors**.

For `[2, 3, 2]`, the answer is **3**. Choosing both 2s would trigger the circular alarm.

---

### 💡 Reuse the Linear Take-or-Skip Recurrence

For a linear range, each house offers two choices:
1️⃣ **Skip**: Keep the previous prefix optimum.
2️⃣ **Take**: Add its amount to the optimum from two houses back.

The recurrence remains:
`current_best = max(one_back, two_back + amount)`

What changes is which houses can belong to the same selection.

---

### 🧩 Exclude One Endpoint

For at least two houses, a valid circular selection cannot contain both endpoints.

Solve two linear problems:
- **Exclude the Last**: Consider indices 0 through n - 2.
- **Exclude the First**: Consider indices 1 through n - 1.

Return the **maximum**, not their sum.

Every circular solution belongs to at least one case. Conversely, every valid selection within either range is legal in the circle.

The cases overlap when neither endpoint is selected. That's harmless when taking a maximum.

---

### ⚠️ Excluding Doesn't Mean Forcing

Excluding the last house doesn't force us to take the first. Each linear DP can still skip any house.

For `[1, 2, 3]`, excluding the last gives 2; excluding the first gives 3. The result is **3**.

A singleton needs separate handling: its value is available, and it isn't treated as its own forbidden neighbor.

---

### 🚫 Don't Apply the Linear Answer Unchanged

For `[10, 1, 1, 10]`:
- Linear House Robber can choose both ends for **20**.
- Circular House Robber can collect only **11**.

Fixed even/odd choices also fail in general. The DP needs the take-or-skip recurrence within each legal range.

---

### 📊 Correctness & Python Space Costs

The original correctly handles empty input, singletons, and the two linear cases. It also preserves nums.

Its helper uses only two totals, but:
**`nums[:-1]` and `nums[1:]` allocate new lists.**

Therefore the original takes:
- **Time**: O(n).
- **Auxiliary Space**: O(n), including slice copies.

Constant-space state inside a helper doesn't make the entire function constant space.

---

### 🚀 What's Next?

Part 2 removes the slices with index ranges, compares an explicit prefix table, and verifies the circular constraint through independent subset enumeration.

#LearningInPublic #Python #Algorithms #DynamicProgramming #LeetCode #CodingInterview #SoftwareEngineering
