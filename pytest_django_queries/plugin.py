import json
from datetime import datetime
from os import environ
from threading import RLock

import pytest
from django.test.utils import CaptureQueriesContext

lock = RLock()
_test_data = {}

ENV_QUERY_SAVE_PATH = 'PYTEST_QUERIES_SAVE_PATH'
PYTEST_QUERY_COUNT_MARKER = 'count_queries'


def _get_date_now():
    return datetime.now().strftime('%m-%d-%Y-%H-%M-%S')


def _get_save_path():
    """Retrieve the save path from the environment variable value or make one
    using the current date and time."""
    return environ.get(ENV_QUERY_SAVE_PATH, None) or (
        '.pytest-queries-{}.json'.format(_get_date_now()))


def _add_test_to_data(module_name, test_name, query_count):
    with lock:
        _test_data.setdefault(module_name, {})[test_name] = {
            'query-count': query_count}


def pytest_load_initial_conftests(early_config, parser, args):
    """Append the plugin markers to the pytest configuration."""
    config_line = (
       '%s: Mark the test as to have their queries counted.'
       '' % PYTEST_QUERY_COUNT_MARKER)
    early_config.addinivalue_line('markers', config_line)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_unconfigure(config):
    """Serialize and export the test data if performance tests were run."""
    yield

    if not _test_data:
        return

    with open(_get_save_path(), 'w') as w:
        json.dump(_test_data, w, indent=2)


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
    _add_test_to_data(module, bench_name, query_count)
