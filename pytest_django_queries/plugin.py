import json
import os.path
import shutil
import tempfile
import warnings
from os import listdir
from os.path import isfile

import pytest
from django.test.utils import CaptureQueriesContext

# Defines the plugin marker name
from pytest_django_queries.utils import create_backup

PYTEST_QUERY_COUNT_MARKER = "count_queries"
PYTEST_QUERY_COUNT_FIXTURE_NAME = "count_queries"
DEFAULT_RESULT_FILENAME = ".pytest-queries"
DEFAULT_OLD_RESULT_FILENAME = ".pytest-queries.old"


def get_worker_input(node):
    workerinput = getattr(node, "workerinput", None)
    if workerinput is None:
        workerinput = node.slaveinput
        warnings.warn(
            "pytest-xdist<2.0 support will be dropped in pytest-django-queries 2.0",
            category=DeprecationWarning,
        )
    return workerinput


def is_worker(config):
    return hasattr(config, "workerinput") or hasattr(config, "slaveinput")


def get_workerid(config):
    if hasattr(config, "workerinput"):
        return config.workerinput["workerid"]
    elif hasattr(config, "slaveinput"):
        # Deprecated: will be removed in pytest-django-queries 2.0
        return config.slaveinput["slaveid"]
    else:
        return "master"


def save_results_to_json(save_path, backup_path, data):
    if backup_path and isfile(save_path):
        create_backup(save_path, backup_path)

    with open(save_path, "w") as fp:
        json.dump(data, fp, indent=2)


def add_entry(request, queries, dirout):
    module_name = request.node.module.__name__
    test_name = request.node.name
    queries = queries[:]
    query_count = len(queries)
    duplicate_count = query_count - len(set((q["sql"] for q in queries)))

    result_line = "%s\t%s\t%d\t%d\n" % (
        module_name,
        test_name,
        query_count,
        duplicate_count,
    )
    save_path = os.path.join(dirout, get_workerid(request.config))
    if os.path.isfile(save_path):
        mode = "a"
    else:
        mode = "w"

    with open(save_path, mode=mode) as fp:
        fp.write(result_line)


def pytest_addoption(parser):
    group = parser.getgroup("django-queries")
    group.addoption(
        "--django-db-bench",
        dest="queries_results_save_path",
        action="store",
        default=DEFAULT_RESULT_FILENAME,
        metavar="PATH",
        help="Output file for storing the results. Default: .pytest-queries",
    )
    group.addoption(
        "--django-backup-queries",
        dest="queries_backup_results",
        action="store",
        default=None,
        metavar="PATH",
        help="Whether the old results should be backed up or not before overriding",
        nargs="?",
    )


@pytest.mark.tryfirst
def pytest_load_initial_conftests(early_config, parser, args):
    """
    :param early_config:
    :param parser:
    :param args:
    :type args: tuple|list
    :return:
    """
    early_config.addinivalue_line(
        "markers",
        "%s: Mark the test as to have their database query counted."
        "" % PYTEST_QUERY_COUNT_MARKER,
    )

    backup_path = early_config.known_args_namespace.queries_backup_results

    # Set default value if the flag was provided without value in arguments
    if backup_path is None and "--django-backup-queries" in args:
        backup_path = DEFAULT_OLD_RESULT_FILENAME

    early_config.known_args_namespace.queries_backup_results = backup_path


def _process_query_count_marker(request, *_args, **kwargs):
    autouse = kwargs.setdefault("autouse", True)
    if autouse:
        request.getfixturevalue(PYTEST_QUERY_COUNT_FIXTURE_NAME)


@pytest.fixture(autouse=True)
def _pytest_query_marker(request):
    """Use the fixture to count the queries on the current node if it's
    marked with 'count_queries'.

    Optional keyword-arguments:
        - autouse (bool, default: True)
          Whether the fixture should be used automatically.
          This might be useful if you are executing fixtures
          that are making queries and still want to mark the test
          but place the fixture manually."""
    marker = request.node.get_closest_marker(PYTEST_QUERY_COUNT_MARKER)
    if marker:
        _process_query_count_marker(request, *marker.args, **marker.kwargs)


def pytest_configure(config):
    config.django_queries_shared_directory = tempfile.mkdtemp(
        prefix="pytest-django-queries"
    )


def pytest_unconfigure(config):
    results_path = config.django_queries_shared_directory
    test_results = {}

    for filename in listdir(results_path):
        with open(os.path.join(results_path, filename)) as fp:
            for result_line in fp.readlines():
                result_line = result_line.strip()

                if not result_line:
                    continue

                module_name, test_name, query_count, duplicates = result_line.split(
                    "\t"
                )

                module_entries = test_results.setdefault(module_name, {})
                module_entries[test_name] = {
                    "query-count": int(query_count),
                    "duplicates": int(duplicates),
                }

    if test_results:
        save_results_to_json(
            save_path=config.known_args_namespace.queries_results_save_path,
            backup_path=config.known_args_namespace.queries_backup_results,
            data=test_results,
        )

    # clean up the temporary directory
    shutil.rmtree(config.django_queries_shared_directory)


def pytest_configure_node(node):
    workerinput = get_worker_input(node)
    workerinput[
        "_django_queries_shared_dir"
    ] = node.config.django_queries_shared_directory


pytest_configure_node.optionalhook = True


def get_shared_directory(request):
    """Returns a unique and temporary directory which can be shared by
    master or worker nodes in xdist runs.
    """
    if not is_worker(request.config):
        return request.config.django_queries_shared_directory
    else:
        return get_worker_input(request.config)["_django_queries_shared_dir"]


@pytest.fixture
def count_queries(request):
    """Wrap a test to count the number of performed queries."""
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        yield context
    add_entry(request, context, get_shared_directory(request))
