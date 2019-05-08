import click
from beautifultable import BeautifulTable

from pytest_django_queries.cli_utils import raise_error


class TestEntryData(object):
    BASE_FIELDS = [
        ('test_name', 'Test Name')
    ]
    REQUIRED_FIELDS = [
        ('query-count', 'Queries'),
    ]
    FIELDS = BASE_FIELDS + REQUIRED_FIELDS

    def __init__(self, test_name, data):
        """
        :param data: The test entry's data.
        :type data: dict
        """

        if type(data) != dict:
            raise_error(
                'Expected a dictionary, got %s instead' % type(data).__name__)

        self._raw_data = data
        self.test_name = test_name

        for field, _ in self.REQUIRED_FIELDS:
            setattr(self, field, self._get_required_key(field))

    def _get_required_key(self, key):
        if key in self._raw_data:
            return self._raw_data.get(key)
        raise_error('Got invalid data. It is missing a required key: %s' % key)


def iter_entries(entries):
    for module_name, module_data in entries.items():
        yield module_name, (
            TestEntryData(test_name, test_data)
            for test_name, test_data in module_data.items())


def print_entries(data):
    table = BeautifulTable()
    table.column_headers = ['Module', 'Tests']
    for module_name, module_entries in iter_entries(data):
        subtable = BeautifulTable()
        subtable.column_headers = [field for _, field in TestEntryData.FIELDS]
        for entry in module_entries:
            subtable.append_row([
                getattr(entry, field) for field, _ in TestEntryData.FIELDS])
        table.append_row([module_name, subtable])
    click.echo(table)
