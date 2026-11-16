"""Verify circular robbery with independently enumerated legal subsets."""

from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import house_robber as linear
import house_robber_ii as original
import house_robber_ii_range_dp as ranges
import house_robber_ii_dp_table as table

MODULES = (original, ranges, table)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]
SMALL_INPUTS = st.lists(st.integers(0, 400), max_size=12)


def circular_oracle(nums):
    """Enumerate index subsets, rejecting every circular neighbor pair."""
    best = 0
    n = len(nums)
    for mask in range(1 << n):
        chosen = [index for index in range(n) if mask & (1 << index)]
        if n > 1 and any((index + 1) % n in chosen for index in chosen):
            continue
        best = max(best, sum(nums[index] for index in chosen))
    return best


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("nums", "expected"),
    [
        ([], 0), ([0], 0), ([7], 7), ([1, 2], 2), ([2, 1], 2),
        ([5, 5], 5), ([2, 3, 2], 3), ([1, 2, 3, 1], 4),
        ([1, 2, 3], 3), ([10, 1, 1, 10], 11),
        ([2, 1, 1, 2], 3), ([5] * 9, 20), ([5] * 10, 25),
        ([0] * 100, 0), ([400] * 100, 20_000),
        ([0, 400] * 50, 20_000), ([400, 0] * 50, 20_000),
        ([10**12, 1, 10**12, 1], 2 * 10**12),
    ],
)
def test_examples_and_boundaries(module, nums, expected):
    before = nums.copy()
    result = module.rob(nums)
    assert type(result) is int
    assert result == expected
    assert nums == before


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_small_inputs(module):
    for size in range(8):
        for values in product(range(3), repeat=size):
            nums = list(values)
            assert module.rob(nums) == circular_oracle(nums), nums


@pytest.mark.parametrize("module", IMPLS)
@given(nums=SMALL_INPUTS)
@settings(max_examples=200, deadline=None)
def test_independent_oracle_and_nonmutation(module, nums):
    before = nums.copy()
    assert module.rob(nums) == circular_oracle(nums)
    assert nums == before


@pytest.mark.parametrize("module", IMPLS)
@given(nums=SMALL_INPUTS, factor=st.integers(0, 10), data=st.data())
@settings(max_examples=150, deadline=None)
def test_properties(module, nums, factor, data):
    result = module.rob(nums)
    assert module.rob(nums[::-1]) == result
    assert module.rob([value * factor for value in nums]) == result * factor
    assert max(nums, default=0) <= result <= linear.rob(nums)
    # A zero between the endpoints breaks the circular conflict for free.
    assert module.rob(nums + [0]) == linear.rob(nums)
    if nums:
        pivot = data.draw(st.integers(0, len(nums) - 1))
        assert module.rob(nums[pivot:] + nums[:pivot]) == result
        changed = nums.copy()
        changed[pivot] += 5
        assert result <= module.rob(changed) <= result + 5


@pytest.mark.parametrize("module", IMPLS)
def test_repeated_calls_and_long_input(module):
    assert module.rob([1] * 10_000) == 5000
    assert module.rob([1] * 10_001) == 5000
    nums = [2, 3, 2]
    assert module.rob(nums) == 3
    nums[:] = [10, 1, 1, 10]
    assert module.rob(nums) == 11
    assert module.rob([]) == 0
    assert module.rob([2, 3, 2]) == 3


@pytest.mark.parametrize("module", (ranges, table), ids=lambda module: module.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    assert solution.rob([2, 3, 2]) == 3
    assert solution.rob([]) == 0
    assert solution.rob([7]) == 7


def test_range_version_does_not_slice_input():
    class NoSlices(list):
        def __getitem__(self, index):
            assert not isinstance(index, slice)
            return super().__getitem__(index)

    assert ranges.rob(NoSlices([10, 1, 1, 10])) == 11


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"house_robber_ii_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
