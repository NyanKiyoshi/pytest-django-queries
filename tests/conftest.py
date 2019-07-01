import pytest

pytest_plugins = "pytester"


@pytest.fixture
def valid_comparison_entries():
    left = {
        "test_module": {
            "test_improved_func": {"query-count": 20, "duplicates": 0},
            "test_degraded_func": {"query-count": 15, "duplicates": 0},
            "test_unchanged_func": {"query-count": 1, "duplicates": 0},
        }
    }

    right = {
        "test_module": {
            "test_improved_func": {"query-count": 19, "duplicates": 0},
            "test_degraded_func": {"query-count": 16, "duplicates": 0},
            "test_unchanged_func": {"query-count": 1, "duplicates": 0},
        }
    }

    return left, right
