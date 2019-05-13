import json

import pytest
from django.test.utils import CaptureQueriesContext

# Defines the plugin marker name
PYTEST_QUERY_COUNT_MARKER = 'count_queries'


def _set_session(config, new_session):
    config.pytest_django_queries_session = new_session


def _get_session(request):
    return request.config.pytest_django_queries_session


class _Session(object):
    def __init__(self, save_path):
        self.save_path = save_path
        self._data = {}

    def add_entry(self, module_name, test_name, query_count):
        module_data = self._data.setdefault(module_name, {})
        module_data[test_name] = {'query-count': query_count}

    def save_json(self):
        with open(self.save_path, 'w') as fp:
            json.dump(self._data, fp, indent=2)

    def finish(self):
        """Serialize and export the test data if performance tests were run."""

        if not self._data:
            return

        self.save_json()


def pytest_addoption(parser):
    group = parser.getgroup('django-queries')
    group.addoption(
        '--django-db-bench',
        dest='queries_results_save_path',
        action='store',
        default='.pytest-queries',
        metavar='PATH',
        help='Output file for storing the results. Default: .pytest-queries')


@pytest.mark.tryfirst
def pytest_configure(config):
    """Append the plugin markers to the pytest configuration."""
    config_line = (
       '%s: Mark the test as to have their queries counted.'
       '' % PYTEST_QUERY_COUNT_MARKER)
    config.addinivalue_line('markers', config_line)


@pytest.mark.tryfirst
def pytest_load_initial_conftests(early_config, parser, args):
    _set_session(
        early_config,
        _Session(early_config.known_args_namespace.queries_results_save_path))


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
