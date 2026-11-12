"""Shared LCS checks using independently enumerated subsequence sets."""

from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import longest_common_subsequence as compressed
import longest_common_subsequence_dp_table as table

MODULES = (compressed, table)
IMPLS = [pytest.param(m.longest_common_subsequence, id=m.__name__) for m in MODULES]
SMALL_TEXT = st.text(alphabet="abc", max_size=8)


def subsequences(text):
    return {
        "".join(c for i, c in enumerate(text) if mask & (1 << i))
        for mask in range(1 << len(text))
    }


def subsequence_oracle(first, second):
    """Enumerate index subsets, then intersect resulting strings; no DP."""
    return max(map(len, subsequences(first) & subsequences(second)))


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ("", "", 0),
        ("", "abc", 0),
        ("abc", "", 0),
        ("a", "a", 1),
        ("a", "b", 0),
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("aaa", "aa", 2),
        ("a", "aaaa", 1),
        ("aaaa", "a", 1),
        ("abc", "cba", 1),
        ("AGGTAB", "GXTXAYB", 4),
        ("abcbdab", "bdcaba", 4),
        ("a猫b🙂", "猫🙂", 2),
        ("a" * 1000, "a" * 1000, 1000),
        ("a" * 1000, "b" * 1000, 0),
        ("ab" * 500, "ba" * 500, 999),
    ],
)
def test_examples_and_boundaries(solve, first, second, expected):
    assert type(solve(first, second)) is int
    assert solve(first, second) == expected


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_binary_strings(solve):
    strings = ["".join(chars) for n in range(5) for chars in product("ab", repeat=n)]
    enumerated = {text: subsequences(text) for text in strings}
    for first in strings:
        for second in strings:
            expected = max(map(len, enumerated[first] & enumerated[second]))
            assert solve(first, second) == expected, (first, second)


@pytest.mark.parametrize("solve", IMPLS)
@given(first=SMALL_TEXT, second=SMALL_TEXT)
@settings(max_examples=150, deadline=None)
def test_independent_oracle(solve, first, second):
    assert solve(first, second) == subsequence_oracle(first, second)


@pytest.mark.parametrize("solve", IMPLS)
@given(first=SMALL_TEXT, second=SMALL_TEXT)
@settings(max_examples=100, deadline=None)
def test_symmetry_identity_bounds_and_reversal(solve, first, second):
    result = solve(first, second)
    assert result == solve(second, first)
    assert result == solve(first[::-1], second[::-1])
    assert solve(first, first) == len(first)
    assert 0 <= result <= min(len(first), len(second))


@pytest.mark.parametrize("solve", IMPLS)
@given(first=SMALL_TEXT, second=SMALL_TEXT, character=st.sampled_from("abc"))
@settings(max_examples=100, deadline=None)
def test_common_suffix_and_single_append(solve, first, second, character):
    result = solve(first, second)
    assert solve(first + character, second + character) == result + 1
    assert result <= solve(first + character, second) <= result + 1


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls(solve):
    assert solve("abcde", "ace") == 3
    assert solve("a", "aaaa") == 1
    assert solve("abc", "def") == 0
    assert solve("", "") == 0
    assert solve("abcde", "ace") == 3


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    assert solution.longestCommonSubsequence("abcde", "ace") == 3
    assert solution.longestCommonSubsequence("", "abc") == 0


def test_compressed_very_unequal_lengths():
    assert compressed.longest_common_subsequence("a" * 100_000, "a") == 1
    assert compressed.longest_common_subsequence("a", "a" * 100_000) == 1
