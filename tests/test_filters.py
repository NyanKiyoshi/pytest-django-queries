import pytest

from pytest_django_queries import filters


@pytest.mark.parametrize(
    "input_, output",
    [
        ("tests.api.test_something", "api something"),
        ("test_something_test", "something test"),
    ],
)
def test_humanize(input_, output):
    assert filters.format_underscore_name_to_human(input_) == output
