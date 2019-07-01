import pytest

from pytest_django_queries.diff import DiffGenerator
from pytest_django_queries.entry import flatten_entries


@pytest.mark.parametrize("right", ({}, {"test_module": {}}, {"test_module_123": {}}))
def test_comparison_deleted_test_triggers_negative_review(right):
    left = flatten_entries({"test_module": {"test_deleted_func": {"query-count": 1}}})
    right = flatten_entries(right)
    module_diffs = list(next(iter(DiffGenerator(left, right)))[1])

    # We expect it to:
    # 1. start with '-'
    # 2. to give a left value of 1
    # 3. to give a right value of N/A
    assert (
        "- deleted func     \t          1\t          -\t            UNK" in module_diffs
    )


@pytest.mark.parametrize("left", ({}, {"test_module": {}}, {"test_module_123": {}}))
def test_comparison_new_test_triggers_positive_review(left):
    left = flatten_entries(left)
    right = flatten_entries({"test_module": {"test_added_func": {"query-count": 1}}})
    module_diffs = list(next(iter(DiffGenerator(left, right)))[1])

    # We expect it to:
    # 1. start with '+'
    # 2. to give a left value of N/A
    # 3. to give a right value of 1
    assert (
        "+ added func     \t          -\t          1\t            UNK" in module_diffs
    )


def test_comparison_diff_is_correct(valid_comparison_entries):
    left, right = valid_comparison_entries
    left = flatten_entries(left)
    right = flatten_entries(right)

    module_diffs = list(next(iter(DiffGenerator(left, right)))[1])

    assert len(module_diffs) == 4  # 3 tests + header
    assert (
        "+ improved func      \t         20\t         19\t              0"
        in module_diffs
    )
    assert (
        "- degraded func      \t         15\t         16\t              0"
        in module_diffs
    )
    assert (
        "  unchanged func     \t          1\t          1\t              0"
        in module_diffs
    )
