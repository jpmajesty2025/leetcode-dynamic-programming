"""Check fixed-difference subsequences by enumerating index subsets."""

from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import longest_arithmetic_subsequence_of_given_difference as original
import longest_arithmetic_subsequence_of_given_difference_dp_table as table
import longest_arithmetic_subsequence_of_given_difference_compressed as compressed

MODULES = (original, table, compressed)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]
SMALL = st.lists(st.integers(-10, 10), max_size=10)


def subset_oracle(arr, difference):
    best = 0
    for mask in range(1 << len(arr)):
        sequence = [value for index, value in enumerate(arr) if mask & (1 << index)]
        if all(b - a == difference for a, b in zip(sequence, sequence[1:])):
            best = max(best, len(sequence))
    return best


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("arr", "difference", "expected"),
    [
        ([], 0, 0), ([], 7, 0), ([5], 0, 1), ([5], -3, 1),
        ([1, 2, 3, 4], 1, 4), ([1, 3, 5, 7], 1, 1),
        ([1, 5, 7, 8, 5, 3, 4, 2, 1], -2, 4),
        ([3, 2, 1], 1, 1), ([3, 2, 1], -1, 3),
        ([7, 7, 7, 7], 0, 4), ([7, 7, 7], 1, 1),
        ([1, 2, 1, 2, 3], 1, 3), ([1, 2, 3, 2, 3, 4], 1, 4),
        ([1, 2, 1, 1, 2], 0, 3), ([-5, -3, -1, 1], 2, 4),
        ([0, 100, 1, 100, 2, 3], 1, 4),
        ([10**30, 0, 10**30 + 7, 10**30 + 14], 7, 3),
    ],
)
def test_examples_and_boundaries(module, arr, difference, expected):
    before = arr.copy()
    result = module.longest_subsequence(arr, difference)
    assert type(result) is int
    assert result == expected
    assert arr == before


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_small_inputs(module):
    for size in range(6):
        for values in product((-1, 0, 1), repeat=size):
            arr = list(values)
            for difference in range(-2, 3):
                assert module.longest_subsequence(arr, difference) == subset_oracle(arr, difference), (arr, difference)


@pytest.mark.parametrize("module", IMPLS)
@given(arr=SMALL, difference=st.integers(-15, 15))
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_nonmutation(module, arr, difference):
    before = arr.copy()
    assert module.longest_subsequence(arr, difference) == subset_oracle(arr, difference)
    assert arr == before


@pytest.mark.parametrize("module", IMPLS)
@given(arr=SMALL, difference=st.integers(-15, 15), shift=st.integers(-100, 100), scale=st.integers(1, 5), extra=st.integers(-10, 10))
@settings(max_examples=150, deadline=None)
def test_properties(module, arr, difference, shift, scale, extra):
    solve = module.longest_subsequence
    result = solve(arr, difference)
    assert 0 <= result <= len(arr)
    assert result >= bool(arr)
    assert solve([v + shift for v in arr], difference) == result
    assert solve([v * scale for v in arr], difference * scale) == result
    assert solve([-v for v in arr], -difference) == result
    assert solve(arr[::-1], -difference) == result
    assert result <= solve(arr + [extra], difference) <= result + 1
    assert solve(arr, 0) == max((arr.count(v) for v in arr), default=0)


@pytest.mark.parametrize("module", IMPLS)
def test_repeated_calls(module):
    arr = [1, 2, 3]
    assert module.longest_subsequence(arr, 1) == 3
    arr[:] = [3, 2, 1]
    assert module.longest_subsequence(arr, 1) == 1
    assert module.longest_subsequence([], 0) == 0
    assert module.longest_subsequence([7, 7], 0) == 2


@pytest.mark.parametrize("module", (table, compressed), ids=lambda module: module.__name__)
def test_solution_wrapper(module):
    assert module.Solution().longestSubsequence([1, 2, 3], 1) == 3
    assert module.Solution().longestSubsequence([], 0) == 0


@pytest.mark.parametrize("module", (original, compressed), ids=lambda module: module.__name__)
def test_large_inputs(module):
    assert module.longest_subsequence(list(range(100_000)), 1) == 100_000
    assert module.longest_subsequence([7] * 100_000, 0) == 100_000
    assert module.longest_subsequence(list(range(100_000)), -1) == 1


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    root = Path(__file__).resolve().parents[1]
    path = root / "posts" / f"longest_arithmetic_subsequence_of_given_difference_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
