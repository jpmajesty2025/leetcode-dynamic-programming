"""Compare non-zero-shift DP with independent complete column sequences."""

from copy import deepcopy
from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import min_falling_path_sum_ii as original
import min_falling_path_sum_ii_two_minima as rolling
import min_falling_path_sum_ii_constant_space as compressed

MODULES = (original, rolling, compressed)
ALTERNATIVES = (rolling, compressed)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]


def sequence_oracle(grid):
    if not grid or not grid[0]:
        return 0
    return min(
        sum(grid[row][column] for row, column in enumerate(sequence))
        for sequence in product(range(len(grid[0])), repeat=len(grid))
        if all(a != b for a, b in zip(sequence, sequence[1:]))
    )


def solve(module, grid):
    candidate = deepcopy(grid)
    result = module.min_falling_path_sum(candidate)
    assert candidate == grid
    assert type(result) is int
    return result


@st.composite
def squares(draw):
    size = draw(st.integers(1, 4))
    row = st.lists(st.integers(-20, 20), min_size=size, max_size=size)
    return draw(st.lists(row, min_size=size, max_size=size))


@st.composite
def rectangles(draw):
    rows = draw(st.integers(1, 5))
    columns = draw(st.integers(2, 4))
    row = st.lists(st.integers(-20, 20), min_size=columns, max_size=columns)
    return draw(st.lists(row, min_size=rows, max_size=rows))


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("grid", "expected"),
    [
        ([], 0), ([[]], 0), ([[], []], 0),
        ([[7]], 7), ([[-7]], -7), ([[0]], 0),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 13),
        ([[1, 1], [1, 1]], 2),
        ([[0, 0], [0, 100]], 0),
        ([[0, 100], [0, 100]], 100),
        ([[1, 2], [3, 4]], 5),
        ([[-1, -2], [-3, -4]], -5),
        ([[1, 100, 100], [1, 100, 100], [1, 100, 100]], 102),
        ([[0, 100, 100], [100, 100, 0], [0, 100, 100]], 0),
        ([[1, 1, 9], [1, 1, 9], [1, 1, 9]], 3),
        ([[5] * 3 for _ in range(3)], 15),
        ([[-5] * 3 for _ in range(3)], -15),
        ([[10**12] * 3 for _ in range(3)], 3 * 10**12),
    ],
)
def test_examples_and_boundaries(module, grid, expected):
    assert solve(module, grid) == expected


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_binary_squares(module):
    for size in range(1, 4):
        for values in product(range(2), repeat=size * size):
            grid = [list(values[row * size:(row + 1) * size]) for row in range(size)]
            assert solve(module, grid) == sequence_oracle(grid), grid


@pytest.mark.parametrize("module", IMPLS)
@given(grid=squares())
@settings(max_examples=200, deadline=None)
def test_independent_oracle(module, grid):
    assert solve(module, grid) == sequence_oracle(grid)


@pytest.mark.parametrize("module", IMPLS)
@given(grid=squares(), shift=st.integers(-10, 10), scale=st.integers(0, 5), data=st.data())
@settings(max_examples=150, deadline=None)
def test_properties(module, grid, shift, scale, data):
    size = len(grid)
    result = solve(module, grid)
    permutation = data.draw(st.permutations(tuple(range(size))))
    assert solve(module, [[row[j] for j in permutation] for row in grid]) == result
    assert solve(module, grid[::-1]) == result
    assert solve(module, [[v + shift for v in row] for row in grid]) == result + size * shift
    assert solve(module, [[v * scale for v in row] for row in grid]) == result * scale
    assert result >= sum(map(min, grid))
    row = data.draw(st.integers(0, size - 1))
    changed = deepcopy(grid)
    changed[row] = [v + 3 for v in changed[row]]
    assert solve(module, changed) == result + 3
    column = data.draw(st.integers(0, size - 1))
    changed = deepcopy(grid)
    changed[row][column] += 5
    assert result <= solve(module, changed) <= result + 5


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
@given(grid=rectangles())
@settings(max_examples=150, deadline=None)
def test_rectangular_extension(module, grid):
    assert solve(module, grid) == sequence_oracle(grid)


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_validation_and_wrapper(module):
    assert solve(module, [[3, -2, 5]]) == -2
    assert solve(module, [[1, 2], [3, 4], [5, 6]]) == 10
    for grid in ([[1], [2]], [[1, 2], [3]], [[], [1]], [[1], []]):
        before = deepcopy(grid)
        with pytest.raises(ValueError):
            module.min_falling_path_sum(grid)
        assert grid == before
    assert module.Solution().minFallingPathSum([[1, 2], [3, 4]]) == 5


@pytest.mark.parametrize("module", IMPLS)
def test_repeated_calls_and_aliased_rows(module):
    row = [1, 2, 3]
    grid = [row] * 3
    assert module.min_falling_path_sum(grid) == 4
    assert all(item is row for item in grid)
    assert row == [1, 2, 3]
    assert solve(module, [[1, 2], [3, 4]]) == 5
    assert solve(module, []) == 0
    assert solve(module, [[1, 2], [3, 4]]) == 5


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_large_optimized_inputs(module):
    assert solve(module, [[1] * 200 for _ in range(200)]) == 200
    assert solve(module, [[-100] * 200 for _ in range(200)]) == -20_000
    assert solve(module, [[0, 1] for _ in range(10_000)]) == 5000


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"min_falling_path_sum_ii_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
