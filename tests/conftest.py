import pytest

from pytest_django_queries.entry import flatten_entries

pytest_plugins = 'pytester'


@pytest.fixture
def valid_comparison_entries():
    left = {
        "test_module": {
            "test_improved_func": {"query-count": 20},
            "test_degraded_func": {"query-count": 15},
            "test_unchanged_func": {"query-count": 1},
        }
    }

    right = {
        "test_module": {
            "test_improved_func": {"query-count": 19},
            "test_degraded_func": {"query-count": 16},
            "test_unchanged_func": {"query-count": 1},
        }
    }

    return left, right
