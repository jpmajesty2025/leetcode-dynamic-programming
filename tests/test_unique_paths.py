"""Verify grid DP and combinatorial counting with independent move words."""

from itertools import product
from math import comb
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import unique_paths as original
import unique_paths_rolling_dp as rolling
import unique_paths_combinatorial as combinatorial

MODULES = (original, rolling, combinatorial)
ALTERNATIVES = (rolling, combinatorial)
IMPLS = [pytest.param(module.unique_paths, id=module.__name__) for module in MODULES]


def move_word_oracle(m, n):
    """Enumerate all right/down words and count those reaching the target."""
    return sum(
        moves.count("D") == m - 1
        for moves in product("RD", repeat=m + n - 2)
    )


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("m", "n", "expected"),
    [
        (1, 1, 1),
        (1, 10, 1),
        (10, 1, 1),
        (2, 2, 2),
        (3, 2, 3),
        (3, 7, 28),
        (7, 3, 28),
        (3, 3, 6),
        (4, 4, 20),
        (2, 100, 100),
        (100, 2, 100),
        (10, 10, 48620),
        (17, 17, 601080390),
        (18, 18, 2333606220),  # Beyond the prompt's result cap; Python is exact.
        (100, 100, comb(198, 99)),
    ],
)
def test_examples_and_boundaries(solve, m, n, expected):
    result = solve(m, n)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_grids(solve):
    for m in range(1, 7):
        for n in range(1, 7):
            assert solve(m, n) == move_word_oracle(m, n), (m, n)


@pytest.mark.parametrize("solve", IMPLS)
@given(m=st.integers(1, 6), n=st.integers(1, 6))
@settings(max_examples=50, deadline=None)
def test_move_enumeration_oracle(solve, m, n):
    assert solve(m, n) == move_word_oracle(m, n)


@pytest.mark.parametrize("solve", IMPLS)
@given(m=st.integers(1, 100), n=st.integers(1, 100))
@settings(max_examples=150, deadline=None)
def test_binomial_reference_symmetry_and_boundaries(solve, m, n):
    result = solve(m, n)
    assert result == comb(m + n - 2, m - 1)
    assert result == solve(n, m)
    assert result >= 1
    assert solve(1, n) == solve(m, 1) == 1
    assert solve(m + 1, n) >= result
    assert solve(m, n + 1) >= result
    if m > 1 and n > 1:
        assert result == solve(m - 1, n) + solve(m, n - 1)


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls(solve):
    assert solve(3, 7) == 28
    assert solve(1, 1) == 1
    assert solve(2, 2) == 2
    assert solve(3, 7) == 28


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
@pytest.mark.parametrize(("m", "n"), [(0, 1), (1, 0), (0, 0), (-1, 3), (3, -1)])
def test_nonpositive_dimension_policy(module, m, n):
    with pytest.raises(ValueError):
        module.unique_paths(m, n)


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_solution_wrapper_and_long_thin_grids(module):
    assert module.Solution().uniquePaths(3, 7) == 28
    assert module.unique_paths(1, 10**9) == 1
    assert module.unique_paths(10**9, 1) == 1
    assert module.unique_paths(2, 100_000) == 100_000
    assert module.unique_paths(100_000, 2) == 100_000


def test_combinatorial_large_grid():
    assert combinatorial.unique_paths(1000, 1000) == comb(1998, 999)
    assert combinatorial.unique_paths(2, 10**12) == 10**12


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"unique_paths_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
