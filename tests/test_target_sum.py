"""Verify sign-assignment counts by independent enumeration of sign vectors."""

from itertools import product
from math import comb
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import target_sum as original
import target_sum_subset_dp as subset
import target_sum_sparse_dp as sparse

MODULES = (original, subset, sparse)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]
SMALL_NUMS = st.lists(st.integers(0, 8), max_size=10)


def sign_oracle(nums, target):
    return sum(
        sum(sign * value for sign, value in zip(signs, nums)) == target
        for signs in product((-1, 1), repeat=len(nums))
    )


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([1, 1, 1, 1, 1], 3, 5), ([1], 1, 1), ([1], -1, 1),
        ([1], -3, 0), ([1], -2, 0), ([1], 3, 0),
        ([], 0, 1), ([], -2, 0), ([], 2, 0),
        ([0], 0, 2), ([0, 0, 0], 0, 8),
        ([0, 0, 1], 1, 4), ([0, 0, 1], -1, 4),
        ([1, 2, 3], 0, 2), ([1, 2], 0, 0),
        ([2, 2], 0, 2), ([2], 0, 0),
        ([1, 2], 3, 1), ([1, 2], -3, 1),
        ([0] * 20, 0, 2**20), ([1] * 20, 0, comb(20, 10)),
        ([1000], -1000, 1), ([1000], -1002, 0),
    ],
)
def test_examples_and_regressions(module, nums, target, expected):
    before = nums.copy()
    result = module.find_target_sum_ways(nums, target)
    assert type(result) is int
    assert result == expected
    assert nums == before


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_small_inputs(module):
    for length in range(5):
        for values in product(range(3), repeat=length):
            nums = list(values)
            for target in range(-sum(nums) - 2, sum(nums) + 3):
                assert module.find_target_sum_ways(nums, target) == sign_oracle(nums, target), (nums, target)


@pytest.mark.parametrize("module", IMPLS)
@given(nums=SMALL_NUMS, target=st.integers(-85, 85))
@settings(max_examples=200, deadline=None)
def test_independent_oracle(module, nums, target):
    before = nums.copy()
    assert module.find_target_sum_ways(nums, target) == sign_oracle(nums, target)
    assert nums == before


@pytest.mark.parametrize("module", IMPLS)
@given(nums=SMALL_NUMS, target=st.integers(-85, 85), scale=st.integers(1, 5))
@settings(max_examples=150, deadline=None)
def test_properties(module, nums, target, scale):
    solve = module.find_target_sum_ways
    result = solve(nums, target)
    assert result == solve(nums, -target)
    assert result == solve(nums[::-1], target)
    assert solve(nums + [0], target) == 2 * result
    assert solve([value * scale for value in nums], target * scale) == result
    assert 0 <= result <= 2 ** len(nums)
    if abs(target) > sum(nums) or (sum(nums) + target) % 2:
        assert result == 0


@pytest.mark.parametrize("module", IMPLS)
@given(nums=st.lists(st.integers(0, 4), max_size=7))
@settings(max_examples=100, deadline=None)
def test_counts_partition_all_expressions(module, nums):
    total = sum(nums)
    assert sum(module.find_target_sum_ways(nums, target) for target in range(-total, total + 1)) == 2 ** len(nums)


@pytest.mark.parametrize("module", (subset, sparse), ids=lambda module: module.__name__)
def test_wrappers_and_large_sparse_magnitudes(module):
    assert module.Solution().findTargetSumWays([1, 1, 1, 1, 1], 3) == 5
    assert module.find_target_sum_ways([10**12, 10**12], 2 * 10**12) == 1


@given(nums=st.lists(st.integers(-8, 8), max_size=9), target=st.integers(-75, 75))
@settings(max_examples=150, deadline=None)
def test_sparse_signed_extension(nums, target):
    before = nums.copy()
    assert sparse.find_target_sum_ways(nums, target) == sign_oracle(nums, target)
    assert nums == before


def test_subset_negative_value_policy():
    with pytest.raises(ValueError):
        subset.find_target_sum_ways([1, -1], 0)


@pytest.mark.parametrize("module", IMPLS)
def test_repeated_calls_and_large_counts(module):
    assert module.find_target_sum_ways([0] * 100, 0) == 2**100
    assert module.find_target_sum_ways([1] * 100, 0) == comb(100, 50)
    assert module.find_target_sum_ways([1], -3) == 0
    assert module.find_target_sum_ways([], 0) == 1
    assert module.find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"target_sum_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
