import json

from freezegun import freeze_time

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
    assert request.config.pluginmanager.hasplugin('django_queries')


def test_fixture_is_invoked_when_marked(temp_results):
    """Ensure marking a test is actually calling the fixture."""
    testdir, results_path = temp_results

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile(DUMMY_TEST_QUERY)
    results = testdir.runpytest()

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
      "test_fixture_is_invoked_when_marked": {
        "test_count_db_query_number": {
          "query-count": 2
        }
      }
    }


def test_plugin_exports_nothing_if_empty(temp_results):
    """Ensure the plugin does not export any results if no performance
    tests were run."""

    testdir, results_path = temp_results

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile("""
        def test_nothing():
            pass
    """)
    results = testdir.runpytest()

    # Ensure the tests have passed
    results.assert_outcomes(1, 0, 0)

    # Ensure the results file was not created
    assert not results_path.check()


def test_plugin_exports_results_even_when_test_fails(temp_results):
    """Ensure the plugin does not export any results if no performance
    tests were run."""

    testdir, results_path = temp_results

    # Run a dummy test that performs queries
    # and triggers a counting of the query number
    testdir.makepyfile("""
        import pytest

        @pytest.mark.count_queries
        def test_failure():
            assert 0
    """)
    results = testdir.runpytest()

    # Ensure the tests have passed
    results.assert_outcomes(0, 0, 1)

    # Ensure the results file was created
    assert results_path.check()
    assert json.load(results_path) == {
      "test_plugin_exports_results_even_when_test_fails": {
        "test_failure": {
          "query-count": 0
        }
      }
    }


def test_marker_message(testdir):
    """Ensure the custom markers configuration is added to pytest."""
    result = testdir.runpytest('--markers')
    result.stdout.fnmatch_lines([
        '@pytest.mark.count_queries: '
        'Mark the test as to have their queries counted.'])


@freeze_time('2012-01-14 03:21:34')
def test_get_save_path_returns_filename_with_date():
    from pytest_django_queries.plugin import _make_save_path

    filename = _make_save_path()
    assert filename.startswith('.pytest-queries-')
    assert filename.endswith('-01-14-2012-03-21-34.json')
