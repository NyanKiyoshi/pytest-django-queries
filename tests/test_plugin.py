import json

import mock

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
        "test_file": {"test_count_db_query_number": {"query-count": 2}}
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

    # Ensure the tests have passed
    results.assert_outcomes(0, 0, 1)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
        "test_plugin_exports_results_even_when_test_fails": {
            "test_failure": {"query-count": 0}
        }
    }


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
        "test_file": {"test_count_db_query_number": {"query-count": 2}},
        "test_otherfile": {"test_count_db_query_number": {"query-count": 2}},
    }
    assert json.load(old_results_path) == {
        "test_file": {"test_count_db_query_number": {"query-count": 2}}
    }


def test_fixture_is_not_backing_up_if_not_asked_to(testdir):
    """Ensure marking a test is backing up old results if asked to."""
    results_path = testdir.tmpdir.join("results.json")
    results_path.ensure(file=True)  # 'touch' the file

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(test_file=DUMMY_TEST_QUERY)

    with mock.patch("pytest_django_queries.plugin._create_backup") as mocked_backup:
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

    with mock.patch("pytest_django_queries.plugin._create_backup") as mocked_backup:
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
            "Mark the test as to have their queries counted."
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
