"""Verify falling-path DP with independent complete column-sequence enumeration."""

from copy import deepcopy
from itertools import product
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import min_falling_path_sum as original
import min_falling_path_sum_rolling_dp as rolling
import min_falling_path_sum_in_place as in_place

MODULES = (original, rolling, in_place)
ALTERNATIVES = (rolling, in_place)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]


def column_sequence_oracle(matrix):
    """Try all column sequences; filter adjacent-column constraints, then sum."""
    if not matrix or not matrix[0]:
        return 0
    rows, columns = len(matrix), len(matrix[0])
    return min(
        sum(matrix[row][column] for row, column in enumerate(sequence))
        for sequence in product(range(columns), repeat=rows)
        if all(abs(a - b) <= 1 for a, b in zip(sequence, sequence[1:]))
    )


def solve(module, matrix):
    candidate = deepcopy(matrix)
    result = module.min_falling_path_sum(candidate)
    if module is not in_place:
        assert candidate == matrix
    return result


@st.composite
def square_matrices(draw):
    size = draw(st.integers(1, 4))
    return draw(st.lists(st.lists(st.integers(-30, 30), min_size=size, max_size=size), min_size=size, max_size=size))


@st.composite
def rectangles(draw):
    rows = draw(st.integers(1, 5))
    columns = draw(st.integers(1, 4))
    return draw(st.lists(st.lists(st.integers(-20, 20), min_size=columns, max_size=columns), min_size=rows, max_size=rows))


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        ([], 0), ([[]], 0), ([[], []], 0),
        ([[5]], 5), ([[-5]], -5), ([[0]], 0),
        ([[2, 1, 3], [6, 5, 4], [7, 8, 9]], 13),
        ([[-19, 57], [-40, -5]], -59),
        ([[0, 0], [0, 0]], 0),
        ([[7] * 3 for _ in range(3)], 21),
        ([[-7] * 3 for _ in range(3)], -21),
        ([[1, 100, 100], [100, 1, 100], [100, 100, 1]], 3),
        ([[100, 100, 1], [100, 1, 100], [1, 100, 100]], 3),
        ([[0, 100, 100], [100, 100, 0], [100, 100, 0]], 100),
        ([[1, 100, 100], [100, 1, 2], [1000, 1000, 0]], 2),
        ([[1, 100, 100, 100], [1, 2, 100, 100], [100, 100, 1, 100], [100, 100, 100, 1]], 5),
        ([[10**12] * 3 for _ in range(3)], 3 * 10**12),
    ],
)
def test_examples_and_boundaries(module, matrix, expected):
    result = solve(module, matrix)
    assert type(result) is int
    assert result == expected


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_binary_squares(module):
    for size in range(1, 4):
        for cells in product(range(2), repeat=size * size):
            matrix = [list(cells[row * size:(row + 1) * size]) for row in range(size)]
            assert solve(module, matrix) == column_sequence_oracle(matrix), matrix


@pytest.mark.parametrize("module", IMPLS)
@given(matrix=square_matrices())
@settings(max_examples=200, deadline=None)
def test_independent_oracle(module, matrix):
    assert solve(module, matrix) == column_sequence_oracle(matrix)


@pytest.mark.parametrize("module", IMPLS)
@given(matrix=square_matrices(), shift=st.integers(-10, 10), scale=st.integers(0, 5), data=st.data())
@settings(max_examples=150, deadline=None)
def test_properties(module, matrix, shift, scale, data):
    size = len(matrix)
    result = solve(module, matrix)
    assert solve(module, [row[::-1] for row in matrix]) == result
    assert solve(module, matrix[::-1]) == result
    assert solve(module, [[value + shift for value in row] for row in matrix]) == result + size * shift
    assert solve(module, [[value * scale for value in row] for row in matrix]) == result * scale
    assert sum(map(min, matrix)) <= result <= min(sum(matrix[row][column] for row in range(size)) for column in range(size))
    changed = deepcopy(matrix)
    row = data.draw(st.integers(0, size - 1))
    changed[row] = [value + 3 for value in changed[row]]
    assert solve(module, changed) == result + 3
    column = data.draw(st.integers(0, size - 1))
    changed = deepcopy(matrix)
    changed[row][column] += 5
    assert result <= solve(module, changed) <= result + 5


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
@given(matrix=rectangles())
@settings(max_examples=150, deadline=None)
def test_rectangular_extension(module, matrix):
    assert solve(module, matrix) == column_sequence_oracle(matrix)


@pytest.mark.parametrize("module", ALTERNATIVES, ids=lambda module: module.__name__)
def test_validation_rectangles_and_wrapper(module):
    assert solve(module, [[3, -2, 5]]) == -2
    assert solve(module, [[3], [-2], [5]]) == 6
    assert solve(module, [[1, 9, 2], [9, 9, 1]]) == 3
    for matrix in ([[1, 2], [3]], [[], [1]], [[1], []]):
        before = deepcopy(matrix)
        with pytest.raises(ValueError):
            module.min_falling_path_sum(matrix)
        assert matrix == before
    assert module.Solution().minFallingPathSum([[2, 1], [3, 4]]) == 4


@pytest.mark.parametrize("module", IMPLS)
def test_scale_and_repeated_calls(module):
    assert solve(module, [[1] * 100 for _ in range(100)]) == 100
    assert solve(module, [[-100] * 100 for _ in range(100)]) == -10_000
    assert solve(module, [[2, 1], [3, 4]]) == 4
    assert solve(module, []) == 0
    assert solve(module, [[2, 1], [3, 4]]) == 4


def test_in_place_complete_output_and_row_identity():
    matrix = [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
    rows = matrix.copy()
    assert in_place.min_falling_path_sum(matrix) == 13
    assert matrix == [[2, 1, 3], [7, 6, 5], [13, 13, 14]]
    assert all(before is after for before, after in zip(rows, matrix))


@pytest.mark.parametrize("module", (original, rolling), ids=lambda module: module.__name__)
def test_nonmutating_aliased_rows(module):
    row = [1, 2, 3]
    matrix = [row] * 3
    assert module.min_falling_path_sum(matrix) == 3
    assert row == [1, 2, 3]
    assert all(item is row for item in matrix)


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"min_falling_path_sum_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
