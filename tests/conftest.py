import pytest

from pytest_django_queries.plugin import ENV_QUERY_SAVE_PATH

pytest_plugins = 'pytester'


@pytest.fixture()
def temp_results(testdir, monkeypatch):
    # Make a dummy path where to save the results
    # and override the dump path by setting the PYTEST_QUERIES_SAVE_PATH
    # environment variable
    results_path = testdir.tmpdir.join('results.json')
    monkeypatch.setenv(ENV_QUERY_SAVE_PATH, str(results_path))

    return testdir, results_path
