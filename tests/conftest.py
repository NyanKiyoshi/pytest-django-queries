import pytest

pytest_plugins = "pytester"

# Prevents autoloading plugins as they could impact the test results,
# e.g., we could fail to detect that the plugin doesn't work if
# pytest-django isn't installed (as it's an optional plugin)
DEFAULT_PYTEST_FLAGS = [
    "--disable-plugin-autoload",
    "-p",
    "xdist",
    "-p",
    "django_queries",
]


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
