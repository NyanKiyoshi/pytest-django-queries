import json
import os
import os.path
import shutil

import mock
import pytest

DUMMY_TEST_QUERY = """
    import pytest

    @pytest.mark.count_queries
    def test_count_db_query_number():
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("SELECT date('now');")
            cursor.execute("SELECT 1;")
            cursor.fetchone()
"""


def test_plugin_is_loaded(request):
    # Check that the plugin has been properly installed before proceeding
    assert request.config.pluginmanager.hasplugin("django_queries")


def test_fixture_is_invoked_when_marked(testdir):
    """Ensure marking a test is actually calling the fixture."""
    results_path = testdir.tmpdir.join("results.json")

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(test_file=DUMMY_TEST_QUERY)
    results = testdir.runpytest("--django-db-bench", results_path)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
        "test_file": {"test_count_db_query_number": {"query-count": 2, "duplicates": 0}}
    }


def test_plugin_exports_nothing_if_empty(testdir):
    """Ensure the plugin does not export any results if no performance
    tests were run."""

    results_path = testdir.tmpdir.join("results.json")

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(
        """
        def test_nothing():
            pass
    """
    )
    results = testdir.runpytest("--django-db-bench", results_path)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was not created
    assert not results_path.check()


def test_plugin_exports_results_even_when_test_fails(testdir):
    """Ensure the plugin does not export any results if no performance
    tests were run."""

    results_path = testdir.tmpdir.join("results.json")

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.count_queries
        def test_failure():
            assert 0
    """
    )
    results = testdir.runpytest("--django-db-bench", results_path)

    # Ensure the tests have failed
    results.assert_outcomes(0, 0, 1)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
        "test_plugin_exports_results_even_when_test_fails": {
            "test_failure": {"query-count": 0, "duplicates": 0}
        }
    }


def test_plugin_marker_without_autouse_handles_other_fixtures(testdir):
    """Ensure marking a test for counting queries is not counting other fixtures."""

    results_path = testdir.tmpdir.join("results.json")
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture()
        def fixture_with_db_queries():
            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT date('now');")
                cursor.execute("SELECT 1;")
                cursor.fetchone()

        @pytest.mark.count_queries(autouse=False)
        def test_with_side_effects(fixture_with_db_queries, count_queries):
            pass
    """
    )
    results = testdir.runpytest("--django-db-bench", results_path)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
        "test_plugin_marker_without_autouse_handles_other_fixtures": {
            "test_with_side_effects": {"query-count": 0, "duplicates": 0}
        }
    }


