"""Check Coin Change independently by enumerating denomination multiplicities."""

from itertools import combinations, product

import pytest
from hypothesis import given, settings, strategies as st

import coin_change as coin_first
import coin_change_amount_first as amount_first
import coin_change_bfs as bfs

MODULES = (coin_first, amount_first, bfs)
IMPLS = [pytest.param(m.coin_change, id=m.__name__) for m in MODULES]
SMALL_COINS = st.lists(st.integers(1, 10), max_size=4)


def multiplicity_oracle(coins, amount):
    """Enumerate coin counts, not DP states or BFS layers."""
    denominations = sorted(set(coins))
    best = None
    ranges = [range(amount // coin + 1) for coin in denominations]
    for counts in product(*ranges):
        if sum(c * k for c, k in zip(denominations, counts)) == amount:
            count = sum(counts)
            best = count if best is None else min(best, count)
    return -1 if best is None else best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("coins", "amount", "expected"),
    [
        ([1, 2, 5], 11, 3),
        ([2], 3, -1),
        ([1], 0, 0),
        ([], 0, 0),
        ([], 7, -1),
        ([1], 7, 7),
        ([3], 9, 3),
        ([1, 3, 4], 6, 2),
        ([4, 1, 3, 3], 6, 2),
        ([2, 4], 7, -1),
        ([4, 6], 2, -1),
        ([5, 7], 7, 1),
        ([2**31 - 1], 10_000, -1),
        ([2, 5, 10, 1], 27, 4),
        ([1], 10_000, 10_000),
        ([1, 2, 5], 10_000, 2_000),
        ([6, 10], 14, -1),
    ],
)
def test_examples_and_boundaries(solve, coins, amount, expected):
    original = coins.copy()
    assert type(solve(coins, amount)) is int
    assert solve(coins, amount) == expected
    assert coins == original


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for size in range(6):
        for values in combinations(range(1, 6), size):
            coins = list(values)
            for amount in range(21):
                assert solve(coins, amount) == multiplicity_oracle(coins, amount)


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("coins", "amount"),
    [([1], -1), ([], -1), ([0], 5), ([-1, 2], 3), ([0], 0), ([-1], 0)],
)
def test_invalid_values(solve, coins, amount):
    original = coins.copy()
    with pytest.raises(ValueError):
        solve(coins, amount)
    assert coins == original


@pytest.mark.parametrize("solve", IMPLS)
@given(coins=SMALL_COINS, amount=st.integers(0, 20))
@settings(max_examples=100, deadline=None)
def test_independent_oracle_and_nonmutation(solve, coins, amount):
    original = coins.copy()
    assert solve(coins, amount) == multiplicity_oracle(coins, amount)
    assert coins == original


@pytest.mark.parametrize("solve", IMPLS)
@given(coins=SMALL_COINS, amount=st.integers(0, 100))
@settings(max_examples=100, deadline=None)
def test_order_and_duplicate_invariance(solve, coins, amount):
    result = solve(coins, amount)
    assert solve(coins[::-1], amount) == result
    assert solve(coins + coins, amount) == result


@pytest.mark.parametrize("solve", IMPLS)
@given(coins=SMALL_COINS, amount=st.integers(0, 40), scale=st.integers(1, 10))
@settings(max_examples=100, deadline=None)
def test_scaling_denominations_and_target(solve, coins, amount, scale):
    assert solve([c * scale for c in coins], amount * scale) == solve(coins, amount)


@pytest.mark.parametrize("solve", IMPLS)
@given(coins=SMALL_COINS, amount=st.integers(0, 100), extra=st.integers(1, 20))
@settings(max_examples=100, deadline=None)
def test_adding_denomination_cannot_worsen_feasible_solution(solve, coins, amount, extra):
    before = solve(coins, amount)
    after = solve(coins + [extra], amount)
    if before != -1:
        assert 0 <= after <= before


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls_and_changed_input(solve):
    coins = [1, 3, 4]
    assert solve(coins, 6) == 2
    assert solve([2], 3) == -1
    coins[:] = [2]
    assert solve(coins, 6) == 3
    assert solve([], 0) == 0


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    coins = [1, 2, 5]
    assert solution.coinChange(coins, 11) == 3
    assert coins == [1, 2, 5]
    assert solution.coinChange([], 0) == 0
    with pytest.raises(ValueError):
        solution.coinChange([0], 0)
