"""Shared correctness checks for all House Robber implementations."""

from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import house_robber
import house_robber_dp_table
import house_robber_top_down

MODULES = (house_robber, house_robber_dp_table, house_robber_top_down)
IMPLEMENTATIONS = [pytest.param(module.rob, id=module.__name__) for module in MODULES]
SMALL_INPUTS = st.lists(st.integers(min_value=0, max_value=400), max_size=12)


def subset_oracle(nums: list[int]) -> int:
    """Enumerate all subsets, rejecting masks with adjacent selected bits."""
    best = 0
    for mask in range(1 << len(nums)):
        if mask & (mask >> 1):
            continue
        total = sum(value for i, value in enumerate(nums) if mask & (1 << i))
        best = max(best, total)
    return best


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0),
        ([0], 0),
        ([7], 7),
        ([1, 2], 2),
        ([2, 1], 2),
        ([5, 5], 5),
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([2, 1, 1, 2], 4),
        ([1, 3, 1, 3, 100], 103),
        ([10, 1, 1, 10], 20),
        ([0] * 100, 0),
        ([400] * 100, 20_000),
        ([5] * 9, 25),
        ([0, 400] * 50, 20_000),
        ([400, 0] * 50, 20_000),
    ],
)
def test_examples_and_boundaries(rob, nums, expected):
    original = nums.copy()
    assert rob(nums) == expected
    assert nums == original


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
def test_exhaustive_small_inputs(rob):
    for size in range(7):
        for values in product(range(3), repeat=size):
            nums = list(values)
            assert rob(nums) == subset_oracle(nums), nums


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
@given(nums=SMALL_INPUTS)
@settings(max_examples=150, deadline=None)
def test_independent_oracle_and_nonmutation(rob, nums):
    original = nums.copy()
    result = rob(nums)
    assert type(result) is int
    assert result == subset_oracle(nums)
    assert nums == original


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
@given(nums=st.lists(st.integers(0, 400), max_size=100))
@settings(max_examples=100, deadline=None)
def test_reversal_padding_and_bounds(rob, nums):
    result = rob(nums)
    assert rob(nums[::-1]) == result
    assert rob([0] + nums + [0]) == result
    assert max(sum(nums[::2]), sum(nums[1::2])) <= result <= sum(nums)


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
@given(nums=SMALL_INPUTS, factor=st.integers(min_value=0, max_value=10))
@settings(max_examples=100, deadline=None)
def test_nonnegative_scaling(rob, nums, factor):
    assert rob([factor * value for value in nums]) == factor * rob(nums)


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
@given(left=SMALL_INPUTS, right=SMALL_INPUTS)
@settings(max_examples=100, deadline=None)
def test_zero_separator_makes_segments_independent(rob, left, right):
    assert rob(left + [0] + right) == rob(left) + rob(right)


@pytest.mark.parametrize("rob", IMPLEMENTATIONS)
def test_repeated_calls_and_changed_input(rob):
    nums = [2, 7, 9, 3, 1]
    assert rob(nums) == 12
    assert rob([1]) == 1
    nums[:] = [100, 1, 1, 100]
    assert rob(nums) == 200
    assert rob([]) == 0


@pytest.mark.parametrize("module", MODULES, ids=lambda module: module.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    nums = [2, 7, 9, 3, 1]
    assert solution.rob(nums) == 12
    assert nums == [2, 7, 9, 3, 1]
    assert solution.rob([]) == 0
    assert solution.rob([4]) == 4


@pytest.mark.parametrize(
    "rob",
    [
        pytest.param(house_robber.rob, id="rolling"),
        pytest.param(house_robber_dp_table.rob, id="table"),
    ],
)
def test_iterative_implementations_handle_long_inputs(rob):
    assert rob([1] * 10_000) == 5_000
