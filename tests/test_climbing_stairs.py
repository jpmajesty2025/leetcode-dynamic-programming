"""Shared Climbing Stairs checks using independent counting methods."""

from math import comb

import pytest
from hypothesis import given, settings, strategies as st

import climbing_stairs as rolling
import climbing_stairs_dp_table as table
import climbing_stairs_fast_doubling as doubling

MODULES = (rolling, table, doubling)
IMPLS = [pytest.param(m.climb_stairs, id=m.__name__) for m in MODULES]


def combinatorial_oracle(n):
    """Choose positions for k two-step moves among n-k total moves."""
    return sum(comb(n - k, k) for k in range(n // 2 + 1))


def path_oracle(n):
    """Enumerate every route using an explicit stack, without memoization."""
    routes = 0
    stack = [0]
    while stack:
        position = stack.pop()
        if position == n:
            routes += 1
        else:
            for step in (1, 2):
                if position + step <= n:
                    stack.append(position + step)
    return routes


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8),
     (10, 89), (45, 1_836_311_903), (100, 573_147_844_013_817_084_101)],
)
def test_known_counts(solve, n, expected):
    assert type(solve(n)) is int
    assert solve(n) == expected


@pytest.mark.parametrize("solve", IMPLS)
def test_all_leetcode_inputs(solve):
    for n in range(1, 46):
        assert solve(n) == combinatorial_oracle(n)


@pytest.mark.parametrize("solve", IMPLS)
def test_explicit_route_enumeration(solve):
    for n in range(16):
        assert solve(n) == path_oracle(n)


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize("n", [-1, -2, -1000])
def test_negative_inputs_rejected(solve, n):
    with pytest.raises(ValueError, match="nonnegative"):
        solve(n)


@pytest.mark.parametrize("solve", IMPLS)
@given(n=st.integers(0, 300))
@settings(max_examples=100, deadline=None)
def test_combinatorial_oracle(solve, n):
    assert solve(n) == combinatorial_oracle(n)


@pytest.mark.parametrize("solve", IMPLS)
@given(n=st.integers(0, 1000))
@settings(max_examples=100, deadline=None)
def test_recurrence_and_monotonicity(solve, n):
    current, following = solve(n), solve(n + 1)
    assert current > 0
    assert following >= current
    assert solve(n + 2) == current + following


@pytest.mark.parametrize("solve", IMPLS)
def test_large_exact_result(solve):
    assert solve(1000) == combinatorial_oracle(1000)


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls(solve):
    assert [solve(n) for n in (5, 0, 45, 1, 5)] == [8, 1, 1_836_311_903, 1, 8]


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    assert solution.climbStairs(45) == 1_836_311_903
    assert solution.climbStairs(0) == 1
    with pytest.raises(ValueError):
        solution.climbStairs(-1)


def test_fast_doubling_large_index():
    # Independent linear recurrence at a size beyond ordinary interview inputs.
    assert doubling.climb_stairs(100_000) == rolling.climb_stairs(100_000)
