import json
from datetime import datetime
from os import environ

import pytest
from django.test.utils import CaptureQueriesContext

# Defines the environment variable name
# for overriding the export path
ENV_QUERY_SAVE_PATH = 'PYTEST_QUERIES_SAVE_PATH'

# Defines the plugin marker name
PYTEST_QUERY_COUNT_MARKER = 'count_queries'


def _get_date_now():
    return datetime.now().strftime('%m-%d-%Y-%H-%M-%S')


def _make_save_path():
    """Retrieve the save path from the environment variable value or make one
    using the current date and time."""
    return environ.get(ENV_QUERY_SAVE_PATH, None) or (
        '.pytest-queries-{}.json'.format(_get_date_now()))


def _set_session(config, new_session):
    config.pytest_django_queries_session = new_session


def _get_session(request):
    return request.config.pytest_django_queries_session


class _Session(object):
    def __init__(self):
        self._data = {}

    def add_entry(self, module_name, test_name, query_count):
        module_data = self._data.setdefault(module_name, {})
        module_data[test_name] = {'query-count': query_count}

    def save_json(self):
        with open(_make_save_path(), 'w') as fp:
            json.dump(self._data, fp, indent=2)

    def finish(self):
        """Serialize and export the test data if performance tests were run."""

        if not self._data:
            return

        self.save_json()


@pytest.mark.tryfirst
def pytest_configure(config):
    """Append the plugin markers to the pytest configuration."""
    config_line = (
       '%s: Mark the test as to have their queries counted.'
       '' % PYTEST_QUERY_COUNT_MARKER)
    config.addinivalue_line('markers', config_line)
    _set_session(config, _Session())


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus):
    _get_session(session).finish()
    yield


@pytest.fixture(autouse=True)
def _pytest_query_marker(request):
    """Use the fixture to count the queries on the current node if it's
    marked with 'count_queries'."""
    marker = request.node.get_closest_marker(PYTEST_QUERY_COUNT_MARKER)
    if marker:
        request.getfixturevalue('count_queries')


@pytest.fixture
def count_queries(request):
    """Wrap a test to count the number of performed queries."""
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        yield context
        query_count = len(context)

    module = request.node.module.__name__
    bench_name = request.node.name
    _get_session(request).add_entry(module, bench_name, query_count)
