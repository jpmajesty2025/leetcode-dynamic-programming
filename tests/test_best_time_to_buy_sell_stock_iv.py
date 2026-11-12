"""Check Stock IV implementations against explicit transaction endpoints."""

from itertools import combinations, product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import best_time_to_buy_sell_stock_iv as original
import best_time_to_buy_sell_stock_iv_rolling_dp as rolling
import best_time_to_buy_sell_stock_iv_state_machine as state_machine

MODULES = (original, rolling, state_machine)
ALTERNATIVES = (rolling, state_machine)
IMPLS = [pytest.param(m.max_profit, id=m.__name__) for m in MODULES]
SMALL_PRICES = st.lists(st.integers(min_value=0, max_value=30), max_size=8)


def endpoint_oracle(k, prices):
    """Enumerate strictly increasing buy/sell days; no DP or greedy logic."""
    best = 0
    for count in range(1, min(k, len(prices) // 2) + 1):
        for days in combinations(range(len(prices)), 2 * count):
            profit = sum(
                prices[days[i + 1]] - prices[days[i]]
                for i in range(0, len(days), 2)
            )
            best = max(best, profit)
    return best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("k", "prices", "expected"),
    [
        (0, [], 0),
        (3, [], 0),
        (0, [1, 5, 2, 8], 0),
        (1, [7], 0),
        (100, [7], 0),
        (1, [2, 4], 2),
        (1, [4, 2], 0),
        (2, [2, 4, 1], 2),
        (2, [3, 2, 6, 5, 0, 3], 7),
        (1, [3, 2, 6, 5, 0, 3], 4),
        (1, [1, 2, 3, 4, 5], 4),
        (2, [5, 4, 3, 2, 1], 0),
        (2, [5, 5, 5, 5, 5, 5], 0),
        (2, [0, 0, 0, 0], 0),
        (1, [1, 5, 2, 10], 9),
        (2, [1, 5, 2, 10], 12),
        (2, [1, 2, 1, 2, 1, 2], 2),
        (3, [1, 2, 1, 2, 1, 2], 3),
        (4, [1, 2, 1, 2, 1, 2], 3),
        (2, [2, 4, 1, 7, 5, 3, 6, 4], 9),
        (2, [0, 10**12, 0, 10**12, 0, 0], 2 * 10**12),
        (10**9, [3, 2, 6, 5, 0, 3], 7),
        (100, [0, 100] * 500, 10_000),
    ],
)
def test_examples_and_boundaries(solve, k, prices, expected):
    before = prices.copy()
    result = solve(k, prices)
    assert type(result) is int
    assert result == expected
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for n in range(7):
        for values in product(range(3), repeat=n):
            prices = list(values)
            for k in range(5):
                assert solve(k, prices) == endpoint_oracle(k, prices), (k, prices)


@pytest.mark.parametrize("solve", IMPLS)
@given(prices=SMALL_PRICES, k=st.integers(min_value=0, max_value=10))
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_no_mutation(solve, prices, k):
    before = prices.copy()
    assert solve(k, prices) == endpoint_oracle(k, prices)
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
@given(
    prices=SMALL_PRICES,
    k=st.integers(min_value=0, max_value=8),
    shift=st.integers(min_value=0, max_value=100),
    scale=st.integers(min_value=0, max_value=5),
    extra=st.integers(min_value=0, max_value=30),
)
@settings(max_examples=150, deadline=None)
def test_profit_properties(solve, prices, k, shift, scale, extra):
    profit = solve(k, prices)
    unlimited = sum(max(b - a, 0) for a, b in zip(prices, prices[1:]))
    assert 0 <= profit <= unlimited
    assert solve(k + 1, prices) >= profit
    assert solve(k, prices + [extra]) >= profit
    assert solve(k, [price + shift for price in prices]) == profit
    assert solve(k, [price * scale for price in prices]) == profit * scale
    assert solve(len(prices) // 2, prices) == unlimited
    assert solve(0, prices) == 0


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls(solve):
    assert solve(2, [3, 2, 6, 5, 0, 3]) == 7
    assert solve(0, [1, 9]) == 0
    assert solve(1, [5, 4, 3]) == 0
    assert solve(2, [3, 2, 6, 5, 0, 3]) == 7


@pytest.mark.parametrize("solve", IMPLS)
def test_large_unlimited_shortcut(solve):
    assert solve(10**9, [0, 1] * 50_000) == 50_000


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solver = module.Solution()
    assert solver.maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7
    assert solver.maxProfit(0, []) == 0


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
def test_documented_nonpositive_budget_extension(module):
    assert module.max_profit(-1, [1, 4, 2]) == 0
    assert module.max_profit(-1, []) == 0


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    root = Path(__file__).resolve().parents[1]
    path = root / "posts" / f"best_time_to_buy_sell_stock_iv_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
