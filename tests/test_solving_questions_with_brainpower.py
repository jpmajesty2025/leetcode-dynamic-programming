"""Verify both DP directions against independent feasible-subset enumeration."""

from itertools import product

import pytest
from hypothesis import given, settings, strategies as st

import solving_questions_with_brainpower as backward
import solving_questions_with_brainpower_forward_dp as forward

MODULES = (backward, forward)
IMPLS = [pytest.param(m.most_points, id=m.__name__) for m in MODULES]
SMALL_QUESTIONS = st.lists(
    st.tuples(st.integers(1, 100), st.integers(1, 20)).map(list),
    max_size=12,
)


def subset_oracle(questions):
    """Check compatibility of selected indices without a DP recurrence."""
    best = 0
    for mask in range(1 << len(questions)):
        chosen = [i for i in range(len(questions)) if mask & (1 << i)]
        if all(j > i + questions[i][1] for i, j in zip(chosen, chosen[1:])):
            best = max(best, sum(questions[i][0] for i in chosen))
    return best


@pytest.mark.parametrize("solve", IMPLS)
@pytest.mark.parametrize(
    ("questions", "expected"),
    [
        ([], 0),
        ([[7, 1]], 7),
        ([[7, 100_000]], 7),
        ([[3, 2], [4, 3], [4, 4], [2, 5]], 5),
        ([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]], 7),
        ([[3, 1], [8, 1]], 8),
        ([[8, 1], [3, 1]], 8),
        ([[5, 2], [1, 1], [1, 1]], 5),
        ([[5, 1], [1, 1], [7, 1]], 12),
        ([[1, 1], [1, 1], [9, 1]], 10),
        ([[8, 3], [5, 1], [1, 1], [5, 1]], 10),
        ([[5, 1], [5, 1], [5, 1], [5, 1]], 10),
        ([[1, 100_000], [100_000, 100_000]], 100_000),
        ([[10, 100], [20, 100], [30, 100]], 30),
    ],
)
def test_examples_and_boundaries(solve, questions, expected):
    original = [row[:] for row in questions]
    assert solve(questions) == expected
    assert questions == original


@pytest.mark.parametrize("solve", IMPLS)
def test_exhaustive_small_inputs(solve):
    options = ((1, 1), (3, 1), (1, 3), (3, 3))
    for size in range(7):
        for values in product(options, repeat=size):
            questions = [list(q) for q in values]
            assert solve(questions) == subset_oracle(questions), questions


@pytest.mark.parametrize("solve", IMPLS)
@given(questions=SMALL_QUESTIONS)
@settings(max_examples=150, deadline=None)
def test_oracle_and_nested_nonmutation(solve, questions):
    original = [row[:] for row in questions]
    rows = list(questions)
    result = solve(questions)
    assert type(result) is int
    assert result == subset_oracle(questions)
    assert questions == original
    assert all(a is b for a, b in zip(questions, rows))


@pytest.mark.parametrize("solve", IMPLS)
@given(questions=SMALL_QUESTIONS, factor=st.integers(1, 10))
@settings(max_examples=100, deadline=None)
def test_score_scaling_and_bounds(solve, questions, factor):
    result = solve(questions)
    scaled = [[points * factor, cooldown] for points, cooldown in questions]
    assert solve(scaled) == factor * result
    assert max((q[0] for q in questions), default=0) <= result
    assert result <= sum(q[0] for q in questions)


@pytest.mark.parametrize("solve", IMPLS)
@given(
    questions=st.lists(
        st.tuples(st.integers(1, 100), st.integers(1, 20)).map(list),
        min_size=1,
        max_size=30,
    ),
    data=st.data(),
)
@settings(max_examples=100, deadline=None)
def test_score_and_cooldown_monotonicity(solve, questions, data):
    i = data.draw(st.integers(0, len(questions) - 1))
    increase = data.draw(st.integers(1, 100))
    original = solve(questions)
    higher_score = [row[:] for row in questions]
    higher_score[i][0] += increase
    assert original <= solve(higher_score) <= original + increase
    longer_cooldown = [row[:] for row in questions]
    longer_cooldown[i][1] += increase
    assert solve(longer_cooldown) <= original


@pytest.mark.parametrize("solve", IMPLS)
def test_repeated_calls_and_changed_nested_input(solve):
    questions = [[5, 1], [2, 1], [7, 1]]
    assert solve(questions) == 12
    assert solve([[100, 1]]) == 100
    questions[0][1] = 10
    assert solve(questions) == 7
    assert solve([]) == 0


@pytest.mark.parametrize("module", MODULES, ids=lambda m: m.__name__)
def test_solution_wrapper(module):
    solution = module.Solution()
    questions = [[3, 2], [4, 3], [4, 4], [2, 5]]
    assert solution.mostPoints(questions) == 5
    assert questions == [[3, 2], [4, 3], [4, 4], [2, 5]]
    assert solution.mostPoints([]) == 0


@pytest.mark.parametrize("solve", IMPLS)
def test_maximum_size_and_large_total(solve):
    questions = [[100_000, 1] for _ in range(100_000)]
    assert solve(questions) == 5_000_000_000


@pytest.mark.parametrize("solve", IMPLS)
def test_maximum_size_with_beyond_end_jumps(solve):
    questions = [[i + 1, 100_000] for i in range(100_000)]
    assert solve(questions) == 100_000
