import json
from datetime import datetime
from os import environ
from threading import RLock

import pytest
from django.test.utils import CaptureQueriesContext

lock = RLock()
_test_data = {}


def _get_date_now():
    return datetime.now().strftime('%m-%d-%Y-%H-%M-%S')


def _get_save_path():
    return environ.get('PYTEST_QUERIES_SAVE_PATH', None) or (
        '.pytest-queries-{}.json'.format(_get_date_now()))


def _add_test_to_data(module_name, test_name, query_count):
    with lock:
        _test_data.setdefault(module_name, {})[test_name] = {
            'query-count': query_count}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_unconfigure(config):
    yield

    with open(_get_save_path(), 'w') as w:
        json.dump(_test_data, w, indent=2)


@pytest.fixture(autouse=True, scope='function')
def trap_queries(request):
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        yield context
        query_count = len(context)

    module = request.node.module.__name__
    bench_name = request.node.name
    _add_test_to_data(module, bench_name, query_count)
