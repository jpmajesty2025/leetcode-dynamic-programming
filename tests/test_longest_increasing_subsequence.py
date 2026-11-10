"""Verify LIS length independently of either implementation's recurrence."""

from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import longest_increasing_subsequence as binary_search
import longest_increasing_subsequence_dp as quadratic

MODULES = (binary_search, quadratic)
IMPLS = [pytest.param(m.length_of_lis, id=m.__name__) for m in MODULES]
SMALL_INPUTS = st.lists(st.integers(-20, 20), max_size=12)


def subsequence_oracle(nums):
    """Enumerate all index subsets and check strict ordering directly."""
    best = 0
    for mask in range(1 << len(nums)):
        selected = [value for i, value in enumerate(nums) if mask & (1 << i)]
        if all(a < b for a, b in zip(selected, selected[1:])):
            best = max(best, len(selected))
    return best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([7], 1),
        ([1, 2], 2),
        ([2, 1], 1),
        ([2, 2], 1),
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([0, 1, 0, 3, 2, 3], 4),
        ([7] * 10, 1),
        ([-4, -3, -2, -1], 4),
        ([-1, -2, -3], 1),
        ([-2, 0, -1, 1], 3),
        ([1, 2, 3, 0], 3),
        ([1, 3, 5, 2, 4, 6], 4),
        ([2, 2, 1, 1, 3, 3], 2),
        ([3, 5, 6, 2, 4, 1], 3),
        ([-10_000, 10_000], 2),
        (list(range(2500)), 2500),
        (list(range(2500, 0, -1)), 1),
    ],
)
def test_examples_and_boundaries(solve, nums, expected):
    original = nums.copy()
    assert solve(nums) == expected
    assert nums == original


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    for size in range(8):
        for values in product((-1, 0, 1), repeat=size):
            nums = list(values)
            assert solve(nums) == subsequence_oracle(nums), nums


@pytest.mark.parametrize("solve", IMPLS)
@given(nums=SMALL_INPUTS)
@settings(max_examples=150, deadline=None)
def test_oracle_and_nonmutation(solve, nums):
    original = nums.copy()
    result = solve(nums)
    assert type(result) is int
    assert result == subsequence_oracle(nums)
    assert nums == original


@pytest.mark.parametrize("solve", IMPLS)
@given(nums=SMALL_INPUTS, value=st.integers(-30, 30))
@settings(max_examples=100, deadline=None)
def test_appending_changes_length_by_at_most_one(solve, nums, value):
    before = solve(nums)
    assert before <= solve(nums + [value]) <= before + 1
    assert solve(nums + [max(nums, default=0) + 1]) == before + 1


@pytest.mark.parametrize("solve", IMPLS)
@given(nums=SMALL_INPUTS, scale=st.integers(1, 10), shift=st.integers(-100, 100))
@settings(max_examples=100, deadline=None)
def test_strictly_increasing_transformation(solve, nums, scale, shift):
    assert solve([scale * x + shift for x in nums]) == solve(nums)


@pytest.mark.parametrize("solve", IMPLS)
@given(nums=SMALL_INPUTS)
@settings(max_examples=100, deadline=None)
def test_adjacent_duplication_preserves_strict_lis(solve, nums):
    assert solve([x for value in nums for x in (value, value)]) == solve(nums)


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls_and_changed_input(solve):
    nums = [1, 2, 3]
    assert solve(nums) == 3
    assert solve([7, 7]) == 1
    nums[:] = [3, 2, 1]
    assert solve(nums) == 1
    assert solve([]) == 0


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    assert solution.lengthOfLIS(nums) == 4
    assert nums == [10, 9, 2, 5, 3, 7, 101, 18]
    assert solution.lengthOfLIS([]) == 0


def test_binary_search_large_inputs():
    assert binary_search.length_of_lis(list(range(100_000))) == 100_000
    assert binary_search.length_of_lis(list(range(100_000, 0, -1))) == 1
    assert binary_search.length_of_lis([5] * 100_000) == 1
