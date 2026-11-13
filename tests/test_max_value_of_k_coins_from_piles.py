"""Check prefix knapsack against independent Cartesian-product enumeration."""

from copy import deepcopy
from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import max_value_of_k_coins_from_piles as original
import max_value_of_k_coins_from_piles_compressed as compressed
import max_value_of_k_coins_from_piles_exact_table as table

MODULES = (original, compressed, table)
ALTERNATIVES = (compressed, table)
IMPLS = [pytest.param(m.max_value_of_coins, id=m.__name__) for m in MODULES]
POSITIVE_PILES = st.lists(
    st.lists(st.integers(1, 30), min_size=1, max_size=4), min_size=1, max_size=4
)
SIGNED_PILES = st.lists(st.lists(st.integers(-20, 20), max_size=4), max_size=4)


def prefix_choice_oracle(piles, k):
    """Try each legal prefix length per pile, filtering for exact total count."""
    return max(
        sum(sum(pile[:take]) for pile, take in zip(piles, counts))
        for counts in product(*(range(len(pile) + 1) for pile in piles))
        if sum(counts) == k
    )


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("piles", "k", "expected"),
    [
        ([[1, 100, 3], [7, 8, 9]], 2, 101),
        ([[100], [100], [100], [100], [100], [100], [1, 1, 1, 1, 1, 1, 700]], 7, 706),
        ([], 0, 0),
        ([[], []], 0, 0),
        ([[5]], 0, 0),
        ([[5]], 1, 5),
        ([[1, 100]], 1, 1),
        ([[1, 100]], 2, 101),
        ([[1, 100], [50]], 2, 101),
        ([[10], [1]], 2, 11),
        ([[5], [4]], 2, 9),
        ([[2, 2], [2, 2]], 3, 6),
        ([[], [1, 9], []], 2, 10),
        ([[3, 2], [4]], 3, 9),
        ([[10**12, 10**12], [1]], 2, 2 * 10**12),
    ],
)
def test_examples_and_boundaries(solve, piles, k, expected):
    before = deepcopy(piles)
    result = solve(piles, k)
    assert type(result) is int
    assert result == expected
    assert piles == before


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_piles(solve):
    options = [[], [1], [2], [1, 1], [1, 2], [2, 1], [2, 2]]
    for count in range(4):
        for piles_tuple in product(options, repeat=count):
            piles = list(piles_tuple)
            for k in range(sum(map(len, piles)) + 1):
                assert solve(piles, k) == prefix_choice_oracle(piles, k), (piles, k)


@pytest.mark.parametrize("solve", IMPLS)
@given(piles=POSITIVE_PILES, data=st.data())
@settings(max_examples=150, deadline=None)
def test_positive_oracle_and_no_mutation(solve, piles, data):
    k = data.draw(st.integers(0, sum(map(len, piles))))
    before = deepcopy(piles)
    assert solve(piles, k) == prefix_choice_oracle(piles, k)
    assert piles == before


@pytest.mark.parametrize("solve", IMPLS)
@given(piles=POSITIVE_PILES, data=st.data(), shift=st.integers(0, 10), scale=st.integers(1, 5))
@settings(max_examples=100, deadline=None)
def test_positive_properties(solve, piles, data, shift, scale):
    total = sum(map(len, piles))
    k = data.draw(st.integers(0, total))
    result = solve(piles, k)
    assert solve(piles[::-1], k) == result  # Reorder piles, never their coins.
    assert solve(piles + [[100]], k) >= result
    assert solve([[v + shift for v in pile] for pile in piles], k) == result + k * shift
    assert solve([[v * scale for v in pile] for pile in piles], k) == result * scale
    assert solve(piles, total) == sum(map(sum, piles))
    if k < total:
        assert solve(piles, k + 1) > result


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
@given(piles=SIGNED_PILES, data=st.data())
@settings(max_examples=150, deadline=None)
def test_signed_exact_count_extension(module, piles, data):
    k = data.draw(st.integers(0, sum(map(len, piles))))
    before = deepcopy(piles)
    assert module.max_value_of_coins(piles, k) == prefix_choice_oracle(piles, k)
    assert piles == before


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda m: m.__name__)
def test_exact_count_and_invalid_budget(module):
    assert module.max_value_of_coins([[-5]], 1) == -5
    assert module.max_value_of_coins([[0], [-2]], 2) == -2
    for piles, k in [([], 1), ([[1]], 2), ([[1]], -1), ([], -1)]:
        with pytest.raises(ValueError):
            module.max_value_of_coins(piles, k)
    assert module.Solution().maxValueOfCoins([[1, 100], [50]], 2) == 101


@pytest.mark.parametrize("solve", IMPLS)
def test_scale_and_repeated_calls(solve):
    assert solve([[1]] * 1000, 1000) == 1000
    assert solve([[1] * 2000], 2000) == 2000
    assert solve([[1, 100], [50]], 2) == 101
    assert solve([], 0) == 0
    assert solve([[5]], 1) == 5


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"max_value_of_k_coins_from_piles_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
