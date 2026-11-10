"""Cross-implementation tests with independent enumeration of legal paths."""

from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import min_cost_climbing_stairs as rolling
import min_cost_climbing_stairs_dp_table as table
import min_cost_climbing_stairs_top_down as memoized

MODULES = (rolling, table, memoized)
IMPLS = [
    pytest.param(module.min_cost_climbing_stairs, id=module.__name__)
    for module in MODULES
]
SMALL_COSTS = st.lists(st.integers(0, 999), max_size=12)


def path_oracle(cost):
    """Enumerate paths without memoization or the prefix DP recurrence."""
    best = float("inf")
    stack = [(0, 0), (1, 0)]
    while stack:
        position, paid = stack.pop()
        if position >= len(cost):
            best = min(best, paid)
        else:
            paid += cost[position]
            stack.append((position + 1, paid))
            stack.append((position + 2, paid))
    return int(best)


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("cost", "expected"),
    [
        ([], 0),
        ([7], 0),
        ([0], 0),
        ([10, 15, 20], 15),
        ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6),
        ([1, 2], 1),
        ([2, 1], 1),
        ([9, 9], 9),
        ([0, 0], 0),
        ([0, 999, 0, 999], 0),
        ([999, 0, 999, 0], 0),
        ([1, 2, 100, 1], 3),
        ([5] * 9, 20),
        ([999] * 1000, 499_500),
        ([0] * 1000, 0),
        ([0, 999] * 500, 0),
    ],
)
def test_examples_and_boundaries(solve, cost, expected):
    original = cost.copy()
    assert solve(cost) == expected
    assert cost == original


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for size in range(8):
        for values in product(range(3), repeat=size):
            cost = list(values)
            assert solve(cost) == path_oracle(cost), cost


@pytest.mark.parametrize("solve", IMPLS)
@given(cost=SMALL_COSTS)
@settings(max_examples=150, deadline=None)
def test_oracle_and_nonmutation(solve, cost):
    original = cost.copy()
    result = solve(cost)
    assert type(result) is int
    assert result == path_oracle(cost)
    assert cost == original


@pytest.mark.parametrize("solve", IMPLS)
@given(cost=SMALL_COSTS, factor=st.integers(0, 10))
@settings(max_examples=100, deadline=None)
def test_scaling_and_bounds(solve, cost, factor):
    result = solve(cost)
    assert solve([factor * value for value in cost]) == factor * result
    assert 0 <= result <= min(sum(cost[::2]), sum(cost[1::2]))


@pytest.mark.parametrize("solve", IMPLS)
@given(
    cost=st.lists(st.integers(0, 999), min_size=2, max_size=100),
    data=st.data(),
)
@settings(max_examples=100, deadline=None)
def test_increasing_one_cost_is_monotone_and_bounded(solve, cost, data):
    i = data.draw(st.integers(0, len(cost) - 1))
    increase = data.draw(st.integers(0, 999))
    modified = cost.copy()
    modified[i] += increase
    before, after = solve(cost), solve(modified)
    assert before <= after <= before + increase


@pytest.mark.parametrize("solve", IMPLS)
def test_per_call_state_and_input_changes(solve):
    cost = [10, 15, 20]
    assert solve(cost) == 15
    assert solve([1, 2]) == 1
    cost[:] = [1, 2, 100, 1]
    assert solve(cost) == 3
    assert solve([]) == 0


@pytest.mark.parametrize("module", MODULES, ids=lambda module: module.__name__)
def test_leetcode_wrapper(module):
    solution = module.Solution()
    assert solution.minCostClimbingStairs([10, 15, 20]) == 15
    assert solution.minCostClimbingStairs([]) == 0


@pytest.mark.parametrize("solve", IMPLS)
def test_long_input_without_recursion_limit_changes(solve):
    assert solve([1] * 10_000) == 5_000
