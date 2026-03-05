"""Ensure when pytest-django is installed, it detects properly."""

import json

import pytest

from tests.conftest import DEFAULT_PYTEST_FLAGS


@pytest.mark.parametrize(
    ("_case", "pytest_flags", "expects_django_plugin"),
    [
        (
            "When using pytest-django, it should detect it",
            # Note: we cannot use `-p django` as it will error out
            # due to a warning being fired
            # (https://github.com/pytest-dev/pytest/issues/5473)
            ["-p", "pytest_django.plugin", "--ds", "example.settings"],
            True,
        ),
        (
            "When pytest-django isn't used, it should detect it as missing",
            ["--disable-plugin-autoload"],
            False,
        ),
    ],
)
def test_detect_pytest_django(
    _case: str,
    pytester: pytest.Pytester,
    pytest_flags: list[str],
    expects_django_plugin: bool,
):
    """Ensure when pytest-django is installed, it detects properly."""
    results_path = pytester.path / "results.json"

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    pytester.makepyfile(
        test_file=f"""
    import pytest

    {"@pytest.mark.django_db" if expects_django_plugin else ""}
    @pytest.mark.count_queries
    def test_count_db_query_number(request: pytest.FixtureRequest):
        from django.db import connection

        assert hasattr(request.config, "dj_queries_has_django_plugin")
        assert (
            request.config.dj_queries_has_django_plugin
            is {"True" if expects_django_plugin else "False"}
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT date('now');")
            cursor.execute("SELECT 1;")
            cursor.fetchone()
    """
    )
    results = pytester.runpytest_inprocess(
        *DEFAULT_PYTEST_FLAGS,
        "-Werror",
        "--django-db-bench",
        results_path,
        *pytest_flags,
    )

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was created
    assert results_path.exists()
    assert json.loads(results_path.read_bytes()) == {
        "test_file": {"test_count_db_query_number": {"query-count": 2, "duplicates": 0}}
    }
