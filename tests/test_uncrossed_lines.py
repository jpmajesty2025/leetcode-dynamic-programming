"""Verify ordered matching via independently enumerated subsequence sets."""

from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import uncrossed_lines as original
import uncrossed_lines_rolling_dp as rolling
import uncrossed_lines_sparse as sparse
import longest_common_subsequence as lcs

MODULES = (original, rolling, sparse)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]
SMALL = st.lists(st.integers(-2, 3), max_size=8)


def subsequences(values):
    return {
        tuple(value for index, value in enumerate(values) if mask & (1 << index))
        for mask in range(1 << len(values))
    }


def oracle(first, second):
    return max(map(len, subsequences(first) & subsequences(second)))


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ([], [], 0), ([], [1], 0), ([1], [], 0),
        ([1], [1], 1), ([1], [2], 0),
        ([1, 4, 2], [1, 2, 4], 2),
        ([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2], 3),
        ([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1], 2),
        ([1], [1, 1, 1], 1), ([1, 1, 1], [1], 1),
        ([1, 2], [2, 1], 1), ([1, 2, 3], [3, 2, 1], 1),
        ([1, 1, 2], [1, 2, 1], 2),
        ([-1, 0, -2], [0, -2], 2),
        ([10**30, -10**30], [10**30, -10**30], 2),
        ([1, 2, 3], [4, 5, 6], 0),
    ],
)
def test_examples_and_boundaries(module, first, second, expected):
    before_first, before_second = first.copy(), second.copy()
    result = module.max_uncrossed_lines(first, second)
    assert type(result) is int
    assert result == expected
    assert first == before_first and second == before_second


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_binary_arrays(module):
    arrays = [list(values) for size in range(5) for values in product(range(2), repeat=size)]
    enumerated = {tuple(values): subsequences(values) for values in arrays}
    for first in arrays:
        for second in arrays:
            expected = max(map(len, enumerated[tuple(first)] & enumerated[tuple(second)]))
            assert module.max_uncrossed_lines(first, second) == expected, (first, second)


@pytest.mark.parametrize("module", IMPLS)
@given(first=SMALL, second=SMALL)
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_nonmutation(module, first, second):
    before_first, before_second = first.copy(), second.copy()
    assert module.max_uncrossed_lines(first, second) == oracle(first, second)
    assert first == before_first and second == before_second


@pytest.mark.parametrize("module", IMPLS)
@given(first=SMALL, second=SMALL, value=st.integers(-2, 3))
@settings(max_examples=150, deadline=None)
def test_properties(module, first, second, value):
    solve = module.max_uncrossed_lines
    result = solve(first, second)
    assert result == solve(second, first)
    assert result == solve(first[::-1], second[::-1])
    assert solve(first, first) == len(first)
    assert 0 <= result <= min(len(first), len(second))
    assert solve(first + [value], second + [value]) == result + 1
    assert result <= solve(first + [value], second) <= result + 1
    assert solve([3 * v + 7 for v in first], [3 * v + 7 for v in second]) == result
    # Existing string LCS is a consistency check, not the independent oracle.
    assert result == lcs.longest_common_subsequence(
        "".join(chr(v + 100) for v in first),
        "".join(chr(v + 100) for v in second),
    )


@pytest.mark.parametrize("module", IMPLS)
def test_scale_repeated_calls_and_aliased_inputs(module):
    assert module.max_uncrossed_lines([1] * 500, [1] * 500) == 500
    assert module.max_uncrossed_lines(list(range(500)), list(reversed(range(500)))) == 1
    values = [1, 4, 2]
    assert module.max_uncrossed_lines(values, values) == 3
    assert values == [1, 4, 2]
    assert module.max_uncrossed_lines([1, 4, 2], [1, 2, 4]) == 2
    assert module.max_uncrossed_lines([], []) == 0
    assert module.max_uncrossed_lines([1], [1, 1]) == 1


@pytest.mark.parametrize("module", (rolling, sparse), ids=lambda module: module.__name__)
def test_solution_wrapper_and_unequal_lengths(module):
    assert module.Solution().maxUncrossedLines([1, 4, 2], [1, 2, 4]) == 2
    assert module.Solution().maxUncrossedLines([], []) == 0
    assert module.max_uncrossed_lines([1] * 100_000, [1]) == 1
    assert module.max_uncrossed_lines([1], [1] * 100_000) == 1


def test_sparse_large_sparse_matching():
    values = list(range(30_000))
    assert sparse.max_uncrossed_lines(values, values) == 30_000
    assert sparse.max_uncrossed_lines(values, list(range(30_000, 60_000))) == 0


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"uncrossed_lines_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
