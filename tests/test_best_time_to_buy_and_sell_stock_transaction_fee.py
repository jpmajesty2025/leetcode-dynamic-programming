"""Check fee-aware trading against independent buy/sell endpoint enumeration."""

from itertools import combinations, product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import best_time_to_buy_and_sell_stock_transaction_fee as original
import best_time_to_buy_and_sell_stock_transaction_fee_dp as dp
import best_time_to_buy_and_sell_stock_transaction_fee_greedy as greedy

MODULES = (original, dp, greedy)
ALTERNATIVES = (dp, greedy)
IMPLS = [pytest.param(m.max_profit, id=m.__name__) for m in MODULES]
SMALL_PRICES = st.lists(st.integers(0, 30), max_size=9)


def endpoint_oracle(prices, fee):
    """Enumerate all strictly ordered buy/sell endpoints, including no trades."""
    best = 0
    for trades in range(1, len(prices) // 2 + 1):
        for days in combinations(range(len(prices)), 2 * trades):
            value = sum(
                prices[days[i + 1]] - prices[days[i]] - fee
                for i in range(0, len(days), 2)
            )
            best = max(best, value)
    return best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("prices", "fee", "expected"),
    [
        ([], 0, 0),
        ([], 5, 0),
        ([5], 2, 0),
        ([0], 0, 0),
        ([1, 3, 2, 8, 4, 9], 2, 8),
        ([1, 3, 7, 5, 10, 3], 3, 6),
        ([1, 4], 2, 1),
        ([1, 3], 2, 0),
        ([1, 2], 5, 0),
        ([5, 4, 3, 2], 0, 0),
        ([5, 5, 5, 5], 2, 0),
        ([1, 4, 7, 10], 2, 7),
        ([1, 5, 4, 8], 2, 5),
        ([1, 5, 1, 5], 2, 4),
        ([1, 5, 3, 8], 2, 5),
        ([1, 5, 2, 8], 2, 6),
        ([1, 3, 2, 8, 4, 9], 0, 13),
        ([0, 5, 0, 5], 1, 8),
        ([0, 0, 0], 0, 0),
        ([0, 10**12, 0, 10**12], 1, 2 * 10**12 - 2),
        ([1, 10, 2, 9], 10**12, 0),
    ],
)
def test_examples_and_boundaries(solve, prices, fee, expected):
    before = prices.copy()
    result = solve(prices, fee)
    assert type(result) is int
    assert result == expected
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for n in range(7):
        for values in product(range(3), repeat=n):
            prices = list(values)
            for fee in range(4):
                assert solve(prices, fee) == endpoint_oracle(prices, fee), (prices, fee)


@pytest.mark.parametrize("solve", IMPLS)
@given(prices=SMALL_PRICES, fee=st.integers(0, 40))
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_nonmutation(solve, prices, fee):
    before = prices.copy()
    assert solve(prices, fee) == endpoint_oracle(prices, fee)
    assert prices == before


@pytest.mark.parametrize("solve", IMPLS)
@given(
    prices=SMALL_PRICES,
    fee=st.integers(0, 30),
    extra_fee=st.integers(0, 10),
    shift=st.integers(0, 100),
    scale=st.integers(0, 5),
    extra_price=st.integers(0, 30),
)
@settings(max_examples=150, deadline=None)
def test_profit_properties(solve, prices, fee, extra_fee, shift, scale, extra_price):
    profit = solve(prices, fee)
    unlimited = sum(max(b - a, 0) for a, b in zip(prices, prices[1:]))
    assert 0 <= profit <= unlimited
    assert solve(prices, 0) == unlimited
    assert solve(prices, fee + extra_fee) <= profit
    assert solve([p + shift for p in prices], fee) == profit
    assert solve([p * scale for p in prices], fee * scale) == profit * scale
    assert solve(prices + [extra_price], fee) >= profit
    if prices:
        assert solve(prices, max(prices) - min(prices)) == 0


@pytest.mark.parametrize("solve", IMPLS)
def test_scale_and_repeated_calls(solve):
    prices = [1, 5] * 25_000
    assert solve(prices, 2) == 50_000
    assert solve(list(range(50_000)), 2) == 49_997
    assert solve([1, 3, 2, 8, 4, 9], 2) == 8
    assert solve([], 0) == 0
    assert solve([5, 4, 3], 1) == 0
    assert solve([1, 3, 2, 8, 4, 9], 2) == 8


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
def test_wrapper_and_negative_fee_policy(module):
    assert module.Solution().maxProfit([1, 3, 2, 8, 4, 9], 2) == 8
    assert module.Solution().maxProfit([], 0) == 0
    for prices in ([], [5], [1, 4]):
        with pytest.raises(ValueError):
            module.max_profit(prices, -1)


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    root = Path(__file__).resolve().parents[1]
    path = root / "posts" / f"best_time_to_buy_and_sell_stock_transaction_fee_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
