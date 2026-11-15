"""Verify Pascal rows with subset counts, binomial coefficients, and identities."""

from itertools import product
from math import comb
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

import pascals_triangle as original
import pascals_triangle_binomial as binomial
import pascals_triangle_streaming as streaming

MODULES = (original, binomial, streaming)
IMPLS = [pytest.param(module, id=module.__name__) for module in MODULES]


def subset_oracle(rows):
    triangle = []
    for size in range(rows):
        counts = [0] * (size + 1)
        for membership in product((0, 1), repeat=size):
            counts[sum(membership)] += 1
        triangle.append(counts)
    return triangle


@pytest.mark.parametrize("module", IMPLS)
@pytest.mark.parametrize(
    ("rows", "expected"),
    [
        (-5, []), (0, []), (1, [[1]]), (2, [[1], [1, 1]]),
        (3, [[1], [1, 1], [1, 2, 1]]),
        (5, [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]),
    ],
)
def test_examples_and_boundaries(module, rows, expected):
    assert module.generate(numRows=rows) == expected


@pytest.mark.parametrize("module", IMPLS)
def test_exhaustive_small_subset_counts(module):
    for rows in range(11):
        assert module.generate(rows) == subset_oracle(rows)


@pytest.mark.parametrize("module", IMPLS)
@given(rows=st.integers(0, 100))
@settings(max_examples=101, deadline=None)
def test_binomial_reference_and_properties(module, rows):
    triangle = module.generate(rows)
    assert type(triangle) is list
    assert len(triangle) == rows
    assert len({id(row) for row in triangle}) == rows
    for index, row in enumerate(triangle):
        assert type(row) is list
        assert len(row) == index + 1
        assert row == [comb(index, column) for column in range(index + 1)]
        assert all(type(value) is int and value > 0 for value in row)
        assert row == row[::-1]
        assert row[0] == row[-1] == 1
        assert sum(row) == 2 ** index
        assert sum((-1) ** column * value for column, value in enumerate(row)) == (1 if index == 0 else 0)
        if index > 1:
            assert row[1:-1] == [a + b for a, b in zip(triangle[index - 1], triangle[index - 1][1:])]
    assert module.generate(rows + 1)[:rows] == triangle


@pytest.mark.parametrize("module", IMPLS)
def test_independent_rows_calls_and_large_values(module):
    triangle = module.generate(6)
    pristine = [row.copy() for row in triangle]
    triangle[2][0] = -100
    triangle[3].append(999)
    assert triangle[1] == pristine[1]
    assert triangle[4] == pristine[4]
    assert module.generate(6) == pristine
    assert module.generate(0) == []
    assert module.generate(101)[100][50] == comb(100, 50)


@pytest.mark.parametrize("module", (binomial, streaming), ids=lambda module: module.__name__)
def test_solution_wrapper(module):
    assert module.Solution().generate(numRows=5) == original.generate(5)
    assert module.Solution().generate(0) == []


def test_streaming_mutation_isolation():
    iterator = streaming.iter_rows(5)
    first = next(iterator)
    first[0] = 999
    second = next(iterator)
    second.clear()
    assert list(iterator) == [[1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert list(iterator) == []
    assert list(streaming.iter_rows(-1)) == []
    assert list(streaming.iter_rows(0)) == []


def test_streaming_early_stop_and_independent_iterators():
    first = streaming.iter_rows(10**9)
    second = streaming.iter_rows(3)
    assert next(first) == next(second) == [1]
    assert next(first) == next(second) == [1, 1]
    first.close()
    assert list(second) == [[1, 2, 1]]


@pytest.mark.parametrize("part", [1, 2])
def test_linkedin_draft_constraints(part):
    path = Path(__file__).resolve().parents[1] / "posts" / f"pascals_triangle_part{part}_linkedin.md"
    text = path.read_text(encoding="utf-8")
    assert 0 < len(text) <= 3000, f"{path.name}: {len(text)} characters"
    assert "#LearningInPublic" in text
    assert "```" not in text
