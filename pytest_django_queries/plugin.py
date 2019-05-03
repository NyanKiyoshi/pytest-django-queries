from pprint import pprint
from threading import RLock

import pytest
from django.test.utils import CaptureQueriesContext

lock = RLock()
_test_data = {}


def _add_test_to_data(module_name, test_name, query_count):
    with lock:
        _test_data.setdefault(module_name, {})[test_name] = {
            'query-count': query_count}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_unconfigure(config):
    yield
    pprint(_test_data)


@pytest.fixture(autouse=True, scope='function')
def trap_queries(request):
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        yield context
        query_count = len(context)

    module = request.node.module.__name__
    bench_name = request.node.name
    _add_test_to_data(module, bench_name, query_count)
