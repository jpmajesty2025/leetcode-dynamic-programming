"""Check obstacle path counting by independently enumerating move sequences."""

from copy import deepcopy
from itertools import combinations, product
from math import comb
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import unique_paths_ii as original
import unique_paths_ii_rolling_dp as rolling
import unique_paths_ii_in_place as in_place

MODULES = (original, rolling, in_place)
ALTERNATIVES = (rolling, in_place)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]


def path_oracle(grid):
    """Enumerate complete paths and reject any that visit a blocked cell."""
    if not grid or not grid[0]:
        return 0
    rows, columns = len(grid), len(grid[0])
    paths = 0
    for down_positions in combinations(range(rows + columns - 2), rows - 1):
        row = column = 0
        blocked = grid[0][0] == 1
        for step in range(rows + columns - 2):
            if step in down_positions:
                row += 1
            else:
                column += 1
            blocked = blocked or grid[row][column] == 1
        paths += not blocked
    return paths


def solve(module, grid):
    candidate = deepcopy(grid)
    result = module.unique_paths_with_obstacles(candidate)
    if module is not in_place:
        assert candidate == grid
    return result


@st.composite
def binary_grids(draw):
    rows = draw(st.integers(1, 5))
    columns = draw(st.integers(1, 5))
    return draw(
        st.lists(
            st.lists(st.integers(0, 1), min_size=columns, max_size=columns),
            min_size=rows,
            max_size=rows,
        )
    )


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("grid", "expected"),
    [
        ([], 0),
        ([[0]], 1),
        ([[1]], 0),
        ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
        ([[0, 1], [0, 0]], 1),
        ([[1, 0], [0, 0]], 0),
        ([[0, 0], [0, 1]], 0),
        ([[0, 0, 0]], 1),
        ([[0, 1, 0]], 0),
        ([[0], [0], [0]], 1),
        ([[0], [1], [0]], 0),
        ([[0, 1], [1, 0]], 0),
        ([[0, 0, 0], [1, 1, 1], [0, 0, 0]], 0),
        ([[0, 1, 0], [0, 0, 0], [0, 0, 0]], 3),
        ([[0, 0, 0], [1, 0, 0], [0, 0, 0]], 3),
        ([[0, 0], [0, 0]], 2),
        ([[0] * 18 for _ in range(18)], comb(34, 17)),
    ],
)
def test_examples_and_boundaries(module, grid, expected):
    result = solve(module, grid)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_small_grids(module):
    for rows in range(1, 4):
        for columns in range(1, 4):
            for cells in product(range(2), repeat=rows * columns):
                grid = [
                    list(cells[row * columns:(row + 1) * columns])
                    for row in range(rows)
                ]
                assert solve(module, grid) == path_oracle(grid), grid


@pytest.mark.parametrize("module", IMPLS)
@given(grid=binary_grids())
@settings(max_examples=200, deadline=None)
def test_independent_oracle(module, grid):
    assert solve(module, grid) == path_oracle(grid)


@pytest.mark.parametrize("module", IMPLS)
@given(grid=binary_grids(), data=st.data())
@settings(max_examples=150, deadline=None)
def test_properties(module, grid, data):
    rows, columns = len(grid), len(grid[0])
    result = solve(module, grid)
    assert 0 <= result <= comb(rows + columns - 2, rows - 1)
    assert solve(module, [list(row) for row in zip(*grid)]) == result
    assert solve(module, [row[::-1] for row in grid[::-1]]) == result
    row = data.draw(st.integers(0, rows - 1))
    column = data.draw(st.integers(0, columns - 1))
    blocked = deepcopy(grid)
    blocked[row][column] = 1
    assert solve(module, blocked) <= result
    opened = deepcopy(grid)
    opened[row][column] = 0
    assert solve(module, opened) >= result


@pytest.mark.parametrize("module", IMPLS)
def test_open_grids_scale_and_repeated_calls(module):
    assert solve(module, [[0] * 100 for _ in range(100)]) == comb(198, 99)
    assert solve(module, [[0] * 10_000]) == 1
    assert solve(module, [[0] for _ in range(10_000)]) == 1
    assert solve(module, [[0, 0], [0, 0]]) == 2
    assert solve(module, [[1]]) == 0
    assert solve(module, [[0, 0], [0, 0]]) == 2


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_empty_rows_validation_and_wrapper(module):
    for grid in ([[]], [[], []]):
        assert module.unique_paths_with_obstacles(grid) == 0
    for grid in ([[0, 0], [0]], [[], [0]], [[0], []], [[1], [0, 0]]):
        before = deepcopy(grid)
        with pytest.raises(ValueError):
            module.unique_paths_with_obstacles(grid)
        assert grid == before
    assert module.Solution().uniquePathsWithObstacles([[0, 1], [0, 0]]) == 1


def test_in_place_complete_grid_and_row_identity():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    rows = grid.copy()
    assert in_place.unique_paths_with_obstacles(grid) == 2
    assert grid == [[1, 1, 1], [1, 0, 1], [1, 1, 2]]
    assert all(before is after for before, after in zip(rows, grid))


@pytest.mark.parametrize("module", (original, rolling), ids=lambda module: module.__name__)
def test_nonmutating_aliased_rows_and_keyword_api(module):
    row = [0, 0, 0]
    grid = [row] * 3
    assert module.unique_paths_with_obstacles(obstacleGrid=grid) == 6
    assert row == [0, 0, 0]
    assert all(item is row for item in grid)


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    root = Path(__file__).resolve().parents[1]
    path = root / "posts" / f"unique_paths_ii_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
