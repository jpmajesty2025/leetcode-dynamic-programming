# House Robber II: Slice-Free Ranges & Circular Tests (Part 2 of 2) ⚡

Part 1 reduced the circle to two linear problems: exclude the first house or exclude the last.

The recurrence already needs only two totals. Removing Python's list slices makes that space saving apply to the whole function.

---

### 💡 Pass Bounds Instead of Copies

The saved helper takes a half-open index range:
**`rob_range(start, stop)`**

It reads amounts directly from nums, using `range(start, stop)`.

Compare:
1️⃣ **`rob_range(0, n - 1)`**: Exclude the last house.
2️⃣ **`rob_range(1, n)`**: Exclude the first house.

No input slices or copied sublists are needed.

---

### 🧩 Preserve the Prefix Invariant

Before processing the next house:
- **`one_back`** is the best total for the processed prefix.
- **`two_back`** is the best total for that prefix without its last house.

Update both together:
`two_back, one_back = one_back, max(one_back, two_back + amount)`

Python evaluates the right-hand side before assigning either new total. Taking the current house therefore uses the correct earlier prefix.

Starting both totals at zero permits skipping every house.

---

### 📊 Complexity & the Table Alternative

Under constant-cost integer arithmetic:
- **Original with Slices**: O(n) time, O(n) auxiliary space.
- **Slice-Free Ranges**: O(n) time, **O(1) auxiliary variables**.
- **Explicit Prefix Tables**: O(n) time, O(n) auxiliary space.

All preserve the input and assume nonnegative house values.

Linear time is worst-case optimal: an unread house could change the maximum.

The range version is my default for returning only the amount. The table version keeps intermediate prefix optima visible; recovering chosen house indices would need additional traceback logic.

Python integer sizes grow with the amounts and totals, so these aren't constant-bit arithmetic bounds.

---

### ⚠️ Circular Properties Differ from Linear Ones

An odd circle of nine houses worth 5 each yields **20**, not the linear answer 25.

Rotating the list doesn't change the circular optimum. Reversing it doesn't either.

Appending a zero house has a different effect: it separates the original endpoints, making the circular result equal to the original list's **linear** optimum. It needn't preserve the old circular answer.

---

### 🧪 Independent Verification

The oracle enumerates house subsets and rejects every selected neighbor pair, including the last-to-first edge.

Coverage includes:
- **Exhaustive Inputs**: All 3,280 lists of lengths 0 through 7 over `{0, 1, 2}`.
- **Hypothesis Properties**: Rotation, reversal, scaling, and single-house value monotonicity.
- **Regressions**: Endpoint conflicts, singletons, pairs, odd cycles, zeros, and large amounts.
- **Contracts**: Nonmutation, repeated calls, wrappers, and a list that rejects slicing.
- **Scale Checks**: 10,000- and 10,001-house inputs.

#LearningInPublic #Python #Algorithms #DynamicProgramming #SoftwareTesting #Hypothesis #LeetCode