def test_plugin_marker_without_autouse_disabled(testdir):
    """Ensure marking a test for counting queries without autouse
    is actually not counting queries unless the fixture is used manually."""

    results_path = testdir.tmpdir.join("results.json")
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.count_queries(autouse=False)
        def test_without_autouse():
            pass
    """
    )
    results = testdir.runpytest("--django-db-bench", results_path)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure not results were found
    assert not results_path.check()


def test_fixture_is_backing_up_old_results(testdir):
    """Ensure marking a test is backing up old results if asked to."""
    results_path = testdir.tmpdir.join("results.json")
    old_results_path = testdir.tmpdir.join("results.old.json")

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(test_file=DUMMY_TEST_QUERY)

    results = testdir.runpytest(
        "--django-db-bench", results_path, "--django-backup-queries", old_results_path
    )

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was created
    assert results_path.check()
    assert (
        not old_results_path.check()
    ), "Nothing should have been backed up--there was nothing to back up"

    # Create another test to generate more results,
    # to ensure the backup results were actually the previous ones
    testdir.makepyfile(test_otherfile=DUMMY_TEST_QUERY)

    # Run again the tests
    results = testdir.runpytest(
        "--django-db-bench", results_path, "--django-backup-queries", old_results_path
    )

    # Ensure the tests have passed
    results.assert_outcomes(2, 0, 0)

    # Ensure the results file was created
    assert results_path.check()
    assert old_results_path.check(), "The backup file should have been created"

    # Check contents
    assert json.load(results_path) == {
        "test_file": {
            "test_count_db_query_number": {"query-count": 2, "duplicates": 0}
        },
        "test_otherfile": {
            "test_count_db_query_number": {"query-count": 2, "duplicates": 0}
        },
    }
    assert json.load(old_results_path) == {
        "test_file": {"test_count_db_query_number": {"query-count": 2, "duplicates": 0}}
    }


def test_fixture_is_not_backing_up_if_not_asked_to(testdir):
    """Ensure marking a test is backing up old results if asked to."""
    results_path = testdir.tmpdir.join("results.json")
    results_path.ensure(file=True)  # 'touch' the file

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(test_file=DUMMY_TEST_QUERY)

    with mock.patch("pytest_django_queries.plugin.create_backup") as mocked_backup:
        results = testdir.runpytest("--django-db-bench", results_path)
        assert mocked_backup.call_count == 0

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)
    assert results_path.check()


def test_fixture_is_backing_up_old_results_to_default_path_if_no_path_provided(testdir):
    """Ensure marking a test is backing up old results if asked to."""
    results_path = testdir.tmpdir.join("results.json")
    results_path.ensure(file=True)  # 'touch' the file

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(test_file=DUMMY_TEST_QUERY)

    with mock.patch("pytest_django_queries.plugin.create_backup") as mocked_backup:
        from pytest_django_queries.plugin import DEFAULT_OLD_RESULT_FILENAME

        results = testdir.runpytest(
            "--django-db-bench", results_path, "--django-backup-queries"
        )
        mocked_backup.assert_called_with(str(results_path), DEFAULT_OLD_RESULT_FILENAME)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)
    assert results_path.check()


def test_marker_message(testdir):
    """Ensure the custom markers configuration is added to pytest."""
    result = testdir.runpytest("--markers")
    result.stdout.fnmatch_lines(
        [
            "@pytest.mark.count_queries: "
            "Mark the test as to have their database query counted."
        ]
    )


def test_implements_custom_options(testdir):
    """Ensure the custom options are added to pytest."""
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines(
        [
            "django-queries:",
            "*--django-db-bench=PATH",
            "*Output file for storing the results. Default: .pytest-",
            "*queries",
            "*--django-backup-queries=[[]PATH[]]",
            "*Whether the old results should be backed up or not",
            "*before overriding",
        ]
    )


def test_duplicated_queries(testdir):
    results_path = testdir.tmpdir.join("results.json")

    script = testdir.makepyfile(
        test_module="""
        import pytest

        @pytest.mark.count_queries
        def test_foo():

            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT date('now');")
                cursor.execute("SELECT 1;")
                cursor.execute("SELECT 1;")
                cursor.execute("SELECT 1;")
                cursor.fetchone()"""
    )

    results = testdir.runpytest("--django-db-bench", results_path, script)

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)
    assert results_path.check()

    # Check the resulst
    assert json.load(results_path) == {
        "test_module": {"test_foo": {"duplicates": 2, "query-count": 4}}
    }


def test_xdist_combine_racecondition(testdir):
    try:
        import xdist  # noqa
    except ImportError:
        pytest.skip("pytest-xdist is not installed.")

    results_path = testdir.tmpdir.join("results.json")

    script = testdir.makepyfile(
        test_module="""
        import pytest
        import sys

        @pytest.mark.parametrize("foo", range(500))
        @pytest.mark.count_queries
        def test_foo(foo):

            from django.db import connection

            with connection.cursor() as cursor:
                cursor.execute("SELECT date('now');")
                cursor.execute("SELECT 1;")
                cursor.fetchone()"""
    )

    # Append current test files into the temporary test directory in order
    # to have settings.py available for PyPi packages
    shutil.copytree(os.path.dirname(__file__), os.path.join(str(testdir) + "/tests"))
    results = testdir.runpytest("--django-db-bench", results_path, "-n", "5", script)

    # Ensure the tests have passed
    results.assert_outcomes(500, 0, 0)
    assert results_path.check()

    # Check the results
    results = json.load(results_path)
    assert list(results.keys()) == ["test_module"]
    assert len(results["test_module"]) == 500
