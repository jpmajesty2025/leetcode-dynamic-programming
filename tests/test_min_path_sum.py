"""Verify weighted grid DP by enumerating move-position combinations."""

from copy import deepcopy
from itertools import combinations, product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import min_path_sum as original
import min_path_sum_rolling_dp as rolling
import min_path_sum_in_place as in_place

MODULES = (original, rolling, in_place)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]


def path_oracle(grid):
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    totals = []
    for down_positions in combinations(range(m + n - 2), m - 1):
        row = column = 0
        total = grid[0][0]
        for step in range(m + n - 2):
            if step in down_positions:
                row += 1
            else:
                column += 1
            total += grid[row][column]
        totals.append(total)
    return min(totals)


def solve(module, grid):
    """Isolate the explicitly mutating implementation for shared checks."""
    candidate = deepcopy(grid)
    result = module.min_path_sum(candidate)
    if module is not in_place:
        assert candidate == grid
    return result


@st.composite
def grids(draw):
    m = draw(st.integers(1, 5))
    n = draw(st.integers(1, 5))
    return draw(st.lists(st.lists(st.integers(-20, 30), min_size=n, max_size=n), min_size=m, max_size=m))


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("grid", "expected"),
    [
        ([], 0), ([[]], 0), ([[], []], 0),
        ([[5]], 5), ([[0]], 0),
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[1, 2, 3], [4, 5, 6]], 12),
        ([[1, 2, 3]], 6), ([[1], [2], [3]], 6),
        ([[0, 0], [0, 0]], 0),
        ([[1, 1, 100], [2, 100, 100], [1, 1, 1]], 6),
        ([[1, 100], [1, 1]], 3),
        ([[-1, -2], [-3, -4]], -8),
        ([[10**12] * 3 for _ in range(2)], 4 * 10**12),
    ],
)
def test_examples_and_boundaries(module, grid, expected):
    result = solve(module, grid)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_binary_grids(module):
    for m in range(1, 4):
        for n in range(1, 4):
            for values in product(range(2), repeat=m * n):
                grid = [list(values[row * n:(row + 1) * n]) for row in range(m)]
                assert solve(module, grid) == path_oracle(grid), grid


@pytest.mark.parametrize("module", IMPLS)
@given(grid=grids())
@settings(max_examples=150, deadline=None)
def test_independent_oracle(module, grid):
    assert solve(module, grid) == path_oracle(grid)


@pytest.mark.parametrize("module", IMPLS)
@given(grid=grids(), shift=st.integers(-10, 10), scale=st.integers(0, 5), data=st.data())
@settings(max_examples=100, deadline=None)
def test_properties(module, grid, shift, scale, data):
    m, n = len(grid), len(grid[0])
    result = solve(module, grid)
    assert solve(module, [list(row) for row in zip(*grid)]) == result
    assert solve(module, [row[::-1] for row in grid[::-1]]) == result
    assert solve(module, [[v + shift for v in row] for row in grid]) == result + (m + n - 1) * shift
    assert solve(module, [[v * scale for v in row] for row in grid]) == result * scale
    row = data.draw(st.integers(0, m - 1))
    column = data.draw(st.integers(0, n - 1))
    changed = deepcopy(grid)
    changed[row][column] += 5
    assert result <= solve(module, changed) <= result + 5


@pytest.mark.parametrize("module", IMPLS)
def test_scale_and_repeated_calls(module):
    assert solve(module, [[1] * 200 for _ in range(200)]) == 399
    assert solve(module, [[1] * 10_000]) == 10_000
    assert solve(module, [[1] for _ in range(10_000)]) == 10_000
    assert solve(module, [[1, 2], [3, 4]]) == 7
    assert solve(module, []) == 0
    assert solve(module, [[1, 2], [3, 4]]) == 7


@pytest.mark.parametrize("module", (rolling, in_place), ids=lambda module: module.__name__)
def test_validation_and_wrapper(module):
    for grid in ([[1, 2], [3]], [[], [1]], [[1], []]):
        before = deepcopy(grid)
        with pytest.raises(ValueError):
            module.min_path_sum(grid)
        assert grid == before
    assert module.Solution().minPathSum([[1, 2], [3, 4]]) == 7


def test_in_place_mutation():
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    rows = grid.copy()
    assert in_place.min_path_sum(grid) == 7
    assert grid == [[1, 4, 5], [2, 7, 6], [6, 8, 7]]
    assert all(a is b for a, b in zip(rows, grid))


@pytest.mark.parametrize("module", (original, rolling), ids=lambda module: module.__name__)
def test_nonmutating_aliased_rows(module):
    row = [1, 2, 3]
    grid = [row] * 3
    assert module.min_path_sum(grid) == 8
    assert row == [1, 2, 3]
    assert all(item is row for item in grid)


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"min_path_sum_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
