"""Verify Tribonacci with independent counting of compositions into 1, 2, 3."""

from math import comb
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import nth_tribonacci_number as original
import nth_tribonacci_number_dp_table as table
import nth_tribonacci_number_matrix as matrix

MODULES = (original, table, matrix)
ALTERNATIVES = (table, matrix)
IMPLS = [pytest.param(module.tribonacci, id=module.__name__) for module in MODULES]


def composition_oracle(n):
    """T[n] counts ordered compositions of n - 1; count by multiplicities."""
    if n == 0:
        return 0
    total = 0
    target = n - 1
    for threes in range(target // 3 + 1):
        remaining = target - 3 * threes
        for twos in range(remaining // 2 + 1):
            ones = remaining - 2 * twos
            parts = ones + twos + threes
            total += comb(parts, ones) * comb(twos + threes, twos)
    return total


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 4), (5, 7),
        (6, 13), (7, 24), (8, 44), (9, 81), (10, 149),
        (25, 1389537), (37, 2082876103), (38, 3831006429),
    ],
)
def test_known_values_and_boundaries(solve, n, expected):
    result = solve(n)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_indices_against_composition_oracle(solve):
    for n in range(101):
        assert solve(n) == composition_oracle(n), n


@pytest.mark.parametrize("solve", IMPLS)
@given(n=st.integers(0, 100))
@settings(max_examples=101, deadline=None)
def test_independent_oracle(solve, n):
    assert solve(n) == composition_oracle(n)


@pytest.mark.parametrize("solve", IMPLS)
@given(n=st.integers(0, 500))
@settings(max_examples=150, deadline=None)
def test_recurrence_and_growth(solve, n):
    result = solve(n)
    assert type(result) is int
    assert result >= 0
    assert solve(n + 3) == result + solve(n + 1) + solve(n + 2)
    if n >= 2:
        assert solve(n + 1) > result
        assert result <= 2 ** n


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls_and_large_exact_result(solve):
    expected = original.tribonacci(1000)
    assert solve(1000) == expected
    assert solve(37) == 2082876103
    assert solve(0) == 0
    assert solve(4) == 4
    assert solve(2) == 1
    assert solve(37) == 2082876103


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_negative_index_policy_and_wrapper(module):
    for n in (-1, -2, -100):
        with pytest.raises(ValueError):
            module.tribonacci(n)
    solution = module.Solution()
    assert solution.tribonacci(0) == 0
    assert solution.tribonacci(4) == 4
    assert solution.tribonacci(37) == 2082876103


def test_matrix_large_index():
    assert matrix.tribonacci(10_000) == original.tribonacci(10_000)


@pytest.mark.parametrize("exponent", [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 63, 64])
def test_matrix_exponent_bit_boundaries(exponent):
    n = exponent + 2
    assert matrix.tribonacci(n) == composition_oracle(n)


def test_matrix_multiplication_preserves_inputs():
    first = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
    before = [row.copy() for row in first]
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert matrix._multiply(first, identity) == first
    assert matrix._multiply(identity, first) == first
    assert matrix._multiply(first, first) == [[2, 2, 1], [1, 1, 1], [1, 0, 0]]
    assert first == before
    assert identity == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"nth_tribonacci_number_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
