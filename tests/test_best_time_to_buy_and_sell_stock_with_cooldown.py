"""Verify cooldown trading using independently enumerated legal endpoints."""

from itertools import combinations, product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import best_time_to_buy_and_sell_stock_with_cooldown as original
import best_time_to_buy_and_sell_stock_with_cooldown_lagged as lagged
import best_time_to_buy_and_sell_stock_with_cooldown_dp_table as table

MODULES = (original, lagged, table)
ALTERNATIVES = (lagged, table)
IMPLS = [pytest.param(m.max_profit, id=m.__name__) for m in MODULES]
SMALL_PRICES = st.lists(st.integers(0, 30), max_size=9)


def endpoint_oracle(prices):
    """Enumerate buy/sell days, excluding buys the day after a sale; no DP."""
    best = 0
    for trades in range(1, (len(prices) + 1) // 3 + 1):
        for days in combinations(range(len(prices)), 2 * trades):
            if any(days[i] < days[i - 1] + 2 for i in range(2, len(days), 2)):
                continue
            best = max(
                best,
                sum(prices[days[i + 1]] - prices[days[i]] for i in range(0, len(days), 2)),
            )
    return best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("prices", "expected"),
    [
        ([], 0),
        ([1], 0),
        ([0], 0),
        ([1, 2], 1),
        ([2, 1], 0),
        ([2, 2], 0),
        ([1, 2, 3, 0, 2], 3),
        ([1, 2, 0, 2], 2),
        ([1, 2, 0, 0, 2], 3),
        ([1, 2, 3], 2),
        ([1, 4, 2], 3),
        ([5, 4, 3, 2, 1], 0),
        ([5, 5, 5, 5], 0),
        ([0, 0, 0], 0),
        ([0, 5, 0, 5], 5),
        ([0, 5, 0, 0, 5], 10),
        ([6, 1, 6, 4, 3, 0, 2], 7),
        ([2, 1, 4, 5, 2, 9, 7], 10),
        ([0, 10**12, 0, 0, 10**12], 2 * 10**12),
    ],
)
def test_examples_and_boundaries(solve, prices, expected):
    before = prices.copy()
    result = solve(prices)
    assert type(result) is int
    assert result == expected
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for n in range(8):
        for values in product(range(3), repeat=n):
            prices = list(values)
            assert solve(prices) == endpoint_oracle(prices), prices


@pytest.mark.parametrize("solve", IMPLS)
@given(prices=SMALL_PRICES)
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_nonmutation(solve, prices):
    before = prices.copy()
    assert solve(prices) == endpoint_oracle(prices)
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
@given(
    prices=SMALL_PRICES,
    shift=st.integers(0, 100),
    scale=st.integers(0, 5),
    extra=st.integers(0, 30),
)
@settings(max_examples=150, deadline=None)
def test_profit_properties(solve, prices, shift, scale, extra):
    profit = solve(prices)
    unlimited = sum(max(b - a, 0) for a, b in zip(prices, prices[1:]))
    assert 0 <= profit <= unlimited
    assert solve([p + shift for p in prices]) == profit
    assert solve([p * scale for p in prices]) == profit * scale
    assert solve(prices + [extra]) >= profit
    assert solve(sorted(prices)) == (max(prices) - min(prices) if prices else 0)
    assert solve(sorted(prices, reverse=True)) == 0


@pytest.mark.parametrize("solve", IMPLS)
def test_scale_and_repeated_calls(solve):
    assert solve([0, 5, 0] * 20_000) == 100_000
    assert solve(list(range(50_000))) == 49_999
    assert solve([1, 2, 3, 0, 2]) == 3
    assert solve([]) == 0
    assert solve([5, 4, 3]) == 0
    assert solve([1, 2, 3, 0, 2]) == 3


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    assert solution.maxProfit([1, 2, 3, 0, 2]) == 3
    assert solution.maxProfit([]) == 0
    assert solution.maxProfit([1, 2]) == 1


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    root = Path(__file__).resolve().parents[1]
    path = root / "posts" / f"best_time_to_buy_and_sell_stock_with_cooldown_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
