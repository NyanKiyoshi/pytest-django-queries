import json
import os.path
import shutil
import tempfile
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


def is_slave(config):
    return hasattr(config, "slaveinput")


def get_slaveid(config):
    if hasattr(config, "slaveinput"):
        return config.workerinput["slaveid"]
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
    query_count = len(queries)

    result_line = "%s\t%s\t%s\n" % (module_name, test_name, query_count)
    save_path = os.path.join(dirout, get_slaveid(request.config))
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

                module_name, test_name, query_count = result_line.split("\t")

                module_entries = test_results.setdefault(module_name, {})
                module_entries[test_name] = {"query-count": int(query_count)}

    if test_results:
        save_results_to_json(
            save_path=config.known_args_namespace.queries_results_save_path,
            backup_path=config.known_args_namespace.queries_backup_results,
            data=test_results,
        )

    # clean up the temporary directory
    shutil.rmtree(config.django_queries_shared_directory)


def pytest_configure_node(node):
    node.slaveinput[
        "_django_queries_shared_dir"
    ] = node.config.django_queries_shared_directory


pytest_configure_node.optionalhook = True


def get_shared_directory(request):
    """Returns a unique and temporary directory which can be shared by
    master or worker nodes in xdist runs.
    """
    if not is_slave(request.config):
        return request.config.django_queries_shared_directory
    else:
        return request.config.slaveinput["_django_queries_shared_dir"]


@pytest.fixture
def count_queries(request):
    """Wrap a test to count the number of performed queries."""
    from django.db import connection

    with CaptureQueriesContext(connection) as context:
        yield context
    add_entry(request, context, get_shared_directory(request))
